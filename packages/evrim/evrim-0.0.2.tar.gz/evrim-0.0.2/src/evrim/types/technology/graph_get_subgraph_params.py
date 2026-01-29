# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from ..._types import SequenceNotStr

__all__ = ["GraphGetSubgraphParams"]


class GraphGetSubgraphParams(TypedDict, total=False):
    community_ids: Required[SequenceNotStr[str]]
    """Community UUIDs to center subgraph around"""

    depth: int
    """Neighborhood depth"""

    min_edge_strength: float
    """Minimum edge composite score"""
