# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import TypeAlias

from ..._models import BaseModel

__all__ = ["OrganizationSearchSemanticResponse", "OrganizationSearchSemanticResponseItem"]


class OrganizationSearchSemanticResponseItem(BaseModel):
    """Organization search result with similarity score"""

    similarity: float

    id: Optional[str] = None

    countries: Optional[List[Optional[str]]] = None

    created_at: Optional[str] = None

    meeting_count: Optional[int] = None

    name_english: Optional[str] = None

    names: Optional[List[Optional[str]]] = None

    types: Optional[List[Optional[str]]] = None

    updated_at: Optional[str] = None


OrganizationSearchSemanticResponse: TypeAlias = List[OrganizationSearchSemanticResponseItem]
