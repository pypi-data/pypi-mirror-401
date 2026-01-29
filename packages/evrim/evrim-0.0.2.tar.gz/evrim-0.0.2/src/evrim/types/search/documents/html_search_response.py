# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import TypeAlias

from ...._models import BaseModel

__all__ = ["HTMLSearchResponse", "HTMLSearchResponseItem"]


class HTMLSearchResponseItem(BaseModel):
    """HTML document search result with snippet and size validation"""

    content: Optional[str] = None

    created_at: Optional[str] = None

    snippet: Optional[str] = None

    updated_at: Optional[str] = None

    url: Optional[str] = None


HTMLSearchResponse: TypeAlias = List[HTMLSearchResponseItem]
