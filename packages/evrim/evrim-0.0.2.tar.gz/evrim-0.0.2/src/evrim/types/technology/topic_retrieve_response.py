# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from ..._models import BaseModel

__all__ = ["TopicRetrieveResponse"]


class TopicRetrieveResponse(BaseModel):
    """Detailed topic information with communities and publications"""

    id: str

    name: str

    checkpoint_url: Optional[str] = None

    communities: Optional[List[Dict[str, object]]] = None

    created_at: Optional[str] = None

    description: Optional[str] = None

    publication_count: Optional[int] = None

    sub_areas: Optional[List[str]] = None

    updated_at: Optional[str] = None
