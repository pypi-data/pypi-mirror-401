# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...types import location_list_params, location_retrieve_meetings_params
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
from .search.search import (
    SearchResource,
    AsyncSearchResource,
    SearchResourceWithRawResponse,
    AsyncSearchResourceWithRawResponse,
    SearchResourceWithStreamingResponse,
    AsyncSearchResourceWithStreamingResponse,
)
from ..._base_client import make_request_options
from ...types.location import Location
from ...types.location_list_response import LocationListResponse
from ...types.location_retrieve_meetings_response import LocationRetrieveMeetingsResponse

__all__ = ["LocationsResource", "AsyncLocationsResource"]


class LocationsResource(SyncAPIResource):
    @cached_property
    def search(self) -> SearchResource:
        return SearchResource(self._client)

    @cached_property
    def with_raw_response(self) -> LocationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return LocationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> LocationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return LocationsResourceWithStreamingResponse(self)

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
    ) -> Location:
        """
        Get detailed information about a specific location.

        Returns complete location data including name, country, administrative division,
        and precise geographic coordinates.

        **Authentication:** Required

        **Path Parameters:**

        - `id`: UUID of the location

        **Response Fields:**

        - Location name
        - Country and admin1 (state/province/municipality)
        - Latitude and longitude coordinates
        - Timestamps

        **Use Cases:**

        - Get coordinates for mapping
        - Retrieve location details for meeting context
        - Geocoding and location analysis

        **Response Codes:**

        - 200: Success
        - 404: Location not found
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
            f"/locations/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Location,
        )

    def list(
        self,
        *,
        end: int | Omit = omit,
        start: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> LocationListResponse:
        """
        Get paginated list of meeting locations.

        Returns geographic locations where meetings have taken place, including
        coordinates, country, and administrative division information.

        **Authentication:** Required

        **Query Parameters:**

        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)

        **Location Fields:**

        - Name of the location
        - Country and administrative division (admin1)
        - Geographic coordinates (latitude/longitude)
        - Creation timestamp

        **Example Response:**

        ```json
        [
          {
            "id": "uuid",
            "name": "Beijing",
            "country": "China",
            "admin1": "Beijing Municipality",
            "lat": 39.9042,
            "lon": 116.4074,
            "created_at": "2024-01-01T00:00:00Z"
          }
        ]
        ```

        Args:
          end: End index for pagination

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/locations",
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
                    location_list_params.LocationListParams,
                ),
            ),
            cast_to=LocationListResponse,
        )

    def retrieve_meetings(
        self,
        id: str,
        *,
        end: int | Omit = omit,
        full: bool | Omit = omit,
        start: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> LocationRetrieveMeetingsResponse:
        """
        Get all meetings associated with a specific location.

        Returns a paginated list of all meetings that took place at this location, with
        optional full details including participants, organizations, other locations,
        and source documents.

        **Authentication:** Required

        **Path Parameters:**

        - `id`: UUID of the location

        **Query Parameters:**

        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)
        - `full`: Include all related data (default: true)
          - When true: Returns complete meeting information with participants,
            organizations, all locations, and sources
          - When false: Returns basic meeting data only (id, topic, summary)

        **Response:** Returns list of MeetingDetails objects. When `full=true`,
        includes:

        - Complete meeting information
        - All participants involved
        - All organizations involved
        - All locations (the meeting may have occurred in multiple locations)
        - Source documents

        **Use Cases:**

        - View all meetings at a specific location
        - Analyze meeting activity by location
        - Build location-based meeting timelines
        - Export location meeting data

        **Example:**

        ```
        GET /locations/{id}/meetings?start=0&end=9&full=true
        ```

        **Response Codes:**

        - 200: Success (empty list if location has no meetings)
        - 401: Unauthorized
        - 422: Invalid UUID format

        Args:
          end: End index for pagination

          full: Whether to include related organizations, participants, and sources

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/locations/{id}/meetings",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "end": end,
                        "full": full,
                        "start": start,
                    },
                    location_retrieve_meetings_params.LocationRetrieveMeetingsParams,
                ),
            ),
            cast_to=LocationRetrieveMeetingsResponse,
        )


class AsyncLocationsResource(AsyncAPIResource):
    @cached_property
    def search(self) -> AsyncSearchResource:
        return AsyncSearchResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncLocationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return AsyncLocationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncLocationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return AsyncLocationsResourceWithStreamingResponse(self)

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
    ) -> Location:
        """
        Get detailed information about a specific location.

        Returns complete location data including name, country, administrative division,
        and precise geographic coordinates.

        **Authentication:** Required

        **Path Parameters:**

        - `id`: UUID of the location

        **Response Fields:**

        - Location name
        - Country and admin1 (state/province/municipality)
        - Latitude and longitude coordinates
        - Timestamps

        **Use Cases:**

        - Get coordinates for mapping
        - Retrieve location details for meeting context
        - Geocoding and location analysis

        **Response Codes:**

        - 200: Success
        - 404: Location not found
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
            f"/locations/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Location,
        )

    async def list(
        self,
        *,
        end: int | Omit = omit,
        start: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> LocationListResponse:
        """
        Get paginated list of meeting locations.

        Returns geographic locations where meetings have taken place, including
        coordinates, country, and administrative division information.

        **Authentication:** Required

        **Query Parameters:**

        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)

        **Location Fields:**

        - Name of the location
        - Country and administrative division (admin1)
        - Geographic coordinates (latitude/longitude)
        - Creation timestamp

        **Example Response:**

        ```json
        [
          {
            "id": "uuid",
            "name": "Beijing",
            "country": "China",
            "admin1": "Beijing Municipality",
            "lat": 39.9042,
            "lon": 116.4074,
            "created_at": "2024-01-01T00:00:00Z"
          }
        ]
        ```

        Args:
          end: End index for pagination

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/locations",
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
                    location_list_params.LocationListParams,
                ),
            ),
            cast_to=LocationListResponse,
        )

    async def retrieve_meetings(
        self,
        id: str,
        *,
        end: int | Omit = omit,
        full: bool | Omit = omit,
        start: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> LocationRetrieveMeetingsResponse:
        """
        Get all meetings associated with a specific location.

        Returns a paginated list of all meetings that took place at this location, with
        optional full details including participants, organizations, other locations,
        and source documents.

        **Authentication:** Required

        **Path Parameters:**

        - `id`: UUID of the location

        **Query Parameters:**

        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)
        - `full`: Include all related data (default: true)
          - When true: Returns complete meeting information with participants,
            organizations, all locations, and sources
          - When false: Returns basic meeting data only (id, topic, summary)

        **Response:** Returns list of MeetingDetails objects. When `full=true`,
        includes:

        - Complete meeting information
        - All participants involved
        - All organizations involved
        - All locations (the meeting may have occurred in multiple locations)
        - Source documents

        **Use Cases:**

        - View all meetings at a specific location
        - Analyze meeting activity by location
        - Build location-based meeting timelines
        - Export location meeting data

        **Example:**

        ```
        GET /locations/{id}/meetings?start=0&end=9&full=true
        ```

        **Response Codes:**

        - 200: Success (empty list if location has no meetings)
        - 401: Unauthorized
        - 422: Invalid UUID format

        Args:
          end: End index for pagination

          full: Whether to include related organizations, participants, and sources

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/locations/{id}/meetings",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "end": end,
                        "full": full,
                        "start": start,
                    },
                    location_retrieve_meetings_params.LocationRetrieveMeetingsParams,
                ),
            ),
            cast_to=LocationRetrieveMeetingsResponse,
        )


