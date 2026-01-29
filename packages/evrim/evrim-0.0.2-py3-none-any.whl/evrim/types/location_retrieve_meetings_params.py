# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["LocationRetrieveMeetingsParams"]


class LocationRetrieveMeetingsParams(TypedDict, total=False):
    end: int
    """End index for pagination"""

    full: bool
    """Whether to include related organizations, participants, and sources"""

    start: int
    """Start index for pagination"""
