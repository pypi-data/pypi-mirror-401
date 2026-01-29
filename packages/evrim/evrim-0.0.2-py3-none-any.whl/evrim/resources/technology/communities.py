# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, Optional, cast

import httpx

from ...types import SortOrder
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
from ...types.sort_order import SortOrder
from ...types.technology import (
    TopicSortField,
    CommunitySortField,
    PublicationSortField,
    community_list_params,
    community_search_params,
    community_get_topics_params,
    community_get_meetings_params,
    community_get_neighbors_params,
    community_get_publications_params,
)
from ...types.technology.topic_sort_field import TopicSortField
from ...types.technology.community_sort_field import CommunitySortField
from ...types.technology.publication_sort_field import PublicationSortField
from ...types.technology.community_list_response import CommunityListResponse
from ...types.technology.community_search_response import CommunitySearchResponse
from ...types.technology.community_retrieve_response import CommunityRetrieveResponse
from ...types.technology.community_get_topics_response import CommunityGetTopicsResponse
from ...types.technology.community_get_meetings_response import CommunityGetMeetingsResponse
from ...types.technology.community_get_neighbors_response import CommunityGetNeighborsResponse
from ...types.technology.community_get_publications_response import CommunityGetPublicationsResponse

__all__ = ["CommunitiesResource", "AsyncCommunitiesResource"]


class CommunitiesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CommunitiesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return CommunitiesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CommunitiesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return CommunitiesResourceWithStreamingResponse(self)

    def retrieve(
        self,
        community_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CommunityRetrieveResponse:
        """
        Get detailed information about a specific technology community.

        **Includes:**

        - Community metadata (summary, novelty assessment, novelty score)
        - Aggregated topics (JSONB array)
        - Incoming and outgoing neighbor counts

        **Response Codes:**

        - 200: Success
        - 401: Unauthorized
        - 404: Community not found
        - 422: Invalid UUID format

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not community_id:
            raise ValueError(f"Expected a non-empty value for `community_id` but received {community_id!r}")
        return self._get(
            f"/technology/communities/{community_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CommunityRetrieveResponse,
        )

    def list(
        self,
        *,
        end: int | Omit = omit,
        min_topics: Optional[int] | Omit = omit,
        novelty_score: Optional[str] | Omit = omit,
        sort_by: Optional[CommunitySortField] | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        start: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CommunityListResponse:
        """
        Get paginated list of technology research communities.

        **Query Parameters:**

        - `start`: Starting index (default: 0)
        - `end`: Ending index (default: 9)
        - `novelty_score`: Filter by novelty assessment
        - `min_topics`: Minimum number of topics in community
        - `sort_by`: Field to sort by (novelty, size, id)
        - `sort_order`: Sort order (asc, desc, default: desc)

        **Community Fields:**

        - community_id, community_uuid
        - summary, novelty_assessment, novelty_score
        - num_topics, topics[]
        - created_at, updated_at

        **Sorting Options:**

        - `novelty`: Sort by novelty score
        - `size`: Sort by number of topics
        - `id`: Sort by community ID

        **Default:** Sorted by ID in descending order

        Args:
          end: End index for pagination

          min_topics: Minimum number of topics in community

          novelty_score: Filter by novelty score: High, Medium, Low

          sort_by: Fields available for sorting technology communities

          sort_order: Sort order

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/technology/communities",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "end": end,
                        "min_topics": min_topics,
                        "novelty_score": novelty_score,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "start": start,
                    },
                    community_list_params.CommunityListParams,
                ),
            ),
            cast_to=CommunityListResponse,
        )

    def get_meetings(
        self,
        community_id: str,
        *,
        full: bool | Omit = omit,
        limit: int | Omit = omit,
        min_similarity: float | Omit = omit,
        offset: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CommunityGetMeetingsResponse:
        """
        Get meetings linked to a specific technology community via semantic similarity.

        **Path Parameters:**

        - `community_id`: UUID of the community

        **Query Parameters:**

        - `limit`: Maximum number of meetings to return (1-100, default: 10)
        - `offset`: Pagination offset (default: 0)
        - `min_similarity`: Minimum similarity threshold (0.0-1.0, default: 0.5)
        - `full`: Return full meeting details including participants, organizations,
          locations, sources (default: true)

        **Meeting Fields (basic):**

        - meeting_id (UUID): Meeting identifier
        - meeting_summary: Summary of the meeting
        - similarity: Semantic similarity score (0.0-1.0)
        - created_at: Timestamp when link was created

        **Additional Fields (when full=true):**

        - topic: Meeting topic
        - summary: Full meeting summary
        - updated_at: Last update timestamp
        - participants: Array of participant objects (id, name)
        - organizations: Array of organization objects (id, name)
        - locations: Array of location objects (id, name, country, etc.)
        - sources: Array of source objects (id, url, date_published)

        **Sorting:** Results are sorted by similarity descending (highest similarity
        first)

        **Response Codes:**

        - 200: Success
        - 404: Community not found
        - 401: Unauthorized
        - 422: Invalid parameters

        **Performance Note:** Use `full=true` (default) to avoid N+1 query problems when
        fetching meeting details. This returns all data in a single optimized database
        query.

        Args:
          full: Return full meeting details (participants, organizations, locations, sources)

          limit: Maximum number of meetings

          min_similarity: Minimum similarity threshold

          offset: Pagination offset

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not community_id:
            raise ValueError(f"Expected a non-empty value for `community_id` but received {community_id!r}")
        return cast(
            CommunityGetMeetingsResponse,
            self._get(
                f"/technology/communities/{community_id}/meetings",
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=maybe_transform(
                        {
                            "full": full,
                            "limit": limit,
                            "min_similarity": min_similarity,
                            "offset": offset,
                        },
                        community_get_meetings_params.CommunityGetMeetingsParams,
                    ),
                ),
                cast_to=cast(
                    Any, CommunityGetMeetingsResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def get_neighbors(
        self,
        community_id: str,
        *,
        direction: str | Omit = omit,
        limit: int | Omit = omit,
        min_strength: float | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CommunityGetNeighborsResponse:
        """
        Get neighboring communities connected by graph edges.

        **Query Parameters:**

        - `limit`: Maximum number of neighbors to return
        - `direction`: Filter by edge direction (incoming/outgoing/both)
        - `min_strength`: Minimum composite score (edge_count \\** avg_weight)
        - `sort_order`: Sort by composite score (desc by default)

        **Returns:**

        - Neighbor community metadata
        - Edge metrics (edge_count, avg_weight, max_weight, composite_score)
        - Direction of relationship

        **Response Codes:**

        - 200: Success
        - 401: Unauthorized
        - 422: Invalid UUID format

        Args:
          direction: Edge direction: 'incoming', 'outgoing', 'both'

          limit: Maximum number of neighbors

          min_strength: Minimum composite score threshold

          sort_order: Sort order by composite score

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not community_id:
            raise ValueError(f"Expected a non-empty value for `community_id` but received {community_id!r}")
        return self._get(
            f"/technology/communities/{community_id}/neighbors",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "direction": direction,
                        "limit": limit,
                        "min_strength": min_strength,
                        "sort_order": sort_order,
                    },
                    community_get_neighbors_params.CommunityGetNeighborsParams,
                ),
            ),
            cast_to=CommunityGetNeighborsResponse,
        )

    def get_publications(
        self,
        community_id: str,
        *,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        sort_by: Optional[PublicationSortField] | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        year_max: Optional[int] | Omit = omit,
        year_min: Optional[int] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CommunityGetPublicationsResponse:
        """
        Get publications related to a community via its topics.

        **Query Parameters:**

        - `limit`: Maximum number of results
        - `offset`: Pagination offset
        - `sort_by`: Field to sort by (year, title)
        - `sort_order`: Sort order (desc by default for year)
        - `year_min`: Filter by minimum publication year
        - `year_max`: Filter by maximum publication year

        **Publication Fields:**

        - id, title, authors[], abstract
        - journal, year, doi
        - matched_topics[] (JSONB with topic names and similarity scores)

        **Response Codes:**

        - 200: Success
        - 401: Unauthorized
        - 422: Invalid UUID format

        Args:
          limit: Maximum number of publications

          offset: Pagination offset

          sort_by: Fields available for sorting technology publications

          sort_order: Sort order

          year_max: Maximum publication year

          year_min: Minimum publication year

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not community_id:
            raise ValueError(f"Expected a non-empty value for `community_id` but received {community_id!r}")
        return self._get(
            f"/technology/communities/{community_id}/publications",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "year_max": year_max,
                        "year_min": year_min,
                    },
                    community_get_publications_params.CommunityGetPublicationsParams,
                ),
            ),
            cast_to=CommunityGetPublicationsResponse,
        )

    def get_topics(
        self,
        community_id: str,
        *,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        sort_by: Optional[TopicSortField] | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CommunityGetTopicsResponse:
        """
        Get topics belonging to a technology community.

        **Query Parameters:**

        - `limit`: Maximum number of results
        - `offset`: Pagination offset
        - `sort_by`: Field to sort by (name, publication_count)
        - `sort_order`: Sort order (asc, desc)

        **Topic Fields:**

        - id, name, description
        - sub_areas[], related_organizations[]
        - publication_count (from join)

        **Response Codes:**

        - 200: Success
        - 401: Unauthorized
        - 422: Invalid UUID format

        Args:
          limit: Maximum number of topics

          offset: Pagination offset

          sort_by: Fields available for sorting technology topics

          sort_order: Sort order

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not community_id:
            raise ValueError(f"Expected a non-empty value for `community_id` but received {community_id!r}")
        return self._get(
            f"/technology/communities/{community_id}/topics",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                    },
                    community_get_topics_params.CommunityGetTopicsParams,
                ),
            ),
            cast_to=CommunityGetTopicsResponse,
        )

    def search(
        self,
        *,
        q: str,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        sort_by: Optional[CommunitySortField] | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CommunitySearchResponse:
        """
        Keyword search for technology communities.

        **Search Method:**

        - Full-text search on summary and topics array (ILIKE)
        - Case-insensitive pattern matching

        **Query Parameters:**

        - `q`: Search query (required)
        - `limit`: Maximum results (1-100, default 10)
        - `offset`: Pagination offset (default 0)
        - `sort_by`: Sort field (id, size, novelty)
        - `sort_order`: Sort order (asc by default)

        **Response Codes:**

        - 200: Success
        - 422: Invalid parameters
        - 401: Unauthorized

        Args:
          q: Search query

          limit: Maximum number of results

          offset: Pagination offset

          sort_by: Fields available for sorting technology communities

          sort_order: Sort order

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/technology/communities/search",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "q": q,
                        "limit": limit,
                        "offset": offset,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                    },
                    community_search_params.CommunitySearchParams,
                ),
            ),
            cast_to=CommunitySearchResponse,
        )


class AsyncCommunitiesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCommunitiesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCommunitiesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCommunitiesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return AsyncCommunitiesResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        community_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CommunityRetrieveResponse:
        """
        Get detailed information about a specific technology community.

        **Includes:**

        - Community metadata (summary, novelty assessment, novelty score)
        - Aggregated topics (JSONB array)
        - Incoming and outgoing neighbor counts

        **Response Codes:**

        - 200: Success
        - 401: Unauthorized
        - 404: Community not found
        - 422: Invalid UUID format

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not community_id:
            raise ValueError(f"Expected a non-empty value for `community_id` but received {community_id!r}")
        return await self._get(
            f"/technology/communities/{community_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CommunityRetrieveResponse,
        )

    async def list(
        self,
        *,
        end: int | Omit = omit,
        min_topics: Optional[int] | Omit = omit,
        novelty_score: Optional[str] | Omit = omit,
        sort_by: Optional[CommunitySortField] | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        start: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CommunityListResponse:
        """
        Get paginated list of technology research communities.

        **Query Parameters:**

        - `start`: Starting index (default: 0)
        - `end`: Ending index (default: 9)
        - `novelty_score`: Filter by novelty assessment
        - `min_topics`: Minimum number of topics in community
        - `sort_by`: Field to sort by (novelty, size, id)
        - `sort_order`: Sort order (asc, desc, default: desc)

        **Community Fields:**

        - community_id, community_uuid
        - summary, novelty_assessment, novelty_score
        - num_topics, topics[]
        - created_at, updated_at

        **Sorting Options:**

        - `novelty`: Sort by novelty score
        - `size`: Sort by number of topics
        - `id`: Sort by community ID

        **Default:** Sorted by ID in descending order

        Args:
          end: End index for pagination

          min_topics: Minimum number of topics in community

          novelty_score: Filter by novelty score: High, Medium, Low

          sort_by: Fields available for sorting technology communities

          sort_order: Sort order

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/technology/communities",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "end": end,
                        "min_topics": min_topics,
                        "novelty_score": novelty_score,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "start": start,
                    },
                    community_list_params.CommunityListParams,
                ),
            ),
            cast_to=CommunityListResponse,
        )

    async def get_meetings(
        self,
        community_id: str,
        *,
        full: bool | Omit = omit,
        limit: int | Omit = omit,
        min_similarity: float | Omit = omit,
        offset: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CommunityGetMeetingsResponse:
        """
        Get meetings linked to a specific technology community via semantic similarity.

        **Path Parameters:**

        - `community_id`: UUID of the community

        **Query Parameters:**

        - `limit`: Maximum number of meetings to return (1-100, default: 10)
        - `offset`: Pagination offset (default: 0)
        - `min_similarity`: Minimum similarity threshold (0.0-1.0, default: 0.5)
        - `full`: Return full meeting details including participants, organizations,
          locations, sources (default: true)

        **Meeting Fields (basic):**

        - meeting_id (UUID): Meeting identifier
        - meeting_summary: Summary of the meeting
        - similarity: Semantic similarity score (0.0-1.0)
        - created_at: Timestamp when link was created

        **Additional Fields (when full=true):**

        - topic: Meeting topic
        - summary: Full meeting summary
        - updated_at: Last update timestamp
        - participants: Array of participant objects (id, name)
        - organizations: Array of organization objects (id, name)
        - locations: Array of location objects (id, name, country, etc.)
        - sources: Array of source objects (id, url, date_published)

        **Sorting:** Results are sorted by similarity descending (highest similarity
        first)

        **Response Codes:**

        - 200: Success
        - 404: Community not found
        - 401: Unauthorized
        - 422: Invalid parameters

        **Performance Note:** Use `full=true` (default) to avoid N+1 query problems when
        fetching meeting details. This returns all data in a single optimized database
        query.

        Args:
          full: Return full meeting details (participants, organizations, locations, sources)

          limit: Maximum number of meetings

          min_similarity: Minimum similarity threshold

          offset: Pagination offset

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not community_id:
            raise ValueError(f"Expected a non-empty value for `community_id` but received {community_id!r}")
        return cast(
            CommunityGetMeetingsResponse,
            await self._get(
                f"/technology/communities/{community_id}/meetings",
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=await async_maybe_transform(
                        {
                            "full": full,
                            "limit": limit,
                            "min_similarity": min_similarity,
                            "offset": offset,
                        },
                        community_get_meetings_params.CommunityGetMeetingsParams,
                    ),
                ),
                cast_to=cast(
                    Any, CommunityGetMeetingsResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def get_neighbors(
        self,
        community_id: str,
        *,
        direction: str | Omit = omit,
        limit: int | Omit = omit,
        min_strength: float | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CommunityGetNeighborsResponse:
        """
        Get neighboring communities connected by graph edges.

        **Query Parameters:**

        - `limit`: Maximum number of neighbors to return
        - `direction`: Filter by edge direction (incoming/outgoing/both)
        - `min_strength`: Minimum composite score (edge_count \\** avg_weight)
        - `sort_order`: Sort by composite score (desc by default)

        **Returns:**

        - Neighbor community metadata
        - Edge metrics (edge_count, avg_weight, max_weight, composite_score)
        - Direction of relationship

        **Response Codes:**

        - 200: Success
        - 401: Unauthorized
        - 422: Invalid UUID format

        Args:
          direction: Edge direction: 'incoming', 'outgoing', 'both'

          limit: Maximum number of neighbors

          min_strength: Minimum composite score threshold

          sort_order: Sort order by composite score

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not community_id:
            raise ValueError(f"Expected a non-empty value for `community_id` but received {community_id!r}")
        return await self._get(
            f"/technology/communities/{community_id}/neighbors",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "direction": direction,
                        "limit": limit,
                        "min_strength": min_strength,
                        "sort_order": sort_order,
                    },
                    community_get_neighbors_params.CommunityGetNeighborsParams,
                ),
            ),
            cast_to=CommunityGetNeighborsResponse,
        )

    async def get_publications(
        self,
        community_id: str,
        *,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        sort_by: Optional[PublicationSortField] | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        year_max: Optional[int] | Omit = omit,
        year_min: Optional[int] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CommunityGetPublicationsResponse:
        """
        Get publications related to a community via its topics.

        **Query Parameters:**

        - `limit`: Maximum number of results
        - `offset`: Pagination offset
        - `sort_by`: Field to sort by (year, title)
        - `sort_order`: Sort order (desc by default for year)
        - `year_min`: Filter by minimum publication year
        - `year_max`: Filter by maximum publication year

        **Publication Fields:**

        - id, title, authors[], abstract
        - journal, year, doi
        - matched_topics[] (JSONB with topic names and similarity scores)

        **Response Codes:**

        - 200: Success
        - 401: Unauthorized
        - 422: Invalid UUID format

        Args:
          limit: Maximum number of publications

          offset: Pagination offset

          sort_by: Fields available for sorting technology publications

          sort_order: Sort order

          year_max: Maximum publication year

          year_min: Minimum publication year

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not community_id:
            raise ValueError(f"Expected a non-empty value for `community_id` but received {community_id!r}")
        return await self._get(
            f"/technology/communities/{community_id}/publications",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "year_max": year_max,
                        "year_min": year_min,
                    },
                    community_get_publications_params.CommunityGetPublicationsParams,
                ),
            ),
            cast_to=CommunityGetPublicationsResponse,
        )

    async def get_topics(
        self,
        community_id: str,
        *,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        sort_by: Optional[TopicSortField] | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CommunityGetTopicsResponse:
        """
        Get topics belonging to a technology community.

        **Query Parameters:**

        - `limit`: Maximum number of results
        - `offset`: Pagination offset
        - `sort_by`: Field to sort by (name, publication_count)
        - `sort_order`: Sort order (asc, desc)

        **Topic Fields:**

        - id, name, description
        - sub_areas[], related_organizations[]
        - publication_count (from join)

        **Response Codes:**

        - 200: Success
        - 401: Unauthorized
        - 422: Invalid UUID format

        Args:
          limit: Maximum number of topics

          offset: Pagination offset

          sort_by: Fields available for sorting technology topics

          sort_order: Sort order

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not community_id:
            raise ValueError(f"Expected a non-empty value for `community_id` but received {community_id!r}")
        return await self._get(
            f"/technology/communities/{community_id}/topics",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                    },
                    community_get_topics_params.CommunityGetTopicsParams,
                ),
            ),
            cast_to=CommunityGetTopicsResponse,
        )

    async def search(
        self,
        *,
        q: str,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        sort_by: Optional[CommunitySortField] | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CommunitySearchResponse:
        """
        Keyword search for technology communities.

        **Search Method:**

        - Full-text search on summary and topics array (ILIKE)
        - Case-insensitive pattern matching

        **Query Parameters:**

        - `q`: Search query (required)
        - `limit`: Maximum results (1-100, default 10)
        - `offset`: Pagination offset (default 0)
        - `sort_by`: Sort field (id, size, novelty)
        - `sort_order`: Sort order (asc by default)

        **Response Codes:**

        - 200: Success
        - 422: Invalid parameters
        - 401: Unauthorized

        Args:
          q: Search query

          limit: Maximum number of results

          offset: Pagination offset

          sort_by: Fields available for sorting technology communities

          sort_order: Sort order

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/technology/communities/search",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "q": q,
                        "limit": limit,
                        "offset": offset,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                    },
                    community_search_params.CommunitySearchParams,
                ),
            ),
            cast_to=CommunitySearchResponse,
        )


