# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel

__all__ = ["TechnologyPublication"]


class TechnologyPublication(BaseModel):
    """Technology publication"""

    id: str

    title: str

    abstract: Optional[str] = None

    authors: Optional[List[str]] = None

    created_at: Optional[str] = None

    journal: Optional[str] = None

    updated_at: Optional[str] = None

    year: Optional[int] = None
