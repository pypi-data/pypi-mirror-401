# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["SearchByRadiusParams"]


class SearchByRadiusParams(TypedDict, total=False):
    lat: Required[float]
    """Latitude of search center"""

    lon: Required[float]
    """Longitude of search center"""

    radius: Required[float]
    """Search radius in kilometers (max 20,000 km)"""

    end: int
    """End index for pagination"""

    start: int
    """Start index for pagination"""
