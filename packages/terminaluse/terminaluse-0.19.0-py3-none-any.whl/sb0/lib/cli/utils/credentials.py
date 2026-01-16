"""Credential storage utilities for CLI authentication.

Manages persistent storage of authentication tokens at ~/.sb0/credentials.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

# Default credentials location
CREDENTIALS_DIR = Path.home() / ".sb0"
CREDENTIALS_FILE = CREDENTIALS_DIR / "credentials.json"


@dataclass
class StoredCredentials:
    """Stored authentication credentials."""

    token: str
    user_id: str | None = None
    email: str | None = None
    expires_at: datetime | None = None
    created_at: datetime | None = None


def get_credentials_path() -> Path:
    """Get the path to the credentials file.

    Can be overridden via SB0_CREDENTIALS_FILE environment variable.
    """
    env_path = os.environ.get("SB0_CREDENTIALS_FILE")
    if env_path:
        return Path(env_path)
    return CREDENTIALS_FILE


def get_stored_token() -> str | None:
    """Read auth token from credentials file.

    Returns:
        The stored token string, or None if not found/invalid
    """
    credentials = get_stored_credentials()
    if credentials:
        return credentials.token
    return None


def get_stored_credentials() -> StoredCredentials | None:
    """Read full credentials from storage.

    Returns:
        StoredCredentials object, or None if not found/invalid
    """
    creds_file = get_credentials_path()

    if not creds_file.exists():
        return None

    try:
        data = json.loads(creds_file.read_text())

        # Parse optional datetime fields
        expires_at = None
        if data.get("expires_at"):
            expires_at = datetime.fromisoformat(data["expires_at"])

        created_at = None
        if data.get("created_at"):
            created_at = datetime.fromisoformat(data["created_at"])

        return StoredCredentials(
            token=data["token"],
            user_id=data.get("user_id"),
            email=data.get("email"),
            expires_at=expires_at,
            created_at=created_at,
        )
    except (json.JSONDecodeError, KeyError, ValueError):
        return None


def store_credentials(
    token: str,
    user_id: str | None = None,
    email: str | None = None,
    expires_at: datetime | None = None,
) -> None:
    """Store authentication credentials.

    Args:
        token: The authentication token
        user_id: Optional user ID
        email: Optional user email
        expires_at: Optional token expiration time
    """
    creds_dir = get_credentials_path().parent
    creds_file = get_credentials_path()

    # Create directory if needed
    creds_dir.mkdir(parents=True, exist_ok=True)

    # Build credentials data
    data: dict[str, Any] = {
        "token": token,
        "created_at": datetime.now().isoformat(),
    }

    if user_id:
        data["user_id"] = user_id
    if email:
        data["email"] = email
    if expires_at:
        data["expires_at"] = expires_at.isoformat()

    # Write credentials with secure permissions
    creds_file.write_text(json.dumps(data, indent=2))

    # Set restrictive permissions (owner read/write only)
    try:
        creds_file.chmod(0o600)
    except OSError:
        # Windows doesn't support chmod the same way, ignore
        pass


def store_token(token: str) -> None:
    """Store just an auth token (simple interface).

    Args:
        token: The authentication token to store
    """
    store_credentials(token=token)


def clear_credentials() -> None:
    """Remove stored credentials."""
    creds_file = get_credentials_path()
    if creds_file.exists():
        creds_file.unlink()


def is_authenticated() -> bool:
    """Check if valid credentials are stored.

    Returns:
        True if credentials exist and haven't expired
    """
    credentials = get_stored_credentials()
    if not credentials:
        return False

    # Check expiration if set
    if credentials.expires_at:
        if datetime.now() >= credentials.expires_at:
            return False

    return True


def get_credentials_info() -> dict[str, Any] | None:
    """Get credential info for display (without exposing full token).

    Returns:
        Dict with masked token and metadata, or None if not authenticated
    """
    credentials = get_stored_credentials()
    if not credentials:
        return None

    # Mask the token for display
    token = credentials.token
    if len(token) > 8:
        masked_token = f"{token[:4]}...{token[-4:]}"
    else:
        masked_token = "****"

    return {
        "token": masked_token,
        "user_id": credentials.user_id,
        "email": credentials.email,
        "expires_at": credentials.expires_at.isoformat() if credentials.expires_at else None,
        "created_at": credentials.created_at.isoformat() if credentials.created_at else None,
    }
