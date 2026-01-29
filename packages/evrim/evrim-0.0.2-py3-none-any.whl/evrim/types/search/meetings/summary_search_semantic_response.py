# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .semantic_meeting_search_result import SemanticMeetingSearchResult

__all__ = ["SummarySearchSemanticResponse"]

SummarySearchSemanticResponse: TypeAlias = List[SemanticMeetingSearchResult]
