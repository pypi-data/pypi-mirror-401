# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel

__all__ = ["Douyin"]


class Douyin(BaseModel):
    id: Optional[str] = None

    created_at: Optional[str] = None

    douyin_link: Optional[str] = None

    updated_at: Optional[str] = None

    urls: Optional[List[Optional[str]]] = None
