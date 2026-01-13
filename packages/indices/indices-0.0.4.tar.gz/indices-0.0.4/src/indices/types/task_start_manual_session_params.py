# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Required, TypedDict

__all__ = ["TaskStartManualSessionParams", "Cookie"]


class TaskStartManualSessionParams(TypedDict, total=False):
    cookies: Iterable[Cookie]
    """Initial cookies to set in the browser session."""

    use_proxy: bool
    """If true, spawn the browser session using a proxy."""


class Cookie(TypedDict, total=False):
    """A cookie to set in the browser session."""

    name: Required[str]
    """The name of the cookie."""

    value: Required[str]
    """The value of the cookie."""

    domain: Optional[str]
    """The domain of the cookie."""

    http_only: Optional[bool]
    """Whether the cookie is HTTP only."""

    path: Optional[str]
    """The path of the cookie."""

    secure: Optional[bool]
    """Whether the cookie is secure."""
