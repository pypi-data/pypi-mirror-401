"""FastAPI integration for the OAuth client.

Provides a router factory that handles the OAuth redirect flow, leaving only
the application-specific token handling to the consuming app.

Example:
    from utpd_oauth_client import OAuthClient
    from utpd_oauth_client.fastapi import create_auth_router

    client = OAuthClient(settings.oauth_service_url)

    async def handle_token(token: str, request: Request) -> Response:
        # Store token, create session, etc.
        request.session["access_token"] = token
        return RedirectResponse("/")

    router = create_auth_router(
        client=client,
        public_base_url=settings.public_base_url,
        on_token=handle_token,
    )
    app.include_router(router)
"""

from collections.abc import Awaitable, Callable
from typing import Protocol

try:
    from fastapi import APIRouter, Request
    from fastapi.responses import JSONResponse, RedirectResponse
    from starlette.responses import Response
except ImportError as exc:
    msg = (
        "FastAPI integration requires fastapi to be installed. "
        "Install it with: pip install fastapi"
    )
    raise ImportError(msg) from exc

from .client import OAuthClient
from .exceptions import TokenExchangeError


class TokenHandler(Protocol):
    """Protocol for the callback that handles a successfully exchanged token.

    The handler receives the access_token and the original request, and must
    return a Response (typically a redirect to the app's main page).
    """

    async def __call__(self, token: str, request: Request) -> Response:
        """Handle the received access token."""
        ...


def create_auth_router(
    *,
    client: OAuthClient,
    public_base_url: str,
    on_token: Callable[[str, Request], Awaitable[Response]],
    start_path: str = "/auth/start",
    callback_path: str = "/auth/callback",
    error_handler: Callable[[TokenExchangeError, Request], Awaitable[Response]]
    | None = None,
) -> APIRouter:
    """Create a FastAPI router with OAuth start and callback endpoints.

    This factory creates two endpoints:
    - Start endpoint: Redirects the user to utpd-oauth to begin the flow
    - Callback endpoint: Receives the token_code, exchanges it, and calls on_token

    Args:
        client: The OAuthClient instance configured with the utpd-oauth service URL.
        public_base_url: Your application's public URL (e.g. "https://myapp.com").
                         Used to build the callback URL that utpd-oauth redirects to.
        on_token: Async callback invoked with the access_token after successful exchange.
                  Must return a Response (typically RedirectResponse to your app).
        start_path: URL path for the "start OAuth" endpoint. Default: "/auth/start".
        callback_path: URL path for the callback endpoint. Default: "/auth/callback".
        error_handler: Optional async callback for handling token exchange errors.
                       If not provided, returns a JSON error response.

    Returns:
        A FastAPI APIRouter ready to be included in your application.

    Example:
        async def handle_token(token: str, request: Request) -> Response:
            user_id = await create_or_get_user(token)
            request.session["user_id"] = user_id
            return RedirectResponse("/dashboard")

        router = create_auth_router(
            client=oauth_client,
            public_base_url="https://beer.example.com",
            on_token=handle_token,
        )
        app.include_router(router)
    """
    router = APIRouter()
    callback_url = f"{public_base_url.rstrip('/')}{callback_path}"

    @router.get(start_path)
    async def auth_start() -> Response:
        """Redirect user to utpd-oauth to begin the OAuth flow."""
        login_url = client.login_url(callback_url)
        return RedirectResponse(login_url)

    @router.get(callback_path)
    async def auth_callback(request: Request, token_code: str | None = None) -> Response:
        """Handle the OAuth callback and exchange token_code for access_token."""
        if not token_code:
            return JSONResponse(
                {"error": "Missing token_code parameter"},
                status_code=400,
            )

        try:
            access_token = await client.exchange(token_code)
        except TokenExchangeError as exc:
            if error_handler:
                return await error_handler(exc, request)
            return JSONResponse(
                {"error": str(exc)},
                status_code=exc.status_code or 502,
            )

        return await on_token(access_token, request)

    return router
