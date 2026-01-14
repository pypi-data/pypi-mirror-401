"""NiceGUI integration for the OAuth client.

Provides helpers to add OAuth routes to a NiceGUI application. Since NiceGUI
is built on Starlette, we use raw HTTP routes for the OAuth flow (which involves
redirects) rather than UI pages.

Example:
    from nicegui import app, ui
    from utpd_oauth_client import OAuthClient
    from utpd_oauth_client.nicegui import setup_oauth_routes

    client = OAuthClient(os.getenv("OAUTH_SERVICE_URL"))

    async def handle_token(token: str, request: Request) -> Response:
        app.storage.user["access_token"] = token
        return RedirectResponse("/")

    setup_oauth_routes(
        app=app,
        client=client,
        public_base_url=os.getenv("PUBLIC_BASE_URL"),
        on_token=handle_token,
    )
"""

from collections.abc import Awaitable, Callable
from typing import Protocol

try:
    from nicegui import App
    from starlette.requests import Request
    from starlette.responses import JSONResponse, RedirectResponse, Response
except ImportError as exc:
    msg = (
        "NiceGUI integration requires nicegui to be installed. "
        "Install it with: pip install nicegui"
    )
    raise ImportError(msg) from exc

from .client import OAuthClient
from .exceptions import TokenExchangeError


class TokenHandler(Protocol):
    """Protocol for the callback that handles a successfully exchanged token.

    The handler receives the access_token and the Starlette request, and must
    return a Response (typically a redirect to the app's main page).
    """

    async def __call__(self, token: str, request: Request) -> Response:
        """Handle the received access token."""
        ...


def setup_oauth_routes(  # noqa: PLR0913 - factory function with sensible defaults
    *,
    app: App,
    client: OAuthClient,
    public_base_url: str,
    on_token: Callable[[str, Request], Awaitable[Response]],
    start_path: str = "/auth/start",
    callback_path: str = "/auth/callback",
    error_handler: Callable[[TokenExchangeError, Request], Awaitable[Response]]
    | None = None,
) -> None:
    """Add OAuth routes to a NiceGUI application.

    This function adds two HTTP routes to your NiceGUI app:
    - Start route: Redirects the user to utpd-oauth to begin the flow
    - Callback route: Receives the token_code, exchanges it, and calls on_token

    These are raw Starlette routes (not @ui.page decorated) since they handle
    redirects rather than rendering UI.

    Args:
        app: The NiceGUI app instance (from `from nicegui import app`).
        client: The OAuthClient instance configured with the utpd-oauth service URL.
        public_base_url: Your application's public URL (e.g. "https://myapp.com").
                         Used to build the callback URL that utpd-oauth redirects to.
        on_token: Async callback invoked with the access_token after successful exchange.
                  Must return a Response (typically RedirectResponse to your app).
        start_path: URL path for the "start OAuth" endpoint. Default: "/auth/start".
        callback_path: URL path for the callback endpoint. Default: "/auth/callback".
        error_handler: Optional async callback for handling token exchange errors.
                       If not provided, returns a JSON error response.

    Example:
        from nicegui import app, ui
        from starlette.responses import RedirectResponse

        async def handle_token(token: str, request: Request) -> Response:
            app.storage.user["access_token"] = token
            app.storage.user["authenticated"] = True
            return RedirectResponse("/")

        setup_oauth_routes(
            app=app,
            client=oauth_client,
            public_base_url="https://beer.example.com",
            on_token=handle_token,
        )

        @ui.page("/")
        def main_page():
            if not app.storage.user.get("authenticated"):
                ui.link("Login with Untappd", "/auth/start")
            else:
                ui.label("Welcome!")
    """
    callback_url = f"{public_base_url.rstrip('/')}{callback_path}"

    async def auth_start(_request: Request) -> Response:
        """Redirect user to utpd-oauth to begin the OAuth flow."""
        login_url = client.login_url(callback_url)
        return RedirectResponse(login_url)

    async def auth_callback(request: Request) -> Response:
        """Handle the OAuth callback and exchange token_code for access_token."""
        token_code = request.query_params.get("token_code")

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

    app.add_route(start_path, auth_start, methods=["GET"])
    app.add_route(callback_path, auth_callback, methods=["GET"])
