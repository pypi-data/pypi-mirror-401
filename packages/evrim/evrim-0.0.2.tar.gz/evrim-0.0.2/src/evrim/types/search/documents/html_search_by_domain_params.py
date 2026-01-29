# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["HTMLSearchByDomainParams"]


class HTMLSearchByDomainParams(TypedDict, total=False):
    domain: Required[str]
    """Domain to search for"""

    end: int
    """End index for pagination"""

    start: int
    """Start index for pagination"""