class LocationsResourceWithRawResponse:
    def __init__(self, locations: LocationsResource) -> None:
        self._locations = locations

        self.retrieve = to_raw_response_wrapper(
            locations.retrieve,
        )
        self.list = to_raw_response_wrapper(
            locations.list,
        )
        self.retrieve_meetings = to_raw_response_wrapper(
            locations.retrieve_meetings,
        )

    @cached_property
    def search(self) -> SearchResourceWithRawResponse:
        return SearchResourceWithRawResponse(self._locations.search)


class AsyncLocationsResourceWithRawResponse:
    def __init__(self, locations: AsyncLocationsResource) -> None:
        self._locations = locations

        self.retrieve = async_to_raw_response_wrapper(
            locations.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            locations.list,
        )
        self.retrieve_meetings = async_to_raw_response_wrapper(
            locations.retrieve_meetings,
        )

    @cached_property
    def search(self) -> AsyncSearchResourceWithRawResponse:
        return AsyncSearchResourceWithRawResponse(self._locations.search)


class LocationsResourceWithStreamingResponse:
    def __init__(self, locations: LocationsResource) -> None:
        self._locations = locations

        self.retrieve = to_streamed_response_wrapper(
            locations.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            locations.list,
        )
        self.retrieve_meetings = to_streamed_response_wrapper(
            locations.retrieve_meetings,
        )

    @cached_property
    def search(self) -> SearchResourceWithStreamingResponse:
        return SearchResourceWithStreamingResponse(self._locations.search)


class AsyncLocationsResourceWithStreamingResponse:
    def __init__(self, locations: AsyncLocationsResource) -> None:
        self._locations = locations

        self.retrieve = async_to_streamed_response_wrapper(
            locations.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            locations.list,
        )
        self.retrieve_meetings = async_to_streamed_response_wrapper(
            locations.retrieve_meetings,
        )

    @cached_property
    def search(self) -> AsyncSearchResourceWithStreamingResponse:
        return AsyncSearchResourceWithStreamingResponse(self._locations.search)
