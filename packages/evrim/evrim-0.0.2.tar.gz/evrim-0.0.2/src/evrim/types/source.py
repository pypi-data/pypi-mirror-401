# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["Source"]


class Source(BaseModel):
    id: Optional[str] = None

    created_at: Optional[str] = None

    date_published: Optional[str] = None

    updated_at: Optional[str] = None

    url: Optional[str] = None
