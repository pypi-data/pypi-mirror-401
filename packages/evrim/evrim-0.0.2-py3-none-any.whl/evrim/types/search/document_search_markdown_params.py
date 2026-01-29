# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["DocumentSearchMarkdownParams"]


class DocumentSearchMarkdownParams(TypedDict, total=False):
    q: Required[str]
    """Search query string"""

    limit: int
    """Maximum number of results"""

    offset: int
    """Offset for pagination"""
