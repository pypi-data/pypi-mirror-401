# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

from .sort_order import SortOrder
from .organization_sort_field import OrganizationSortField

__all__ = ["OrganizationListParams"]


class OrganizationListParams(TypedDict, total=False):
    end: int
    """End index for pagination"""

    sort_by: Optional[OrganizationSortField]
    """Fields available for sorting organizations"""

    sort_order: SortOrder
    """Sort order"""

    start: int
    """Start index for pagination"""
