# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["HTMLSearchByURLParams"]


class HTMLSearchByURLParams(TypedDict, total=False):
    url: Required[str]
    """URL pattern to search for"""

    limit: int
    """Maximum number of results"""

    offset: int
    """Offset for pagination"""
