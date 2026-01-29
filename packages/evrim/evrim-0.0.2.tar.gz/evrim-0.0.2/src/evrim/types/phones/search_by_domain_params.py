# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["SearchByDomainParams"]


class SearchByDomainParams(TypedDict, total=False):
    domain: Required[str]
    """Domain to search in source URLs (e.g., 'example.com')"""

    end: int
    """End index for pagination"""

    start: int
    """Start index for pagination"""
