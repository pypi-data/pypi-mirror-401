# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

from ..sort_order import SortOrder
from .community_sort_field import CommunitySortField

__all__ = ["CommunityListParams"]


class CommunityListParams(TypedDict, total=False):
    end: int
    """End index for pagination"""

    min_topics: Optional[int]
    """Minimum number of topics in community"""

    novelty_score: Optional[str]
    """Filter by novelty score: High, Medium, Low"""

    sort_by: Optional[CommunitySortField]
    """Fields available for sorting technology communities"""

    sort_order: SortOrder
    """Sort order"""

    start: int
    """Start index for pagination"""
