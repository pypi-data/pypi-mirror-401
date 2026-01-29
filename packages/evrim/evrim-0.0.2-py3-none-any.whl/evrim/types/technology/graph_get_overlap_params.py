# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["GraphGetOverlapParams"]


class GraphGetOverlapParams(TypedDict, total=False):
    community_id1: Required[str]
    """First community UUID"""

    community_id2: Required[str]
    """Second community UUID"""
