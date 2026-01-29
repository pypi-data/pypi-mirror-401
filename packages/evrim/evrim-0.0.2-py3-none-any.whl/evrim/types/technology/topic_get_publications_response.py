# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import TypeAlias

from ..._models import BaseModel

__all__ = ["TopicGetPublicationsResponse", "TopicGetPublicationsResponseItem"]


class TopicGetPublicationsResponseItem(BaseModel):
    """Publication matched to a topic with similarity score"""

    matched_subarea: str

    publication_id: str

    similarity: float

    title: str

    abstract: Optional[str] = None

    authors: Optional[List[str]] = None

    journal: Optional[str] = None

    year: Optional[int] = None


TopicGetPublicationsResponse: TypeAlias = List[TopicGetPublicationsResponseItem]
