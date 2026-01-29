# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["CommunityGetMeetingsParams"]


class CommunityGetMeetingsParams(TypedDict, total=False):
    full: bool
    """Return full meeting details (participants, organizations, locations, sources)"""

    limit: int
    """Maximum number of meetings"""

    min_similarity: float
    """Minimum similarity threshold"""

    offset: int
    """Pagination offset"""
