# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["SecretCreateParams"]


class SecretCreateParams(TypedDict, total=False):
    name: Required[str]
    """Human-readable name for the secret."""

    secret_type: Required[Literal["login", "string"]]
    """Type of secret: 'login' for credentials, 'string' for simple values."""

    password: Optional[str]
    """Login password. Required for 'login' type."""

    totp_secret: Optional[str]
    """Optional TOTP secret (base32 encoded). Only for 'login' type."""

    username: Optional[str]
    """Login username. Required for 'login' type."""

    value: Optional[str]
    """Secret value. Required for 'string' type."""

    website: Optional[str]
    """Optional website URL for context."""
