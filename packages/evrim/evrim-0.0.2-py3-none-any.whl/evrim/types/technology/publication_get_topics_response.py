# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import TypeAlias

from ..._models import BaseModel

__all__ = ["PublicationGetTopicsResponse", "PublicationGetTopicsResponseItem"]


class PublicationGetTopicsResponseItem(BaseModel):
    """Topic matched to a publication with similarity score"""

    matched_subarea: str

    similarity: float

    topic_id: str

    topic_name: str

    sub_areas: Optional[List[str]] = None

    topic_description: Optional[str] = None


PublicationGetTopicsResponse: TypeAlias = List[PublicationGetTopicsResponseItem]
