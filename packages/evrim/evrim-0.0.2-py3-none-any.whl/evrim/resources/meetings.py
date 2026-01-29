# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ..types import SortOrder, MeetingSortField, meeting_list_params, meeting_retrieve_params
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
from ..types.meeting_details import MeetingDetails
from ..types.meeting_sort_field import MeetingSortField
from ..types.meeting_list_response import MeetingListResponse

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

    def retrieve(
        self,
        id: str,
        *,
        full: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MeetingDetails:
        """
        Get detailed information about a specific meeting.

        Returns comprehensive meeting data including topic, summary, and optionally all
        related participants, organizations, locations, and source documents.

        **Authentication:** Required

        **Path Parameters:**

        - `id`: UUID of the meeting

        **Query Parameters:**

        - `full`: Include all related data (default: true)

        **Response Codes:**

        - 200: Success
        - 404: Meeting not found
        - 401: Unauthorized

        Args:
          full: Whether to include related organizations, participants, and location

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/meetings/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"full": full}, meeting_retrieve_params.MeetingRetrieveParams),
            ),
            cast_to=MeetingDetails,
        )

    def list(
        self,
        *,
        end: int | Omit = omit,
        full: bool | Omit = omit,
        sort_by: Optional[MeetingSortField] | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        start: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MeetingListResponse:
        """
        Get paginated list of meetings.

        Retrieves meetings with optional full details including participants,
        organizations, locations, and sources.

        **Authentication:** Required

        **Query Parameters:**

        - `start`: Starting index (default: 0)
        - `end`: Ending index (default: 9)
        - `full`: Include related data like participants and organizations (default:
          true)
        - `sort_by`: Field to sort by (default: None). Only available if `full` is true.
        - `sort_order`: Sort order (default: asc). Only available if `full` is true and
          `sort_by` is provided.

        **Note:** Sorting is only supported when `full=true`. If `sort_by` is provided
        with `full=false`, a 400 error will be returned.

        **Full Details Include:**

        - Topic and summary
        - List of participants with names and roles
        - Associated organizations
        - Meeting locations
        - Source documents

        **Example Response:**

        ```json
        [
          {
            "id": "uuid",
            "topic": "Meeting topic",
            "summary": "Meeting summary",
            "participants": [...],
            "organizations": [...],
            "locations": [...],
            "sources": [...]
          }
        ]
        ```

        Args:
          end: End index for pagination

          full: Whether to include related organizations, participants, and location

          sort_by: Fields available for sorting meetings

          sort_order: Sort order

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/meetings",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "end": end,
                        "full": full,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "start": start,
                    },
                    meeting_list_params.MeetingListParams,
                ),
            ),
            cast_to=MeetingListResponse,
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

    async def retrieve(
        self,
        id: str,
        *,
        full: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MeetingDetails:
        """
        Get detailed information about a specific meeting.

        Returns comprehensive meeting data including topic, summary, and optionally all
        related participants, organizations, locations, and source documents.

        **Authentication:** Required

        **Path Parameters:**

        - `id`: UUID of the meeting

        **Query Parameters:**

        - `full`: Include all related data (default: true)

        **Response Codes:**

        - 200: Success
        - 404: Meeting not found
        - 401: Unauthorized

        Args:
          full: Whether to include related organizations, participants, and location

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/meetings/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"full": full}, meeting_retrieve_params.MeetingRetrieveParams),
            ),
            cast_to=MeetingDetails,
        )

    async def list(
        self,
        *,
        end: int | Omit = omit,
        full: bool | Omit = omit,
        sort_by: Optional[MeetingSortField] | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        start: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MeetingListResponse:
        """
        Get paginated list of meetings.

        Retrieves meetings with optional full details including participants,
        organizations, locations, and sources.

        **Authentication:** Required

        **Query Parameters:**

        - `start`: Starting index (default: 0)
        - `end`: Ending index (default: 9)
        - `full`: Include related data like participants and organizations (default:
          true)
        - `sort_by`: Field to sort by (default: None). Only available if `full` is true.
        - `sort_order`: Sort order (default: asc). Only available if `full` is true and
          `sort_by` is provided.

        **Note:** Sorting is only supported when `full=true`. If `sort_by` is provided
        with `full=false`, a 400 error will be returned.

        **Full Details Include:**

        - Topic and summary
        - List of participants with names and roles
        - Associated organizations
        - Meeting locations
        - Source documents

        **Example Response:**

        ```json
        [
          {
            "id": "uuid",
            "topic": "Meeting topic",
            "summary": "Meeting summary",
            "participants": [...],
            "organizations": [...],
            "locations": [...],
            "sources": [...]
          }
        ]
        ```

        Args:
          end: End index for pagination

          full: Whether to include related organizations, participants, and location

          sort_by: Fields available for sorting meetings

          sort_order: Sort order

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/meetings",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "end": end,
                        "full": full,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "start": start,
                    },
                    meeting_list_params.MeetingListParams,
                ),
            ),
            cast_to=MeetingListResponse,
        )


class MeetingsResourceWithRawResponse:
    def __init__(self, meetings: MeetingsResource) -> None:
        self._meetings = meetings

        self.retrieve = to_raw_response_wrapper(
            meetings.retrieve,
        )
        self.list = to_raw_response_wrapper(
            meetings.list,
        )


class AsyncMeetingsResourceWithRawResponse:
    def __init__(self, meetings: AsyncMeetingsResource) -> None:
        self._meetings = meetings

        self.retrieve = async_to_raw_response_wrapper(
            meetings.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            meetings.list,
        )


class MeetingsResourceWithStreamingResponse:
    def __init__(self, meetings: MeetingsResource) -> None:
        self._meetings = meetings

        self.retrieve = to_streamed_response_wrapper(
            meetings.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            meetings.list,
        )


class AsyncMeetingsResourceWithStreamingResponse:
    def __init__(self, meetings: AsyncMeetingsResource) -> None:
        self._meetings = meetings

        self.retrieve = async_to_streamed_response_wrapper(
            meetings.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            meetings.list,
        )
