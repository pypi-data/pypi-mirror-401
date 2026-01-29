# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from ..._models import BaseModel

__all__ = ["GraphGetSubgraphResponse"]


class GraphGetSubgraphResponse(BaseModel):
    """Subgraph around communities"""

    edges: Optional[List[Dict[str, object]]] = None

    nodes: Optional[List[Dict[str, object]]] = None

    stats: Optional[Dict[str, object]] = None
