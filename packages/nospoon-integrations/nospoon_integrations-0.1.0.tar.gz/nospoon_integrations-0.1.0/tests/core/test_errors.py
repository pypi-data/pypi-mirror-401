"""Tests for custom error classes."""

from nospoon_integrations.core.errors import (
    IntegrationError,
    OAuthError,
    ProviderAPIError,
    TokenExpiredError,
    TokenNotFoundError,
    TokenRefreshError,
)


class TestIntegrationError:
    """Tests for the base IntegrationError class."""

    def test_creates_base_error_with_message(self):
        """Should create base error with message."""
        error = IntegrationError("Something went wrong")
        assert str(error) == "Something went wrong"
        assert isinstance(error, Exception)


class TestOAuthError:
    """Tests for OAuthError class."""

    def test_creates_oauth_error_with_provider(self):
        """Should create OAuth error with provider."""
        error = OAuthError("google", "Invalid authorization code")
        assert "[google]" in str(error)
        assert "Invalid authorization code" in str(error)
        assert error.provider == "google"
        assert isinstance(error, IntegrationError)

    def test_includes_original_error_details(self):
        """Should include original error details."""
        error = OAuthError("hubspot", "Token exchange failed", "invalid_grant")
        assert error.original_error == "invalid_grant"


class TestTokenNotFoundError:
    """Tests for TokenNotFoundError class."""

    def test_creates_token_not_found_error(self):
        """Should create token not found error."""
        error = TokenNotFoundError("google", "user-123")
        assert "google" in str(error)
        assert "user-123" in str(error)
        assert error.provider == "google"
        assert error.user_id == "user-123"
        assert isinstance(error, IntegrationError)


class TestTokenExpiredError:
    """Tests for TokenExpiredError class."""

    def test_creates_token_expired_error(self):
        """Should create token expired error."""
        error = TokenExpiredError("google", "user-123")
        assert "google" in str(error)
        assert "user-123" in str(error)
        assert "expired" in str(error).lower()
        assert error.provider == "google"
        assert error.user_id == "user-123"
        assert isinstance(error, IntegrationError)


class TestTokenRefreshError:
    """Tests for TokenRefreshError class."""

    def test_creates_token_refresh_error(self):
        """Should create token refresh error."""
        error = TokenRefreshError("hubspot", "Refresh token revoked")
        assert "hubspot" in str(error)
        assert "Refresh token revoked" in str(error)
        assert error.provider == "hubspot"
        assert isinstance(error, IntegrationError)


class TestProviderAPIError:
    """Tests for ProviderAPIError class."""

    def test_creates_provider_api_error_with_status(self):
        """Should create provider API error with status."""
        error = ProviderAPIError("google", 403, "Forbidden")
        assert "google" in str(error)
        assert "403" in str(error)
        assert "Forbidden" in str(error)
        assert error.provider == "google"
        assert error.status_code == 403
        assert isinstance(error, IntegrationError)

    def test_includes_response_body_if_provided(self):
        """Should include response body if provided."""
        error = ProviderAPIError("hubspot", 400, "Bad Request", '{"error": "invalid_property"}')
        assert error.response_body == '{"error": "invalid_property"}'


class TestErrorInheritance:
    """Tests for error inheritance hierarchy."""

    def test_all_errors_inherit_from_integration_error(self):
        """All errors should inherit from IntegrationError."""
        errors = [
            TokenNotFoundError("google", "user-1"),
            TokenExpiredError("google", "user-1"),
            TokenRefreshError("google", "reason"),
            ProviderAPIError("google", 500, "error"),
            OAuthError("google", "error"),
        ]

        for error in errors:
            assert isinstance(error, IntegrationError)
            assert isinstance(error, Exception)

    def test_can_catch_specific_error_types(self):
        """Should be able to catch specific error types."""
        error = TokenNotFoundError("google", "user-1")

        assert isinstance(error, TokenNotFoundError)
        assert not isinstance(error, TokenExpiredError)
        assert not isinstance(error, ProviderAPIError)

    def test_can_catch_by_base_class(self):
        """Should be able to catch all by base class."""
        try:
            raise TokenNotFoundError("google", "user-1")
        except IntegrationError as e:
            assert e.provider == "google"
            assert e.user_id == "user-1"
