# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["SecretGetTotpResponse"]


class SecretGetTotpResponse(BaseModel):
    code: str
    """Current 6-digit TOTP code."""

    uuid: str
    """Unique identifier of the secret."""
