# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel

__all__ = ["TechnologyTopic"]


class TechnologyTopic(BaseModel):
    """Technology topic"""

    id: str

    name: str

    checkpoint_url: Optional[str] = None

    created_at: Optional[str] = None

    description: Optional[str] = None

    publication_count: Optional[int] = None

    sub_areas: Optional[List[str]] = None

    updated_at: Optional[str] = None
