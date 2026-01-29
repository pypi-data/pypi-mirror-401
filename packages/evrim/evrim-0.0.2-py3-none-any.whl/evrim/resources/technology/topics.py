# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

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
    topic_search_params,
    topic_get_publications_params,
    topic_get_similar_topics_params,
)
from ...types.technology.topic_sort_field import TopicSortField
from ...types.technology.topic_search_response import TopicSearchResponse
from ...types.technology.topic_retrieve_response import TopicRetrieveResponse
from ...types.technology.topic_get_publications_response import TopicGetPublicationsResponse
from ...types.technology.topic_get_similar_topics_response import TopicGetSimilarTopicsResponse

__all__ = ["TopicsResource", "AsyncTopicsResource"]


class TopicsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TopicsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return TopicsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TopicsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return TopicsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        topic_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TopicRetrieveResponse:
        """
        Get detailed information about a specific technology topic.

        **Includes:**

        - Topic metadata (name, description, sub_areas)
        - Associated communities (JSONB array)
        - Publication count

        **Response Codes:**

        - 200: Success
        - 401: Unauthorized
        - 404: Topic not found

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not topic_id:
            raise ValueError(f"Expected a non-empty value for `topic_id` but received {topic_id!r}")
        return self._get(
            f"/technology/topics/{topic_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TopicRetrieveResponse,
        )

    def get_publications(
        self,
        topic_id: str,
        *,
        limit: int | Omit = omit,
        min_similarity: float | Omit = omit,
        offset: int | Omit = omit,
        sort_by: str | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        year_max: Optional[int] | Omit = omit,
        year_min: Optional[int] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TopicGetPublicationsResponse:
        """
        Get all publications matched to a topic with similarity scores.

        Returns publications that are semantically similar to the topic based on the
        publication-topic edge table. Each result includes the matched subarea and
        similarity score.

        **Query Parameters:**

        - min_similarity: Filter by minimum similarity (0.0-1.0)
        - limit: Maximum number of results (1-100)
        - offset: Pagination offset
        - sort_by: Sort by 'similarity', 'year', or 'title'
        - sort_order: 'asc' or 'desc'
        - year_min: Filter by minimum year
        - year_max: Filter by maximum year

        **Response Fields:**

        - publication_id, title, authors[], abstract
        - journal, year
        - matched_subarea: The subarea that matched
        - similarity: Similarity score (0-1)

        **Response Codes:**

        - 200: Success (empty list if no matches)
        - 401: Unauthorized

        Args:
          limit: Maximum results

          min_similarity: Minimum similarity score (0-1)

          offset: Pagination offset

          sort_by: Sort field: similarity, year, or title

          sort_order: Sort order

          year_max: Maximum publication year

          year_min: Minimum publication year

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not topic_id:
            raise ValueError(f"Expected a non-empty value for `topic_id` but received {topic_id!r}")
        return self._get(
            f"/technology/topics/{topic_id}/publications",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "min_similarity": min_similarity,
                        "offset": offset,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "year_max": year_max,
                        "year_min": year_min,
                    },
                    topic_get_publications_params.TopicGetPublicationsParams,
                ),
            ),
            cast_to=TopicGetPublicationsResponse,
        )

    def get_similar_topics(
        self,
        topic_id: str,
        *,
        limit: int | Omit = omit,
        min_similarity: float | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TopicGetSimilarTopicsResponse:
        """
        Get topics similar to a specific topic based on subarea semantic similarity.

        **Query Parameters:**

        - `min_similarity`: Minimum semantic similarity score (0-1, default 0.7)
        - `limit`: Maximum number of results (default 20)

        **Similarity Calculation:**

        - Based on semantic similarity between topic subareas
        - Uses technology_subarea_subarea_edges table with pre-computed embeddings
        - Returns topics with similarity >= min_similarity threshold

        **Response Codes:**

        - 200: Success
        - 401: Unauthorized

        Args:
          limit: Maximum number of similar topics

          min_similarity: Minimum similarity score

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not topic_id:
            raise ValueError(f"Expected a non-empty value for `topic_id` but received {topic_id!r}")
        return self._get(
            f"/technology/topics/{topic_id}/similar-topics",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "min_similarity": min_similarity,
                    },
                    topic_get_similar_topics_params.TopicGetSimilarTopicsParams,
                ),
            ),
            cast_to=TopicGetSimilarTopicsResponse,
        )

    def search(
        self,
        *,
        q: str,
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
    ) -> TopicSearchResponse:
        """
        Keyword search for technology topics.

        **Search Method:**

        - Full-text search on name, description, and sub_areas (ILIKE)
        - Case-insensitive pattern matching

        **Query Parameters:**

        - `q`: Search query (required)
        - `limit`: Maximum results (1-100, default 10)
        - `offset`: Pagination offset (default 0)
        - `sort_by`: Sort field (name, publication_count)
        - `sort_order`: Sort order (asc by default)

        **Response Codes:**

        - 200: Success
        - 422: Invalid parameters
        - 401: Unauthorized

        Args:
          q: Search query

          limit: Maximum number of results

          offset: Pagination offset

          sort_by: Fields available for sorting technology topics

          sort_order: Sort order

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/technology/topics/search",
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
                    topic_search_params.TopicSearchParams,
                ),
            ),
            cast_to=TopicSearchResponse,
        )


class AsyncTopicsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTopicsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTopicsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTopicsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return AsyncTopicsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        topic_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TopicRetrieveResponse:
        """
        Get detailed information about a specific technology topic.

        **Includes:**

        - Topic metadata (name, description, sub_areas)
        - Associated communities (JSONB array)
        - Publication count

        **Response Codes:**

        - 200: Success
        - 401: Unauthorized
        - 404: Topic not found

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not topic_id:
            raise ValueError(f"Expected a non-empty value for `topic_id` but received {topic_id!r}")
        return await self._get(
            f"/technology/topics/{topic_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TopicRetrieveResponse,
        )

    async def get_publications(
        self,
        topic_id: str,
        *,
        limit: int | Omit = omit,
        min_similarity: float | Omit = omit,
        offset: int | Omit = omit,
        sort_by: str | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        year_max: Optional[int] | Omit = omit,
        year_min: Optional[int] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TopicGetPublicationsResponse:
        """
        Get all publications matched to a topic with similarity scores.

        Returns publications that are semantically similar to the topic based on the
        publication-topic edge table. Each result includes the matched subarea and
        similarity score.

        **Query Parameters:**

        - min_similarity: Filter by minimum similarity (0.0-1.0)
        - limit: Maximum number of results (1-100)
        - offset: Pagination offset
        - sort_by: Sort by 'similarity', 'year', or 'title'
        - sort_order: 'asc' or 'desc'
        - year_min: Filter by minimum year
        - year_max: Filter by maximum year

        **Response Fields:**

        - publication_id, title, authors[], abstract
        - journal, year
        - matched_subarea: The subarea that matched
        - similarity: Similarity score (0-1)

        **Response Codes:**

        - 200: Success (empty list if no matches)
        - 401: Unauthorized

        Args:
          limit: Maximum results

          min_similarity: Minimum similarity score (0-1)

          offset: Pagination offset

          sort_by: Sort field: similarity, year, or title

          sort_order: Sort order

          year_max: Maximum publication year

          year_min: Minimum publication year

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not topic_id:
            raise ValueError(f"Expected a non-empty value for `topic_id` but received {topic_id!r}")
        return await self._get(
            f"/technology/topics/{topic_id}/publications",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "min_similarity": min_similarity,
                        "offset": offset,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "year_max": year_max,
                        "year_min": year_min,
                    },
                    topic_get_publications_params.TopicGetPublicationsParams,
                ),
            ),
            cast_to=TopicGetPublicationsResponse,
        )

    async def get_similar_topics(
        self,
        topic_id: str,
        *,
        limit: int | Omit = omit,
        min_similarity: float | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TopicGetSimilarTopicsResponse:
        """
        Get topics similar to a specific topic based on subarea semantic similarity.

        **Query Parameters:**

        - `min_similarity`: Minimum semantic similarity score (0-1, default 0.7)
        - `limit`: Maximum number of results (default 20)

        **Similarity Calculation:**

        - Based on semantic similarity between topic subareas
        - Uses technology_subarea_subarea_edges table with pre-computed embeddings
        - Returns topics with similarity >= min_similarity threshold

        **Response Codes:**

        - 200: Success
        - 401: Unauthorized

        Args:
          limit: Maximum number of similar topics

          min_similarity: Minimum similarity score

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not topic_id:
            raise ValueError(f"Expected a non-empty value for `topic_id` but received {topic_id!r}")
        return await self._get(
            f"/technology/topics/{topic_id}/similar-topics",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "min_similarity": min_similarity,
                    },
                    topic_get_similar_topics_params.TopicGetSimilarTopicsParams,
                ),
            ),
            cast_to=TopicGetSimilarTopicsResponse,
        )

    async def search(
        self,
        *,
        q: str,
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
    ) -> TopicSearchResponse:
        """
        Keyword search for technology topics.

        **Search Method:**

        - Full-text search on name, description, and sub_areas (ILIKE)
        - Case-insensitive pattern matching

        **Query Parameters:**

        - `q`: Search query (required)
        - `limit`: Maximum results (1-100, default 10)
        - `offset`: Pagination offset (default 0)
        - `sort_by`: Sort field (name, publication_count)
        - `sort_order`: Sort order (asc by default)

        **Response Codes:**

        - 200: Success
        - 422: Invalid parameters
        - 401: Unauthorized

        Args:
          q: Search query

          limit: Maximum number of results

          offset: Pagination offset

          sort_by: Fields available for sorting technology topics

          sort_order: Sort order

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/technology/topics/search",
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
                    topic_search_params.TopicSearchParams,
                ),
            ),
            cast_to=TopicSearchResponse,
        )


