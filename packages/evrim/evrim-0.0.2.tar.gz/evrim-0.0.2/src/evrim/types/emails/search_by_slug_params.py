# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["SearchBySlugParams"]


class SearchBySlugParams(TypedDict, total=False):
    slug: Required[str]
    """Username/slug to search (e.g., 'john')"""

    end: int
    """End index for pagination"""

    start: int
    """Start index for pagination"""