class CommunitiesResourceWithRawResponse:
    def __init__(self, communities: CommunitiesResource) -> None:
        self._communities = communities

        self.retrieve = to_raw_response_wrapper(
            communities.retrieve,
        )
        self.list = to_raw_response_wrapper(
            communities.list,
        )
        self.get_meetings = to_raw_response_wrapper(
            communities.get_meetings,
        )
        self.get_neighbors = to_raw_response_wrapper(
            communities.get_neighbors,
        )
        self.get_publications = to_raw_response_wrapper(
            communities.get_publications,
        )
        self.get_topics = to_raw_response_wrapper(
            communities.get_topics,
        )
        self.search = to_raw_response_wrapper(
            communities.search,
        )


class AsyncCommunitiesResourceWithRawResponse:
    def __init__(self, communities: AsyncCommunitiesResource) -> None:
        self._communities = communities

        self.retrieve = async_to_raw_response_wrapper(
            communities.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            communities.list,
        )
        self.get_meetings = async_to_raw_response_wrapper(
            communities.get_meetings,
        )
        self.get_neighbors = async_to_raw_response_wrapper(
            communities.get_neighbors,
        )
        self.get_publications = async_to_raw_response_wrapper(
            communities.get_publications,
        )
        self.get_topics = async_to_raw_response_wrapper(
            communities.get_topics,
        )
        self.search = async_to_raw_response_wrapper(
            communities.search,
        )


