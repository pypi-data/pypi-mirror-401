# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["SearchByBboxParams"]


class SearchByBboxParams(TypedDict, total=False):
    max_lat: Required[float]
    """Maximum latitude of bounding box"""

    max_lon: Required[float]
    """Maximum longitude of bounding box"""

    min_lat: Required[float]
    """Minimum latitude of bounding box"""

    min_lon: Required[float]
    """Minimum longitude of bounding box"""

    end: int
    """End index for pagination"""

    start: int
    """Start index for pagination"""
