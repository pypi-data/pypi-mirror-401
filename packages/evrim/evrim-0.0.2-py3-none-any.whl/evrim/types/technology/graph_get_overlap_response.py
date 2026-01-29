# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from ..._models import BaseModel

__all__ = ["GraphGetOverlapResponse"]


class GraphGetOverlapResponse(BaseModel):
    """Overlap analysis between two communities"""

    community1_id: str

    community2_id: str

    overlap_score: float

    shared_topics_count: int

    unique_topics_1: int

    unique_topics_2: int

    shared_topics: Optional[List[Dict[str, object]]] = None
