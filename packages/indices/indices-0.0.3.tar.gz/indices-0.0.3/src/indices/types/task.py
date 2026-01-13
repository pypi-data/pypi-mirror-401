# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["Task", "CreationSecret", "FailureInfo", "RequiredSecret"]


class CreationSecret(BaseModel):
    """A secret provided during task creation"""

    secret_uuid: str
    """UUID of the secret to bind."""

    description: Optional[str] = None
    """
    Optional description of what this secret is used for (helps generate meaningful
    slot names).
    """


class FailureInfo(BaseModel):
    """Information about why a task failed, for user display."""

    category: str
    """Primary failure category"""

    message: str
    """Summary of the failure cause"""


class RequiredSecret(BaseModel):
    """Definition of a secret slot that a task requires."""

    name: str
    """
    Name of the secret slot (used as env var prefix, e.g., 'LOGIN' →
    LOGIN_USERNAME).
    """

    type: Literal["login", "string"]
    """Type of secret required: 'login' or 'string'."""

    requires_totp: Optional[bool] = None
    """Whether this login slot requires 2FA/TOTP. Only applicable for 'login' type."""


class Task(BaseModel):
    id: str
    """Unique identifier for the object."""

    created_at: datetime
    """Timestamp when the object was created."""

    current_state: Literal["not_ready", "waiting_for_manual_completion", "ready", "failed"]
    """Current state of the task, in particular whether it is ready to use."""

    display_name: str
    """Short title shown in the dashboard. Informational only."""

    input_schema: str
    """Task input parameters in the form of a JSON schema."""

    output_schema: str
    """Task output in the form of a JSON schema."""

    task: str
    """Detailed explanation of the task to be performed."""

    updated_at: datetime
    """Timestamp when the object was last updated."""

    website: str
    """The website to perform the task on."""

    creation_secrets: Optional[List[CreationSecret]] = None
    """List of secrets provided during task creation."""

    failure_info: Optional[FailureInfo] = None
    """Information about why a task failed, for user display."""

    required_secrets: Optional[List[RequiredSecret]] = None
    """List of secrets that must be provided when running this task."""

    secret_bindings: Optional[Dict[str, str]] = None
    """
    Mapping of required secret slot names to secret UUIDs bound during task
    creation.
    """
