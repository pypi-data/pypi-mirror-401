# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal, TypeAlias

from ..._models import BaseModel

__all__ = ["CommunityGetNeighborsResponse", "CommunityGetNeighborsResponseItem"]


class CommunityGetNeighborsResponseItem(BaseModel):
    """Community neighbor with relationship information"""

    direction: str

    edge_count: int

    neighbor_community_uuid: str

    avg_weight: Optional[float] = None

    composite_score: Optional[float] = None

    max_weight: Optional[float] = None

    neighbor_novelty_score: Optional[Literal["High", "Medium", "Low"]] = None

    neighbor_summary: Optional[str] = None


CommunityGetNeighborsResponse: TypeAlias = List[CommunityGetNeighborsResponseItem]
