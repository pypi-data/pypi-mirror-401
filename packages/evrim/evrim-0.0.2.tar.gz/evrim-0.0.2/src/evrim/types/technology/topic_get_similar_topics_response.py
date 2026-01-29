# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from ..._models import BaseModel

__all__ = ["TopicGetSimilarTopicsResponse", "TopicGetSimilarTopicsResponseItem"]


class TopicGetSimilarTopicsResponseItem(BaseModel):
    """Related topic with similarity score via subarea matching"""

    similarity: float

    source_subarea: str

    target_subarea: str

    topic_id: str

    topic_name: str


TopicGetSimilarTopicsResponse: TypeAlias = List[TopicGetSimilarTopicsResponseItem]
