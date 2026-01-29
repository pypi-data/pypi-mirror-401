# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ...._utils import maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.locations.search import admin1_list_meetings_params
from ....types.locations.search.admin1_list_meetings_response import Admin1ListMeetingsResponse

__all__ = ["Admin1Resource", "AsyncAdmin1Resource"]


class Admin1Resource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> Admin1ResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return Admin1ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> Admin1ResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return Admin1ResourceWithStreamingResponse(self)

    def list_meetings(
        self,
        *,
        admin1: str,
        end: int | Omit = omit,
        start: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Admin1ListMeetingsResponse:
        """
        Search meetings by location administrative division (admin1).

        Returns all meetings at locations within the specified administrative division
        (e.g., state, province, municipality). Search is case-insensitive and requires
        exact match of the admin1 field.

        **Authentication:** Required

        **Query Parameters:**

        - `admin1`: Administrative division name (1-200 characters)
        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)

        **Response:** Returns list of MeetingDetails objects with full information
        including:

        - Complete meeting information
        - All participants involved
        - All organizations involved
        - All locations (meetings may span multiple locations)
        - Source documents

        **Use Cases:**

        - Find all meetings in a specific province/state
        - Analyze meeting patterns by administrative region
        - Filter meetings by local jurisdiction
        - Regional meeting discovery

        **Example:**

        ```
        # Search meetings in Beijing Municipality
        GET /locations/search/admin1?admin1=Beijing%20Municipality

        # Search meetings in California
        GET /locations/search/admin1?admin1=California
        ```

        **Response Codes:**

        - 200: Success (empty list if no meetings found)
        - 401: Unauthorized
        - 422: Invalid admin1 parameter (too short/long)

        **Note:** The search is case-insensitive and requires exact match. For partial
        matching, consider using text search endpoints.

        Args:
          admin1: Administrative division name (e.g., 'Beijing Municipality', 'California')

          end: End index for pagination

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/locations/search/admin1/meetings",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "admin1": admin1,
                        "end": end,
                        "start": start,
                    },
                    admin1_list_meetings_params.Admin1ListMeetingsParams,
                ),
            ),
            cast_to=Admin1ListMeetingsResponse,
        )


class AsyncAdmin1Resource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAdmin1ResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAdmin1ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAdmin1ResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return AsyncAdmin1ResourceWithStreamingResponse(self)

    async def list_meetings(
        self,
        *,
        admin1: str,
        end: int | Omit = omit,
        start: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Admin1ListMeetingsResponse:
        """
        Search meetings by location administrative division (admin1).

        Returns all meetings at locations within the specified administrative division
        (e.g., state, province, municipality). Search is case-insensitive and requires
        exact match of the admin1 field.

        **Authentication:** Required

        **Query Parameters:**

        - `admin1`: Administrative division name (1-200 characters)
        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)

        **Response:** Returns list of MeetingDetails objects with full information
        including:

        - Complete meeting information
        - All participants involved
        - All organizations involved
        - All locations (meetings may span multiple locations)
        - Source documents

        **Use Cases:**

        - Find all meetings in a specific province/state
        - Analyze meeting patterns by administrative region
        - Filter meetings by local jurisdiction
        - Regional meeting discovery

        **Example:**

        ```
        # Search meetings in Beijing Municipality
        GET /locations/search/admin1?admin1=Beijing%20Municipality

        # Search meetings in California
        GET /locations/search/admin1?admin1=California
        ```

        **Response Codes:**

        - 200: Success (empty list if no meetings found)
        - 401: Unauthorized
        - 422: Invalid admin1 parameter (too short/long)

        **Note:** The search is case-insensitive and requires exact match. For partial
        matching, consider using text search endpoints.

        Args:
          admin1: Administrative division name (e.g., 'Beijing Municipality', 'California')

          end: End index for pagination

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/locations/search/admin1/meetings",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "admin1": admin1,
                        "end": end,
                        "start": start,
                    },
                    admin1_list_meetings_params.Admin1ListMeetingsParams,
                ),
            ),
            cast_to=Admin1ListMeetingsResponse,
        )


class Admin1ResourceWithRawResponse:
    def __init__(self, admin1: Admin1Resource) -> None:
        self._admin1 = admin1

        self.list_meetings = to_raw_response_wrapper(
            admin1.list_meetings,
        )


class AsyncAdmin1ResourceWithRawResponse:
    def __init__(self, admin1: AsyncAdmin1Resource) -> None:
        self._admin1 = admin1

        self.list_meetings = async_to_raw_response_wrapper(
            admin1.list_meetings,
        )


class Admin1ResourceWithStreamingResponse:
    def __init__(self, admin1: Admin1Resource) -> None:
        self._admin1 = admin1

        self.list_meetings = to_streamed_response_wrapper(
            admin1.list_meetings,
        )


class AsyncAdmin1ResourceWithStreamingResponse:
    def __init__(self, admin1: AsyncAdmin1Resource) -> None:
        self._admin1 = admin1

        self.list_meetings = async_to_streamed_response_wrapper(
            admin1.list_meetings,
        )
