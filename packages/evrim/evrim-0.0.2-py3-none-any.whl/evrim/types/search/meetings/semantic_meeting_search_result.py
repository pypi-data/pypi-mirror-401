# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ...._models import BaseModel

__all__ = ["SemanticMeetingSearchResult"]


class SemanticMeetingSearchResult(BaseModel):
    """Meeting search result with similarity score"""

    similarity: float

    id: Optional[str] = None

    created_at: Optional[str] = None

    summary: Optional[str] = None

    topic: Optional[str] = None

    updated_at: Optional[str] = None