class CommunitiesResourceWithStreamingResponse:
    def __init__(self, communities: CommunitiesResource) -> None:
        self._communities = communities

        self.retrieve = to_streamed_response_wrapper(
            communities.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            communities.list,
        )
        self.get_meetings = to_streamed_response_wrapper(
            communities.get_meetings,
        )
        self.get_neighbors = to_streamed_response_wrapper(
            communities.get_neighbors,
        )
        self.get_publications = to_streamed_response_wrapper(
            communities.get_publications,
        )
        self.get_topics = to_streamed_response_wrapper(
            communities.get_topics,
        )
        self.search = to_streamed_response_wrapper(
            communities.search,
        )


class AsyncCommunitiesResourceWithStreamingResponse:
    def __init__(self, communities: AsyncCommunitiesResource) -> None:
        self._communities = communities

        self.retrieve = async_to_streamed_response_wrapper(
            communities.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            communities.list,
        )
        self.get_meetings = async_to_streamed_response_wrapper(
            communities.get_meetings,
        )
        self.get_neighbors = async_to_streamed_response_wrapper(
            communities.get_neighbors,
        )
        self.get_publications = async_to_streamed_response_wrapper(
            communities.get_publications,
        )
        self.get_topics = async_to_streamed_response_wrapper(
            communities.get_topics,
        )
        self.search = async_to_streamed_response_wrapper(
            communities.search,
        )
