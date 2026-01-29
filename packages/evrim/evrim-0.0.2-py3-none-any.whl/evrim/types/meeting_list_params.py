# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

from .sort_order import SortOrder
from .meeting_sort_field import MeetingSortField

__all__ = ["MeetingListParams"]


class MeetingListParams(TypedDict, total=False):
    end: int
    """End index for pagination"""

    full: bool
    """Whether to include related organizations, participants, and location"""

    sort_by: Optional[MeetingSortField]
    """Fields available for sorting meetings"""

    sort_order: SortOrder
    """Sort order"""

    start: int
    """Start index for pagination"""