class TopicsResourceWithRawResponse:
    def __init__(self, topics: TopicsResource) -> None:
        self._topics = topics

        self.retrieve = to_raw_response_wrapper(
            topics.retrieve,
        )
        self.get_publications = to_raw_response_wrapper(
            topics.get_publications,
        )
        self.get_similar_topics = to_raw_response_wrapper(
            topics.get_similar_topics,
        )
        self.search = to_raw_response_wrapper(
            topics.search,
        )


class AsyncTopicsResourceWithRawResponse:
    def __init__(self, topics: AsyncTopicsResource) -> None:
        self._topics = topics

        self.retrieve = async_to_raw_response_wrapper(
            topics.retrieve,
        )
        self.get_publications = async_to_raw_response_wrapper(
            topics.get_publications,
        )
        self.get_similar_topics = async_to_raw_response_wrapper(
            topics.get_similar_topics,
        )
        self.search = async_to_raw_response_wrapper(
            topics.search,
        )


class TopicsResourceWithStreamingResponse:
    def __init__(self, topics: TopicsResource) -> None:
        self._topics = topics

        self.retrieve = to_streamed_response_wrapper(
            topics.retrieve,
        )
        self.get_publications = to_streamed_response_wrapper(
            topics.get_publications,
        )
        self.get_similar_topics = to_streamed_response_wrapper(
            topics.get_similar_topics,
        )
        self.search = to_streamed_response_wrapper(
            topics.search,
        )


class AsyncTopicsResourceWithStreamingResponse:
    def __init__(self, topics: AsyncTopicsResource) -> None:
        self._topics = topics

        self.retrieve = async_to_streamed_response_wrapper(
            topics.retrieve,
        )
        self.get_publications = async_to_streamed_response_wrapper(
            topics.get_publications,
        )
        self.get_similar_topics = async_to_streamed_response_wrapper(
            topics.get_similar_topics,
        )
        self.search = async_to_streamed_response_wrapper(
            topics.search,
        )
