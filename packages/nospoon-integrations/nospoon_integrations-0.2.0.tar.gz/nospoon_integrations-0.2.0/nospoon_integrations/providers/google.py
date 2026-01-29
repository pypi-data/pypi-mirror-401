"""Google OAuth provider with Gmail API support."""

import base64
import json
from dataclasses import dataclass
from typing import Any, Optional

from nospoon_integrations.core.errors import ProviderAPIError
from nospoon_integrations.core.types import (
    ProviderConfig,
    ProviderEndpoints,
    TokenStorage,
)
from nospoon_integrations.providers.base_provider import BaseProvider

GOOGLE_ENDPOINTS = ProviderEndpoints(
    auth_url="https://accounts.google.com/o/oauth2/v2/auth",
    token_url="https://oauth2.googleapis.com/token",
    revoke_url="https://oauth2.googleapis.com/revoke",
    user_info_url="https://www.googleapis.com/oauth2/v2/userinfo",
)


@dataclass
class DraftEmailParams:
    """Parameters for creating a draft email."""

    to: str
    subject: str
    body: str
    cc: Optional[str] = None
    bcc: Optional[str] = None


@dataclass
class DraftEmailResult:
    """Result from creating a draft email."""

    id: str
    message_id: str
    thread_id: str


@dataclass
class GoogleUserInfo:
    """Google user info."""

    id: str
    email: str
    name: str
    picture: Optional[str] = None


class GoogleProvider(BaseProvider):
    """Google OAuth provider with Gmail API support."""

    def __init__(self, config: ProviderConfig, storage: TokenStorage) -> None:
        super().__init__("google", GOOGLE_ENDPOINTS, config, storage)

    def _get_token_request_headers(self) -> dict[str, str]:
        """Override to use JSON content type for Google."""
        return {"Content-Type": "application/json"}

    def _get_token_request_body(self, code: str, redirect_uri: str) -> str:
        """Override to use JSON body for Google."""
        return json.dumps(
            {
                "grant_type": "authorization_code",
                "client_id": self._config.client_id,
                "client_secret": self._config.client_secret,
                "code": code,
                "redirect_uri": redirect_uri,
            }
        )

    def _get_refresh_token_request_body(self, refresh_token: str) -> str:
        """Override to use JSON body for Google refresh."""
        return json.dumps(
            {
                "grant_type": "refresh_token",
                "client_id": self._config.client_id,
                "client_secret": self._config.client_secret,
                "refresh_token": refresh_token,
            }
        )

    def get_auth_url(
        self,
        redirect_uri: str,
        state: Optional[str] = None,
        additional_params: Optional[dict[str, str]] = None,
    ) -> str:
        """Override auth URL to include access_type=offline for refresh token."""
        params = additional_params or {}
        params.update(
            {
                "access_type": "offline",
                "prompt": "consent",
            }
        )
        return super().get_auth_url(redirect_uri, state, params)

    # Google-specific API methods

    async def create_draft_email(self, user_id: str, params: DraftEmailParams) -> DraftEmailResult:
        """
        Create a draft email in Gmail.

        Args:
            user_id: User ID
            params: Draft email parameters

        Returns:
            Draft email result
        """
        access_token = await self.get_valid_token(user_id)

        email_lines = [f"To: {params.to}"]
        if params.cc:
            email_lines.append(f"Cc: {params.cc}")
        if params.bcc:
            email_lines.append(f"Bcc: {params.bcc}")
        email_lines.extend(
            [
                f"Subject: {params.subject}",
                "Content-Type: text/html; charset=utf-8",
                "",
                params.body,
            ]
        )

        email_content = "\r\n".join(email_lines)
        encoded_email = self._base64_url_encode(email_content)

        response = await self._client.post(
            "https://gmail.googleapis.com/gmail/v1/users/me/drafts",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            json={"message": {"raw": encoded_email}},
        )

        if not response.is_success:
            raise ProviderAPIError(
                "google",
                response.status_code,
                "Failed to create draft email",
                response.text,
            )

        data: dict[str, Any] = response.json()
        return DraftEmailResult(
            id=data["id"],
            message_id=data["message"]["id"],
            thread_id=data["message"]["threadId"],
        )

    async def get_user_info(self, user_id: str) -> GoogleUserInfo:
        """
        Get user info from Google.

        Args:
            user_id: User ID

        Returns:
            Google user info
        """
        access_token = await self.get_valid_token(user_id)

        response = await self._client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        if not response.is_success:
            raise ProviderAPIError(
                "google",
                response.status_code,
                "Failed to get user info",
                response.text,
            )

        data: dict[str, Any] = response.json()
        return GoogleUserInfo(
            id=data["id"],
            email=data["email"],
            name=data["name"],
            picture=data.get("picture"),
        )

    @staticmethod
    def _base64_url_encode(data: str) -> str:
        """URL-safe base64 encoding for Gmail API."""
        encoded = base64.urlsafe_b64encode(data.encode("utf-8"))
        return encoded.decode("utf-8").rstrip("=")
