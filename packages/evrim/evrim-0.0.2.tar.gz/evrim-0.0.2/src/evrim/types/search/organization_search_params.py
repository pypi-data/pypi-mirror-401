# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from ..sort_order import SortOrder
from ..organization_sort_field import OrganizationSortField

__all__ = ["OrganizationSearchParams"]


class OrganizationSearchParams(TypedDict, total=False):
    q: Required[str]
    """Search query string"""

    limit: int
    """Maximum number of results"""

    offset: int
    """Offset for pagination"""

    sort_by: Optional[OrganizationSortField]
    """Fields available for sorting organizations"""

    sort_order: SortOrder
    """Sort order"""
