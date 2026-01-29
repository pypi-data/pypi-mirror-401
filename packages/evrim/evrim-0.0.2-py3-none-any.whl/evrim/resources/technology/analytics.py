# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import Body, Query, Headers, NotGiven, not_given
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.technology.analytics_get_community_stats_response import AnalyticsGetCommunityStatsResponse

__all__ = ["AnalyticsResource", "AsyncAnalyticsResource"]


class AnalyticsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AnalyticsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return AnalyticsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AnalyticsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return AnalyticsResourceWithStreamingResponse(self)

    def get_community_stats(
        self,
        community_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AnalyticsGetCommunityStatsResponse:
        """
        Get detailed statistics for a specific technology community.

        **Path Parameters:**

        - community_id: UUID of the community to get stats for

        **Statistics:**

        - num_topics: Number of topics in the community
        - num_publications: Total publications related to community topics
        - avg_publication_year: Average year of publications
        - publication_year_range: [min_year, max_year]
        - top_organizations: Top 10 organizations mentioned in topics
        - topic_diversity: Ratio of community topics to total topics
        - total_connections: Number of edges to/from this community
        - avg_edge_strength: Average composite score of edges

        **Response Codes:**

        - 200: Success
        - 401: Unauthorized
        - 404: Community not found

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not community_id:
            raise ValueError(f"Expected a non-empty value for `community_id` but received {community_id!r}")
        return self._get(
            f"/technology/analytics/community-stats/{community_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AnalyticsGetCommunityStatsResponse,
        )


class AsyncAnalyticsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAnalyticsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAnalyticsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAnalyticsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return AsyncAnalyticsResourceWithStreamingResponse(self)

    async def get_community_stats(
        self,
        community_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AnalyticsGetCommunityStatsResponse:
        """
        Get detailed statistics for a specific technology community.

        **Path Parameters:**

        - community_id: UUID of the community to get stats for

        **Statistics:**

        - num_topics: Number of topics in the community
        - num_publications: Total publications related to community topics
        - avg_publication_year: Average year of publications
        - publication_year_range: [min_year, max_year]
        - top_organizations: Top 10 organizations mentioned in topics
        - topic_diversity: Ratio of community topics to total topics
        - total_connections: Number of edges to/from this community
        - avg_edge_strength: Average composite score of edges

        **Response Codes:**

        - 200: Success
        - 401: Unauthorized
        - 404: Community not found

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not community_id:
            raise ValueError(f"Expected a non-empty value for `community_id` but received {community_id!r}")
        return await self._get(
            f"/technology/analytics/community-stats/{community_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AnalyticsGetCommunityStatsResponse,
        )


class AnalyticsResourceWithRawResponse:
    def __init__(self, analytics: AnalyticsResource) -> None:
        self._analytics = analytics

        self.get_community_stats = to_raw_response_wrapper(
            analytics.get_community_stats,
        )


class AsyncAnalyticsResourceWithRawResponse:
    def __init__(self, analytics: AsyncAnalyticsResource) -> None:
        self._analytics = analytics

        self.get_community_stats = async_to_raw_response_wrapper(
            analytics.get_community_stats,
        )


class AnalyticsResourceWithStreamingResponse:
    def __init__(self, analytics: AnalyticsResource) -> None:
        self._analytics = analytics

        self.get_community_stats = to_streamed_response_wrapper(
            analytics.get_community_stats,
        )


class AsyncAnalyticsResourceWithStreamingResponse:
    def __init__(self, analytics: AsyncAnalyticsResource) -> None:
        self._analytics = analytics

        self.get_community_stats = async_to_streamed_response_wrapper(
            analytics.get_community_stats,
        )
