# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

from ..sort_order import SortOrder

__all__ = ["TopicGetPublicationsParams"]


class TopicGetPublicationsParams(TypedDict, total=False):
    limit: int
    """Maximum results"""

    min_similarity: float
    """Minimum similarity score (0-1)"""

    offset: int
    """Pagination offset"""

    sort_by: str
    """Sort field: similarity, year, or title"""

    sort_order: SortOrder
    """Sort order"""

    year_max: Optional[int]
    """Maximum publication year"""

    year_min: Optional[int]
    """Minimum publication year"""
