# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["Document"]


class Document(BaseModel):
    markdown: Optional[str] = None

    url: Optional[str] = None
