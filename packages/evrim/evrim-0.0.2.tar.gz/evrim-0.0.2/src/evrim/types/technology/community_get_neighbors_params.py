# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

from ..sort_order import SortOrder

__all__ = ["CommunityGetNeighborsParams"]


class CommunityGetNeighborsParams(TypedDict, total=False):
    direction: str
    """Edge direction: 'incoming', 'outgoing', 'both'"""

    limit: int
    """Maximum number of neighbors"""

    min_strength: float
    """Minimum composite score threshold"""

    sort_order: SortOrder
    """Sort order by composite score"""
