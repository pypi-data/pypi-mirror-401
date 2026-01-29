# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["MeetingGetCommunitiesParams"]


class MeetingGetCommunitiesParams(TypedDict, total=False):
    limit: int
    """Maximum number of communities"""

    min_similarity: float
    """Minimum similarity threshold"""

    novelty_filter: Optional[str]
    """Filter by novelty score: High, Medium, Low"""
