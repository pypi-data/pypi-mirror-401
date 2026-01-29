# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.technology import meeting_get_communities_params
from ...types.technology.meeting_get_communities_response import MeetingGetCommunitiesResponse

__all__ = ["MeetingsResource", "AsyncMeetingsResource"]


class MeetingsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> MeetingsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return MeetingsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MeetingsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return MeetingsResourceWithStreamingResponse(self)

    def get_communities(
        self,
        meeting_id: str,
        *,
        limit: int | Omit = omit,
        min_similarity: float | Omit = omit,
        novelty_filter: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MeetingGetCommunitiesResponse:
        """
        Get technology communities linked to a specific meeting via semantic similarity.

        **Path Parameters:**

        - `meeting_id`: UUID of the meeting

        **Query Parameters:**

        - `limit`: Maximum number of communities to return (1-100, default: 10)
        - `min_similarity`: Minimum similarity threshold (0.0-1.0, default: 0.5)
        - `novelty_filter`: Optional filter by community novelty score

        **Community Fields:**

        - community_id (UUID): Community identifier
        - community_summary: Summary of the community
        - novelty_score: High/Medium/Low novelty assessment
        - num_topics: Number of topics in the community
        - similarity: Semantic similarity score (0.0-1.0)
        - sub_areas: Community topic areas

        **Sorting:** Results are sorted by similarity descending (highest similarity
        first)

        **Response Codes:**

        - 200: Success
        - 404: Meeting not found
        - 401: Unauthorized
        - 422: Invalid parameters

        Args:
          limit: Maximum number of communities

          min_similarity: Minimum similarity threshold

          novelty_filter: Filter by novelty score: High, Medium, Low

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not meeting_id:
            raise ValueError(f"Expected a non-empty value for `meeting_id` but received {meeting_id!r}")
        return self._get(
            f"/technology/meetings/{meeting_id}/communities",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "min_similarity": min_similarity,
                        "novelty_filter": novelty_filter,
                    },
                    meeting_get_communities_params.MeetingGetCommunitiesParams,
                ),
            ),
            cast_to=MeetingGetCommunitiesResponse,
        )


class AsyncMeetingsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMeetingsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return AsyncMeetingsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMeetingsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return AsyncMeetingsResourceWithStreamingResponse(self)

    async def get_communities(
        self,
        meeting_id: str,
        *,
        limit: int | Omit = omit,
        min_similarity: float | Omit = omit,
        novelty_filter: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MeetingGetCommunitiesResponse:
        """
        Get technology communities linked to a specific meeting via semantic similarity.

        **Path Parameters:**

        - `meeting_id`: UUID of the meeting

        **Query Parameters:**

        - `limit`: Maximum number of communities to return (1-100, default: 10)
        - `min_similarity`: Minimum similarity threshold (0.0-1.0, default: 0.5)
        - `novelty_filter`: Optional filter by community novelty score

        **Community Fields:**

        - community_id (UUID): Community identifier
        - community_summary: Summary of the community
        - novelty_score: High/Medium/Low novelty assessment
        - num_topics: Number of topics in the community
        - similarity: Semantic similarity score (0.0-1.0)
        - sub_areas: Community topic areas

        **Sorting:** Results are sorted by similarity descending (highest similarity
        first)

        **Response Codes:**

        - 200: Success
        - 404: Meeting not found
        - 401: Unauthorized
        - 422: Invalid parameters

        Args:
          limit: Maximum number of communities

          min_similarity: Minimum similarity threshold

          novelty_filter: Filter by novelty score: High, Medium, Low

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not meeting_id:
            raise ValueError(f"Expected a non-empty value for `meeting_id` but received {meeting_id!r}")
        return await self._get(
            f"/technology/meetings/{meeting_id}/communities",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "min_similarity": min_similarity,
                        "novelty_filter": novelty_filter,
                    },
                    meeting_get_communities_params.MeetingGetCommunitiesParams,
                ),
            ),
            cast_to=MeetingGetCommunitiesResponse,
        )


class MeetingsResourceWithRawResponse:
    def __init__(self, meetings: MeetingsResource) -> None:
        self._meetings = meetings

        self.get_communities = to_raw_response_wrapper(
            meetings.get_communities,
        )


class AsyncMeetingsResourceWithRawResponse:
    def __init__(self, meetings: AsyncMeetingsResource) -> None:
        self._meetings = meetings

        self.get_communities = async_to_raw_response_wrapper(
            meetings.get_communities,
        )


class MeetingsResourceWithStreamingResponse:
    def __init__(self, meetings: MeetingsResource) -> None:
        self._meetings = meetings

        self.get_communities = to_streamed_response_wrapper(
            meetings.get_communities,
        )


class AsyncMeetingsResourceWithStreamingResponse:
    def __init__(self, meetings: AsyncMeetingsResource) -> None:
        self._meetings = meetings

        self.get_communities = async_to_streamed_response_wrapper(
            meetings.get_communities,
        )
