# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from ..._models import BaseModel

__all__ = ["AnalyticsGetCommunityStatsResponse"]


class AnalyticsGetCommunityStatsResponse(BaseModel):
    """Statistics for a specific technology community"""

    avg_publication_year: float

    community_uuid: str

    num_publications: int

    num_topics: int

    publication_year_range: List[int]

    topic_diversity: float

    total_connections: int

    avg_edge_strength: Optional[float] = None

    top_organizations: Optional[List[Dict[str, object]]] = None
