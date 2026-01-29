# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

from ..sort_order import SortOrder

__all__ = ["PublicationGetTopicsParams"]


class PublicationGetTopicsParams(TypedDict, total=False):
    limit: int
    """Maximum results"""

    min_similarity: float
    """Minimum similarity score (0-1)"""

    offset: int
    """Pagination offset"""

    sort_by: str
    """Sort field: similarity or name"""

    sort_order: SortOrder
    """Sort order"""
