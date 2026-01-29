# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["Location"]


class Location(BaseModel):
    id: Optional[str] = None

    admin1: Optional[str] = None

    country: Optional[str] = None

    created_at: Optional[str] = None

    lat: Optional[float] = None

    lon: Optional[float] = None

    name: Optional[str] = None
