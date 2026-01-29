# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["SearchQueryParams"]


class SearchQueryParams(TypedDict, total=False):
    query: Required[str]
    """Phone number to search for"""

    end: int
    """End index for pagination"""

    start: int
    """Start index for pagination"""
