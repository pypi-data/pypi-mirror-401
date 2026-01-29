# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import TypeAlias

from ..._models import BaseModel

__all__ = ["DocumentSearchSemanticResponse", "DocumentSearchSemanticResponseItem"]


class DocumentSearchSemanticResponseItem(BaseModel):
    """Document search result with similarity score"""

    similarity: float

    markdown: Optional[str] = None

    url: Optional[str] = None


DocumentSearchSemanticResponse: TypeAlias = List[DocumentSearchSemanticResponseItem]
