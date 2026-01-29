# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["HTMLDocument"]


class HTMLDocument(BaseModel):
    """HTML document model with content size validation"""

    content: Optional[str] = None

    created_at: Optional[str] = None

    updated_at: Optional[str] = None

    url: Optional[str] = None
