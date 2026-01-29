# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["Admin1ListMeetingsParams"]


class Admin1ListMeetingsParams(TypedDict, total=False):
    admin1: Required[str]
    """Administrative division name (e.g., 'Beijing Municipality', 'California')"""

    end: int
    """End index for pagination"""

    start: int
    """Start index for pagination"""
