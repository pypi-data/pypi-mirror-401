"""Exception hierarchy for the OAuth client."""


class OAuthClientError(Exception):
    """Base exception for all OAuth client errors."""


class TokenExchangeError(OAuthClientError):
    """Raised when token exchange with the OAuth service fails.

    Attributes:
        status_code: HTTP status code from the failed request, if available.
        detail: Additional error detail from the service response.
    """

    _message = "Token exchange failed"

    def __init__(
        self,
        *,
        status_code: int | None = None,
        detail: str | None = None,
    ) -> None:
        """Initialise the error with context about the failure."""
        super().__init__(self._message)
        self.status_code = status_code
        self.detail = detail

    def __str__(self) -> str:
        """Format the error with available context."""
        parts = [self._message]
        if self.status_code is not None:
            parts.append(f"status={self.status_code}")
        if self.detail:
            parts.append(f"detail={self.detail}")
        return " ".join(parts)


class NetworkError(TokenExchangeError):
    """Raised when a network error occurs during token exchange."""

    _message = "Network error during token exchange"


class InvalidResponseError(TokenExchangeError):
    """Raised when the OAuth service returns an invalid response."""

    _message = "Invalid response from OAuth service"


class MissingTokenError(TokenExchangeError):
    """Raised when the response is missing the access_token field."""

    _message = "Response missing access_token"
