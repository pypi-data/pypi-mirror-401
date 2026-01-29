# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .meeting_details import MeetingDetails

__all__ = ["ParticipantListMeetingsResponse"]

ParticipantListMeetingsResponse: TypeAlias = List[MeetingDetails]
