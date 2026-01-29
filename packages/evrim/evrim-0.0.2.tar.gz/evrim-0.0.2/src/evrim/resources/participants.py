# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ..types import SortOrder, ParticipantSortField, participant_list_params, participant_list_meetings_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.sort_order import SortOrder
from ..types.participant import Participant
from ..types.participant_sort_field import ParticipantSortField
from ..types.participant_list_response import ParticipantListResponse
from ..types.participant_list_meetings_response import ParticipantListMeetingsResponse

__all__ = ["ParticipantsResource", "AsyncParticipantsResource"]


class ParticipantsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ParticipantsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return ParticipantsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ParticipantsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return ParticipantsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Participant:
        """
        Get detailed information about a specific participant.

        Returns comprehensive participant data including names (Chinese and English),
        roles, affiliations, countries, and total meeting participation count.

        **Authentication:** Required

        **Path Parameters:**

        - `id`: UUID of the participant

        **Response Fields:**

        - Names in multiple languages
        - Roles and affiliations
        - Associated countries
        - Total number of meetings participated in

        **Response Codes:**

        - 200: Success
        - 404: Participant not found
        - 401: Unauthorized

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/participants/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Participant,
        )

    def list(
        self,
        *,
        end: int | Omit = omit,
        sort_by: Optional[ParticipantSortField] | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        start: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ParticipantListResponse:
        """
        Get paginated list of participants.

        Returns individuals who have participated in meetings, including their names,
        roles, affiliations, and meeting count.

        **Authentication:** Required

        **Query Parameters:**

        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)
        - `sort_by`: Field to sort by (default: None).
        - `sort_order`: Sort order (default: asc). Only available if `sort_by` is
          provided.

        **Participant Fields:**

        - Names (Chinese and English)
        - Roles and affiliations
        - Countries
        - Meeting participation count

        Args:
          end: End index for pagination

          sort_by: Fields available for sorting participants

          sort_order: Sort order

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/participants",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "end": end,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "start": start,
                    },
                    participant_list_params.ParticipantListParams,
                ),
            ),
            cast_to=ParticipantListResponse,
        )

    def list_meetings(
        self,
        id: str,
        *,
        end: int | Omit = omit,
        start: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ParticipantListMeetingsResponse:
        """
        Get all meetings associated with a specific participant.

        Returns a paginated list of all meetings that this participant has attended or
        been involved with, including full meeting details with participants,
        organizations, locations, and sources.

        **Authentication:** Required

        **Path Parameters:**

        - `id`: UUID of the participant

        **Query Parameters:**

        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)

        **Response:** Returns list of MeetingDetails objects with complete meeting
        information.

        **Response Codes:**

        - 200: Success (empty list if participant has no meetings)
        - 401: Unauthorized

        Args:
          end: End index for pagination

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/participants/{id}/meetings",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "end": end,
                        "start": start,
                    },
                    participant_list_meetings_params.ParticipantListMeetingsParams,
                ),
            ),
            cast_to=ParticipantListMeetingsResponse,
        )


class AsyncParticipantsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncParticipantsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return AsyncParticipantsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncParticipantsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return AsyncParticipantsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Participant:
        """
        Get detailed information about a specific participant.

        Returns comprehensive participant data including names (Chinese and English),
        roles, affiliations, countries, and total meeting participation count.

        **Authentication:** Required

        **Path Parameters:**

        - `id`: UUID of the participant

        **Response Fields:**

        - Names in multiple languages
        - Roles and affiliations
        - Associated countries
        - Total number of meetings participated in

        **Response Codes:**

        - 200: Success
        - 404: Participant not found
        - 401: Unauthorized

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/participants/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Participant,
        )

    async def list(
        self,
        *,
        end: int | Omit = omit,
        sort_by: Optional[ParticipantSortField] | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        start: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ParticipantListResponse:
        """
        Get paginated list of participants.

        Returns individuals who have participated in meetings, including their names,
        roles, affiliations, and meeting count.

        **Authentication:** Required

        **Query Parameters:**

        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)
        - `sort_by`: Field to sort by (default: None).
        - `sort_order`: Sort order (default: asc). Only available if `sort_by` is
          provided.

        **Participant Fields:**

        - Names (Chinese and English)
        - Roles and affiliations
        - Countries
        - Meeting participation count

        Args:
          end: End index for pagination

          sort_by: Fields available for sorting participants

          sort_order: Sort order

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/participants",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "end": end,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "start": start,
                    },
                    participant_list_params.ParticipantListParams,
                ),
            ),
            cast_to=ParticipantListResponse,
        )

    async def list_meetings(
        self,
        id: str,
        *,
        end: int | Omit = omit,
        start: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ParticipantListMeetingsResponse:
        """
        Get all meetings associated with a specific participant.

        Returns a paginated list of all meetings that this participant has attended or
        been involved with, including full meeting details with participants,
        organizations, locations, and sources.

        **Authentication:** Required

        **Path Parameters:**

        - `id`: UUID of the participant

        **Query Parameters:**

        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)

        **Response:** Returns list of MeetingDetails objects with complete meeting
        information.

        **Response Codes:**

        - 200: Success (empty list if participant has no meetings)
        - 401: Unauthorized

        Args:
          end: End index for pagination

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/participants/{id}/meetings",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "end": end,
                        "start": start,
                    },
                    participant_list_meetings_params.ParticipantListMeetingsParams,
                ),
            ),
            cast_to=ParticipantListMeetingsResponse,
        )


class ParticipantsResourceWithRawResponse:
    def __init__(self, participants: ParticipantsResource) -> None:
        self._participants = participants

        self.retrieve = to_raw_response_wrapper(
            participants.retrieve,
        )
        self.list = to_raw_response_wrapper(
            participants.list,
        )
        self.list_meetings = to_raw_response_wrapper(
            participants.list_meetings,
        )


class AsyncParticipantsResourceWithRawResponse:
    def __init__(self, participants: AsyncParticipantsResource) -> None:
        self._participants = participants

        self.retrieve = async_to_raw_response_wrapper(
            participants.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            participants.list,
        )
        self.list_meetings = async_to_raw_response_wrapper(
            participants.list_meetings,
        )


class ParticipantsResourceWithStreamingResponse:
    def __init__(self, participants: ParticipantsResource) -> None:
        self._participants = participants

        self.retrieve = to_streamed_response_wrapper(
            participants.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            participants.list,
        )
        self.list_meetings = to_streamed_response_wrapper(
            participants.list_meetings,
        )


class AsyncParticipantsResourceWithStreamingResponse:
    def __init__(self, participants: AsyncParticipantsResource) -> None:
        self._participants = participants

        self.retrieve = async_to_streamed_response_wrapper(
            participants.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            participants.list,
        )
        self.list_meetings = async_to_streamed_response_wrapper(
            participants.list_meetings,
        )
