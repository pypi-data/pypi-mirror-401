# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable, Optional
from typing_extensions import Required, TypedDict

__all__ = ["TaskCreateParams", "CreationParams", "CreationParamsSecret"]


class TaskCreateParams(TypedDict, total=False):
    creation_params: Required[CreationParams]
    """Information used during task creation."""

    display_name: Required[str]
    """Short title shown in the dashboard.

    Informational only; not used to generate the task.
    """

    input_schema: Required[str]
    """Task input parameters in the form of a JSON schema."""

    output_schema: Required[str]
    """Task output in the form of a JSON schema."""

    task: Required[str]
    """Detailed explanation of the task to be performed."""

    website: Required[str]
    """The website to perform the task on."""


class CreationParamsSecret(TypedDict, total=False):
    """A secret provided during task creation"""

    secret_uuid: Required[str]
    """UUID of the secret to bind."""

    description: Optional[str]
    """
    Optional description of what this secret is used for (helps generate meaningful
    slot names).
    """


class CreationParams(TypedDict, total=False):
    """Information used during task creation."""

    initial_input_values: Dict[str, object]
    """Initial values for input schema fields, keyed by property name.

    Used during task creation to demonstrate the task. Especially important for
    tasks requiring authentication, as initial credentials must be provided.
    """

    is_fully_autonomous: bool
    """If true, the server will run the browser task autonomously.

    If false, the user must complete the task manually in a spawned browser.
    """

    secrets: Iterable[CreationParamsSecret]
    """List of secrets to use for this task."""
