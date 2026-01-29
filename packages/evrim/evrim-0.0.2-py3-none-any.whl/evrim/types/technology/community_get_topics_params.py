# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

from ..sort_order import SortOrder
from .topic_sort_field import TopicSortField

__all__ = ["CommunityGetTopicsParams"]


class CommunityGetTopicsParams(TypedDict, total=False):
    limit: int
    """Maximum number of topics"""

    offset: int
    """Pagination offset"""

    sort_by: Optional[TopicSortField]
    """Fields available for sorting technology topics"""

    sort_order: SortOrder
    """Sort order"""
