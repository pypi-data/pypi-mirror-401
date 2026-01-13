"""Custom error classes for the NoSpoon Integrations SDK."""

from typing import Optional


class IntegrationError(Exception):
    """Base error class for all integration errors."""

    def __init__(self, message: str, provider: Optional[str] = None):
        self.provider = provider
        formatted_message = f"[{provider}] {message}" if provider else message
        super().__init__(formatted_message)


class OAuthError(IntegrationError):
    """OAuth-related error (authorization, token exchange, etc.)."""

    def __init__(self, provider: str, message: str, original_error: Optional[str] = None):
        self.original_error = original_error
        super().__init__(message, provider)


class TokenNotFoundError(IntegrationError):
    """No tokens found for user."""

    def __init__(self, provider: str, user_id: Optional[str] = None):
        self.user_id = user_id
        message = f"No tokens found for user {user_id}" if user_id else "No tokens found"
        super().__init__(message, provider)


class TokenExpiredError(IntegrationError):
    """Token expired and cannot be refreshed."""

    def __init__(self, provider: str, user_id: Optional[str] = None, reason: str = ""):
        self.user_id = user_id
        self.reason = reason
        if user_id:
            message = f"Token expired for user {user_id}"
        else:
            message = f"Token expired: {reason}" if reason else "Token expired"
        super().__init__(message, provider)


class TokenRefreshError(IntegrationError):
    """Token refresh failed."""

    def __init__(self, provider: str, message: str):
        super().__init__(message, provider)


class ProviderAPIError(IntegrationError):
    """Error from provider API."""

    def __init__(
        self,
        provider: str,
        status_code: int,
        message: str,
        response_body: Optional[str] = None,
    ):
        self.status_code = status_code
        self.response_body = response_body
        super().__init__(f"API error ({status_code}): {message}", provider)


class ConfigurationError(IntegrationError):
    """Configuration error (missing credentials, invalid config, etc.)."""

    pass
