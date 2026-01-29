# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import TypeAlias

from ..._models import BaseModel

__all__ = ["DocumentSearchMarkdownResponse", "DocumentSearchMarkdownResponseItem"]


class DocumentSearchMarkdownResponseItem(BaseModel):
    markdown: Optional[str] = None

    snippet: Optional[str] = None

    url: Optional[str] = None


DocumentSearchMarkdownResponse: TypeAlias = List[DocumentSearchMarkdownResponseItem]
