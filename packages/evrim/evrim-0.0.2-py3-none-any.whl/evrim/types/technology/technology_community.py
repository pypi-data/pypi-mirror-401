# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["TechnologyCommunity"]


class TechnologyCommunity(BaseModel):
    """Technology research community"""

    community_uuid: str

    created_at: Optional[str] = None

    novelty_assessment: Optional[str] = None

    novelty_score: Optional[Literal["High", "Medium", "Low"]] = None

    summary: Optional[str] = None

    updated_at: Optional[str] = None
