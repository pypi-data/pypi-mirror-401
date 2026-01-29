# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from ..._models import BaseModel

__all__ = ["GraphFindPathResponse"]


class GraphFindPathResponse(BaseModel):
    """Path between two communities"""

    path_communities: List[str]

    path_length: int

    total_weight: float

    path_details: Optional[List[Dict[str, object]]] = None
