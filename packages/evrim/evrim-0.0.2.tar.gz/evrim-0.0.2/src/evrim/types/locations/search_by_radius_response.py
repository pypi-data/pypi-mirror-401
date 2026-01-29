# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import TypeAlias

from ..._models import BaseModel
from ..location import Location
from ..source_snippet import SourceSnippet
from ..participant_snippet import ParticipantSnippet
from ..organization_snippet import OrganizationSnippet

__all__ = ["SearchByRadiusResponse", "SearchByRadiusResponseItem"]


class SearchByRadiusResponseItem(BaseModel):
    """Meeting details with distance from search point (for radius searches)"""

    id: Optional[str] = None

    created_at: Optional[str] = None

    distance_km: Optional[float] = None
    """Distance in kilometers from the search point"""

    locations: Optional[List[Location]] = None

    organizations: Optional[List[OrganizationSnippet]] = None

    participants: Optional[List[ParticipantSnippet]] = None

    sources: Optional[List[SourceSnippet]] = None

    summary: Optional[str] = None

    topic: Optional[str] = None

    updated_at: Optional[str] = None


SearchByRadiusResponse: TypeAlias = List[SearchByRadiusResponseItem]
