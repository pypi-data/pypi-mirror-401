# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from typing_extensions import TypeAlias

from ..._models import BaseModel

__all__ = ["CommunityGetPublicationsResponse", "CommunityGetPublicationsResponseItem"]


class CommunityGetPublicationsResponseItem(BaseModel):
    """Publication with matched topics"""

    id: str

    title: str

    abstract: Optional[str] = None

    authors: Optional[List[str]] = None

    journal: Optional[str] = None

    matched_topics: Optional[List[Dict[str, object]]] = None

    year: Optional[int] = None


CommunityGetPublicationsResponse: TypeAlias = List[CommunityGetPublicationsResponseItem]
