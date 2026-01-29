# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel

__all__ = ["Qq"]


class Qq(BaseModel):
    id: Optional[str] = None

    created_at: Optional[str] = None

    qq_link: Optional[str] = None

    updated_at: Optional[str] = None

    urls: Optional[List[Optional[str]]] = None
