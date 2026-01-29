# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal, TypeAlias

from ..._models import BaseModel

__all__ = ["MeetingGetCommunitiesResponse", "MeetingGetCommunitiesResponseItem"]


class MeetingGetCommunitiesResponseItem(BaseModel):
    """Technology community linked to a meeting"""

    community_id: str

    similarity: float

    community_summary: Optional[str] = None

    novelty_score: Optional[Literal["High", "Medium", "Low"]] = None

    num_topics: Optional[int] = None

    sub_areas: Optional[str] = None


MeetingGetCommunitiesResponse: TypeAlias = List[MeetingGetCommunitiesResponseItem]
