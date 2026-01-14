"""Client library for the utpd-oauth service.

This package provides a framework-agnostic client for exchanging OAuth token codes
with the utpd-oauth service, plus optional integrations for FastAPI and NiceGUI.

Basic usage:
    from utpd_oauth_client import OAuthClient

    client = OAuthClient("https://utpd-oauth.example.com")
    login_url = client.login_url("https://myapp.com/callback")
    # ... user completes OAuth flow, returns with token_code ...
    access_token = await client.exchange(token_code)

FastAPI integration:
    from utpd_oauth_client.fastapi import create_auth_router

NiceGUI integration:
    from utpd_oauth_client.nicegui import setup_oauth_routes
"""

from .client import OAuthClient
from .exceptions import (
    InvalidResponseError,
    MissingTokenError,
    NetworkError,
    OAuthClientError,
    TokenExchangeError,
)

__all__ = [
    "InvalidResponseError",
    "MissingTokenError",
    "NetworkError",
    "OAuthClient",
    "OAuthClientError",
    "TokenExchangeError",
]
