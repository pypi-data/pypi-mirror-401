# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import TypeAlias

from ..._models import BaseModel

__all__ = ["ParticipantSearchSemanticResponse", "ParticipantSearchSemanticResponseItem"]


class ParticipantSearchSemanticResponseItem(BaseModel):
    """Participant search result with similarity score"""

    similarity: float

    id: Optional[str] = None

    affiliation_types: Optional[List[Optional[str]]] = None

    affiliations: Optional[List[Optional[str]]] = None

    countries: Optional[List[Optional[str]]] = None

    created_at: Optional[str] = None

    meeting_count: Optional[int] = None

    name_english: Optional[str] = None

    names: Optional[List[Optional[str]]] = None

    roles: Optional[List[Optional[str]]] = None

    roles_english: Optional[List[Optional[str]]] = None

    updated_at: Optional[str] = None


ParticipantSearchSemanticResponse: TypeAlias = List[ParticipantSearchSemanticResponseItem]
