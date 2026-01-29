# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from ..sort_order import SortOrder
from .community_sort_field import CommunitySortField

__all__ = ["CommunitySearchParams"]


class CommunitySearchParams(TypedDict, total=False):
    q: Required[str]
    """Search query"""

    limit: int
    """Maximum number of results"""

    offset: int
    """Pagination offset"""

    sort_by: Optional[CommunitySortField]
    """Fields available for sorting technology communities"""

    sort_order: SortOrder
    """Sort order"""
