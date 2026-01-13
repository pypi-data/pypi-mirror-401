"""NoSpoon Integrations SDK - Cross-platform OAuth integrations."""

from nospoon_integrations.client import IntegrationClient
from nospoon_integrations.core.errors import (
    IntegrationError,
    OAuthError,
    ProviderAPIError,
    TokenExpiredError,
    TokenNotFoundError,
    TokenRefreshError,
)
from nospoon_integrations.core.types import (
    ConnectionStatus,
    OAuthCallbackParams,
    ProviderConfig,
    TokenData,
    TokenRefreshResult,
    TokenStorage,
)

__version__ = "0.1.0"

__all__ = [
    "ConnectionStatus",
    "IntegrationClient",
    "IntegrationError",
    "OAuthCallbackParams",
    "OAuthError",
    "ProviderAPIError",
    "ProviderConfig",
    "TokenData",
    "TokenExpiredError",
    "TokenNotFoundError",
    "TokenRefreshError",
    "TokenRefreshResult",
    "TokenStorage",
    "__version__",
]
