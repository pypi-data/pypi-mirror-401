# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .admin1 import (
    Admin1Resource,
    AsyncAdmin1Resource,
    Admin1ResourceWithRawResponse,
    AsyncAdmin1ResourceWithRawResponse,
    Admin1ResourceWithStreamingResponse,
    AsyncAdmin1ResourceWithStreamingResponse,
)
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
from ....types.locations import search_by_bbox_params, search_by_radius_params
from ....types.locations.search_by_bbox_response import SearchByBboxResponse
from ....types.locations.search_by_radius_response import SearchByRadiusResponse

__all__ = ["SearchResource", "AsyncSearchResource"]


class SearchResource(SyncAPIResource):
    @cached_property
    def admin1(self) -> Admin1Resource:
        return Admin1Resource(self._client)

    @cached_property
    def with_raw_response(self) -> SearchResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return SearchResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SearchResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return SearchResourceWithStreamingResponse(self)

    def by_bbox(
        self,
        *,
        max_lat: float,
        max_lon: float,
        min_lat: float,
        min_lon: float,
        end: int | Omit = omit,
        start: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SearchByBboxResponse:
        """
        Search meetings by location bounding box (rectangular area).

        Returns all meetings at locations within the specified rectangular geographic
        area defined by minimum and maximum latitude/longitude coordinates.

        **Authentication:** Required

        **Query Parameters:**

        - `min_lat`: Minimum latitude (-90 to 90)
        - `max_lat`: Maximum latitude (-90 to 90)
        - `min_lon`: Minimum longitude (-180 to 180)
        - `max_lon`: Maximum longitude (-180 to 180)
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

        - Search meetings in a specific geographic region
        - Find all meetings within city/province boundaries
        - Geographic analysis of meeting patterns
        - Map-based meeting discovery

        **Example:**

        ```
        # Search meetings in Beijing area
        GET /locations/search/bbox?min_lat=39.7&max_lat=40.1&min_lon=116.2&max_lon=116.6
        ```

        **Response Codes:**

        - 200: Success (empty list if no meetings found)
        - 401: Unauthorized
        - 422: Invalid coordinates

        Args:
          max_lat: Maximum latitude of bounding box

          max_lon: Maximum longitude of bounding box

          min_lat: Minimum latitude of bounding box

          min_lon: Minimum longitude of bounding box

          end: End index for pagination

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/locations/search/bbox",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "max_lat": max_lat,
                        "max_lon": max_lon,
                        "min_lat": min_lat,
                        "min_lon": min_lon,
                        "end": end,
                        "start": start,
                    },
                    search_by_bbox_params.SearchByBboxParams,
                ),
            ),
            cast_to=SearchByBboxResponse,
        )

    def by_radius(
        self,
        *,
        lat: float,
        lon: float,
        radius: float,
        end: int | Omit = omit,
        start: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SearchByRadiusResponse:
        """
        Search meetings by radius from a geographic point.

        Returns all meetings at locations within the specified radius from a center
        point, sorted by distance (nearest first). Each result includes the distance in
        kilometers.

        **Authentication:** Required

        **Query Parameters:**

        - `lat`: Latitude of center point (-90 to 90)
        - `lon`: Longitude of center point (-180 to 180)
        - `radius`: Search radius in kilometers (0 to 20,000 km)
        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)

        **Response:** Returns list of MeetingDetailsWithDistance objects, sorted by
        distance. Includes:

        - Complete meeting information
        - All participants involved
        - All organizations involved
        - All locations (meetings may span multiple locations)
        - Source documents
        - **distance_km**: Distance from search center in kilometers

        **Use Cases:**

        - Find meetings near a specific location
        - Discover nearby meetings from current position
        - Proximity-based meeting analysis
        - Location-aware meeting recommendations

        **Example:**

        ```
        # Find meetings within 50km of Beijing city center
        GET /locations/search/radius?lat=39.9042&lon=116.4074&radius=50
        ```

        **Response Example:**

        ```json
        [
          {
            "id": "uuid",
            "topic": "Meeting topic",
            "distance_km": 12.5,
            ...
          }
        ]
        ```

        **Response Codes:**

        - 200: Success (empty list if no meetings found)
        - 401: Unauthorized
        - 422: Invalid coordinates or radius

        Args:
          lat: Latitude of search center

          lon: Longitude of search center

          radius: Search radius in kilometers (max 20,000 km)

          end: End index for pagination

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/locations/search/radius",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "lat": lat,
                        "lon": lon,
                        "radius": radius,
                        "end": end,
                        "start": start,
                    },
                    search_by_radius_params.SearchByRadiusParams,
                ),
            ),
            cast_to=SearchByRadiusResponse,
        )


