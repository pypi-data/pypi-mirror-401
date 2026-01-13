# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["Secret"]


class Secret(BaseModel):
    created_at: datetime
    """Timestamp when the secret was created."""

    has_totp: bool
    """Whether the secret has a TOTP configured (only applicable for login type)."""

    name: str
    """Human-readable name for the secret."""

    secret_type: Literal["login", "string"]
    """Type of secret: 'login' or 'string'."""

    updated_at: datetime
    """Timestamp when the secret was last updated."""

    uuid: str
    """Unique identifier for the secret."""

    website: Optional[str] = None
    """Optional website URL."""
