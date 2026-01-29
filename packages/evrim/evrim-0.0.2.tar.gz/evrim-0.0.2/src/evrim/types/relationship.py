# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["Relationship"]


class Relationship(BaseModel):
    id: Optional[str] = None

    created_at: Optional[str] = None

    from_participant_id: Optional[str] = None

    meeting_id: Optional[str] = None

    purpose: Optional[str] = None

    relationship_type: Optional[str] = None

    to_participant_id: Optional[str] = None
