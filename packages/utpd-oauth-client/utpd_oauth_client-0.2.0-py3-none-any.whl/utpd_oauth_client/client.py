"""Framework-agnostic OAuth client for the utpd-oauth service."""

import contextlib
from typing import Final
from urllib.parse import urlencode

import httpx

from .exceptions import (
    InvalidResponseError,
    MissingTokenError,
    NetworkError,
    TokenExchangeError,
)

DEFAULT_TIMEOUT: Final = 10.0


class OAuthClient:
    """Client for interacting with the utpd-oauth service.

    This client handles the two main operations needed by consuming applications:
    1. Building the login URL to redirect users to start the OAuth flow
    2. Exchanging the token_code (received after OAuth) for an access_token

    The client is stateless and thread-safe. It creates a new httpx connection
    for each exchange request, making it suitable for use across multiple
    concurrent requests.

    Example:
        client = OAuthClient("https://utpd-oauth.ward.au")

        # Step 1: Redirect user to login
        login_url = client.login_url("https://myapp.com/auth/callback")

        # Step 2: After OAuth completes, exchange the token_code
        access_token = await client.exchange(token_code)
    """

    def __init__(self, base_url: str, *, timeout: float = DEFAULT_TIMEOUT) -> None:
        """Initialise the client with the utpd-oauth service URL.

        Args:
            base_url: Base URL of the utpd-oauth service (e.g. "https://utpd-oauth.ward.au").
            timeout: Request timeout in seconds for the token exchange.
        """
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    @property
    def base_url(self) -> str:
        """The base URL of the utpd-oauth service."""
        return self._base_url

    def login_url(self, next_url: str) -> str:
        """Build the URL to redirect users to start the OAuth flow.

        Args:
            next_url: Where utpd-oauth should redirect after successful authentication.
                      This is typically your application's callback endpoint.

        Returns:
            The full URL to redirect the user to.
        """
        params = urlencode({"next_url": next_url})
        return f"{self._base_url}/login?{params}"

    async def exchange(self, token_code: str) -> str:
        """Exchange a token_code for an access_token.

        This should be called from your callback endpoint after the user
        completes the OAuth flow. The token_code is a one-time-use code
        that expires quickly.

        Args:
            token_code: The one-time code received from utpd-oauth via query parameter.

        Returns:
            The Untappd access_token for API calls.

        Raises:
            NetworkError: If a network error occurs during the exchange.
            TokenExchangeError: If the OAuth service returns an error status.
            InvalidResponseError: If the response is not valid JSON.
            MissingTokenError: If the response doesn't contain an access_token.
        """
        url = f"{self._base_url}/get-token"

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as http:
                response = await http.post(url, json={"token_code": token_code})
        except httpx.HTTPError as exc:
            raise NetworkError(detail=str(exc)) from exc

        if response.status_code != httpx.codes.OK:
            detail = self._extract_error_detail(response)
            raise TokenExchangeError(status_code=response.status_code, detail=detail)

        try:
            data = response.json()
        except ValueError as exc:
            raise InvalidResponseError(status_code=response.status_code) from exc

        if access_token := data.get("access_token"):
            return access_token

        raise MissingTokenError(status_code=response.status_code)

    def _extract_error_detail(self, response: httpx.Response) -> str | None:
        """Attempt to extract error detail from a failed response."""
        with contextlib.suppress(ValueError):
            data = response.json()
            if isinstance(data, dict):
                return data.get("detail") or data.get("error")
        return response.text[:200] if response.text else None