class AsyncSearchResource(AsyncAPIResource):
    @cached_property
    def admin1(self) -> AsyncAdmin1Resource:
        return AsyncAdmin1Resource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncSearchResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSearchResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSearchResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return AsyncSearchResourceWithStreamingResponse(self)

    async def by_bbox(
        self,
        *,
        max_lat: float,
        max_lon: float,
        min_lat: float,
        min_lon: float,
        end: int | Omit = omit,
        start: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SearchByBboxResponse:
        """
        Search meetings by location bounding box (rectangular area).

        Returns all meetings at locations within the specified rectangular geographic
        area defined by minimum and maximum latitude/longitude coordinates.

        **Authentication:** Required

        **Query Parameters:**

        - `min_lat`: Minimum latitude (-90 to 90)
        - `max_lat`: Maximum latitude (-90 to 90)
        - `min_lon`: Minimum longitude (-180 to 180)
        - `max_lon`: Maximum longitude (-180 to 180)
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

        - Search meetings in a specific geographic region
        - Find all meetings within city/province boundaries
        - Geographic analysis of meeting patterns
        - Map-based meeting discovery

        **Example:**

        ```
        # Search meetings in Beijing area
        GET /locations/search/bbox?min_lat=39.7&max_lat=40.1&min_lon=116.2&max_lon=116.6
        ```

        **Response Codes:**

        - 200: Success (empty list if no meetings found)
        - 401: Unauthorized
        - 422: Invalid coordinates

        Args:
          max_lat: Maximum latitude of bounding box

          max_lon: Maximum longitude of bounding box

          min_lat: Minimum latitude of bounding box

          min_lon: Minimum longitude of bounding box

          end: End index for pagination

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/locations/search/bbox",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "max_lat": max_lat,
                        "max_lon": max_lon,
                        "min_lat": min_lat,
                        "min_lon": min_lon,
                        "end": end,
                        "start": start,
                    },
                    search_by_bbox_params.SearchByBboxParams,
                ),
            ),
            cast_to=SearchByBboxResponse,
        )

    async def by_radius(
        self,
        *,
        lat: float,
        lon: float,
        radius: float,
        end: int | Omit = omit,
        start: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SearchByRadiusResponse:
        """
        Search meetings by radius from a geographic point.

        Returns all meetings at locations within the specified radius from a center
        point, sorted by distance (nearest first). Each result includes the distance in
        kilometers.

        **Authentication:** Required

        **Query Parameters:**

        - `lat`: Latitude of center point (-90 to 90)
        - `lon`: Longitude of center point (-180 to 180)
        - `radius`: Search radius in kilometers (0 to 20,000 km)
        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)

        **Response:** Returns list of MeetingDetailsWithDistance objects, sorted by
        distance. Includes:

        - Complete meeting information
        - All participants involved
        - All organizations involved
        - All locations (meetings may span multiple locations)
        - Source documents
        - **distance_km**: Distance from search center in kilometers

        **Use Cases:**

        - Find meetings near a specific location
        - Discover nearby meetings from current position
        - Proximity-based meeting analysis
        - Location-aware meeting recommendations

        **Example:**

        ```
        # Find meetings within 50km of Beijing city center
        GET /locations/search/radius?lat=39.9042&lon=116.4074&radius=50
        ```

        **Response Example:**

        ```json
        [
          {
            "id": "uuid",
            "topic": "Meeting topic",
            "distance_km": 12.5,
            ...
          }
        ]
        ```

        **Response Codes:**

        - 200: Success (empty list if no meetings found)
        - 401: Unauthorized
        - 422: Invalid coordinates or radius

        Args:
          lat: Latitude of search center

          lon: Longitude of search center

          radius: Search radius in kilometers (max 20,000 km)

          end: End index for pagination

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/locations/search/radius",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "lat": lat,
                        "lon": lon,
                        "radius": radius,
                        "end": end,
                        "start": start,
                    },
                    search_by_radius_params.SearchByRadiusParams,
                ),
            ),
            cast_to=SearchByRadiusResponse,
        )


class SearchResourceWithRawResponse:
    def __init__(self, search: SearchResource) -> None:
        self._search = search

        self.by_bbox = to_raw_response_wrapper(
            search.by_bbox,
        )
        self.by_radius = to_raw_response_wrapper(
            search.by_radius,
        )

    @cached_property
    def admin1(self) -> Admin1ResourceWithRawResponse:
        return Admin1ResourceWithRawResponse(self._search.admin1)


class AsyncSearchResourceWithRawResponse:
    def __init__(self, search: AsyncSearchResource) -> None:
        self._search = search

        self.by_bbox = async_to_raw_response_wrapper(
            search.by_bbox,
        )
        self.by_radius = async_to_raw_response_wrapper(
            search.by_radius,
        )

    @cached_property
    def admin1(self) -> AsyncAdmin1ResourceWithRawResponse:
        return AsyncAdmin1ResourceWithRawResponse(self._search.admin1)


class SearchResourceWithStreamingResponse:
    def __init__(self, search: SearchResource) -> None:
        self._search = search

        self.by_bbox = to_streamed_response_wrapper(
            search.by_bbox,
        )
        self.by_radius = to_streamed_response_wrapper(
            search.by_radius,
        )

    @cached_property
    def admin1(self) -> Admin1ResourceWithStreamingResponse:
        return Admin1ResourceWithStreamingResponse(self._search.admin1)


class AsyncSearchResourceWithStreamingResponse:
    def __init__(self, search: AsyncSearchResource) -> None:
        self._search = search

        self.by_bbox = async_to_streamed_response_wrapper(
            search.by_bbox,
        )
        self.by_radius = async_to_streamed_response_wrapper(
            search.by_radius,
        )

    @cached_property
    def admin1(self) -> AsyncAdmin1ResourceWithStreamingResponse:
        return AsyncAdmin1ResourceWithStreamingResponse(self._search.admin1)
