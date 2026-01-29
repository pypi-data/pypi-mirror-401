# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["SourceSnippet"]


class SourceSnippet(BaseModel):
    id: str

    date_published: Optional[str] = None

    url: Optional[str] = None
