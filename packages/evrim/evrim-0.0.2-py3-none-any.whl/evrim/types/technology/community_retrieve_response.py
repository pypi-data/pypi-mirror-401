# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["CommunityRetrieveResponse"]


class CommunityRetrieveResponse(BaseModel):
    """Detailed community information with topics and neighbors"""

    community_uuid: str

    created_at: Optional[str] = None

    incoming_neighbors: Optional[int] = None

    novelty_assessment: Optional[str] = None

    novelty_score: Optional[Literal["High", "Medium", "Low"]] = None

    num_topics: Optional[int] = None

    outgoing_neighbors: Optional[int] = None

    summary: Optional[str] = None

    topics: Optional[List[Dict[str, object]]] = None

    updated_at: Optional[str] = None
