# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .location import Location
from .source_snippet import SourceSnippet
from .participant_snippet import ParticipantSnippet
from .organization_snippet import OrganizationSnippet

__all__ = ["MeetingDetails"]


class MeetingDetails(BaseModel):
    id: Optional[str] = None

    created_at: Optional[str] = None

    locations: Optional[List[Location]] = None

    organizations: Optional[List[OrganizationSnippet]] = None

    participants: Optional[List[ParticipantSnippet]] = None

    sources: Optional[List[SourceSnippet]] = None

    summary: Optional[str] = None

    topic: Optional[str] = None

    updated_at: Optional[str] = None
