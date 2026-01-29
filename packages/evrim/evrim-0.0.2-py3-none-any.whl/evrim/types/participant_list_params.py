# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

from .sort_order import SortOrder
from .participant_sort_field import ParticipantSortField

__all__ = ["ParticipantListParams"]


class ParticipantListParams(TypedDict, total=False):
    end: int
    """End index for pagination"""

    sort_by: Optional[ParticipantSortField]
    """Fields available for sorting participants"""

    sort_order: SortOrder
    """Sort order"""

    start: int
    """Start index for pagination"""
