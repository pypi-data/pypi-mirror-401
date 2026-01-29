# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from ..sort_order import SortOrder
from .publication_sort_field import PublicationSortField

__all__ = ["PublicationSearchParams"]


class PublicationSearchParams(TypedDict, total=False):
    q: Required[str]
    """Search query"""

    limit: int
    """Maximum number of results"""

    offset: int
    """Pagination offset"""

    sort_by: Optional[PublicationSortField]
    """Fields available for sorting technology publications"""

    sort_order: SortOrder
    """Sort order"""

    year_max: Optional[int]
    """Maximum publication year"""

    year_min: Optional[int]
    """Minimum publication year"""
