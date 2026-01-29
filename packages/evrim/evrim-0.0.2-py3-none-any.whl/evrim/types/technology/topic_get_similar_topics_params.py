# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["TopicGetSimilarTopicsParams"]


class TopicGetSimilarTopicsParams(TypedDict, total=False):
    limit: int
    """Maximum number of similar topics"""

    min_similarity: float
    """Minimum similarity score"""
