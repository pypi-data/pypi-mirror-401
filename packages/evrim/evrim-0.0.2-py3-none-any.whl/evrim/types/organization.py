# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["Organization"]


class Organization(BaseModel):
    id: Optional[str] = None

    countries: Optional[List[Optional[str]]] = None

    created_at: Optional[str] = None

    meeting_count: Optional[int] = None

    name_english: Optional[str] = None

    names: Optional[List[Optional[str]]] = None

    types: Optional[List[Optional[str]]] = None

    updated_at: Optional[str] = None
