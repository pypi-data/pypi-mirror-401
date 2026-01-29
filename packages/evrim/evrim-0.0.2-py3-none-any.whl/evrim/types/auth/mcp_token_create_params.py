# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["McpTokenCreateParams"]


class McpTokenCreateParams(TypedDict, total=False):
    name: Required[str]
    """User-friendly name for the token"""

    expiry_days: int
    """Number of days until token expires"""
