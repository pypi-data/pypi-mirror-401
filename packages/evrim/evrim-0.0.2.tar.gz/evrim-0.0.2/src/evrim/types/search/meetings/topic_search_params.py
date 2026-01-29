# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from ...sort_order import SortOrder
from ...meeting_sort_field import MeetingSortField

__all__ = ["TopicSearchParams"]


class TopicSearchParams(TypedDict, total=False):
    q: Required[str]
    """Search query string"""

    limit: int
    """Maximum number of results"""

    offset: int
    """Offset for pagination"""

    sort_by: Optional[MeetingSortField]
    """Fields available for sorting meetings"""

    sort_order: SortOrder
    """Sort order"""
