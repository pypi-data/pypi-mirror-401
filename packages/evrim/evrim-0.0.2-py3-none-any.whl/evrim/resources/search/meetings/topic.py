# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ....types import SortOrder, MeetingSortField
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
from ....types.sort_order import SortOrder
from ....types.search.meetings import topic_search_params, topic_search_semantic_params
from ....types.meeting_sort_field import MeetingSortField
from ....types.search.meetings.topic_search_response import TopicSearchResponse
from ....types.search.meetings.topic_search_semantic_response import TopicSearchSemanticResponse

__all__ = ["TopicResource", "AsyncTopicResource"]


class TopicResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TopicResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return TopicResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TopicResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return TopicResourceWithStreamingResponse(self)

    def search(
        self,
        *,
        q: str,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        sort_by: Optional[MeetingSortField] | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TopicSearchResponse:
        """
        Search meetings by topic using exact keyword matching.

        Traditional keyword search that finds meetings where the topic contains your
        search term. Fast and precise for exact text matching.

        **Authentication:** Required

        **Search Method:**

        - Case-insensitive substring matching
        - Searches the topic field only
        - Exact text matching (not semantic)

        **Query Parameters:**

        - `q`: Search term (required)
          - Example: "trade" → matches "International Trade Summit"
          - Example: "合作" → matches topics with "合作" in Chinese
        - `limit`: Maximum results (1-100, default: 10)
        - `offset`: Skip first N results for pagination (default: 0)

        **Response:** Returns list of MeetingDetails with full information including
        participants, organizations, locations, and sources.

        **When to Use:**

        - When you know the exact topic keywords
        - For precise, predictable matching
        - When you need fast results

        **Comparison with Semantic Search:**

        - Keyword: Fast, exact matching, requires correct wording
        - Semantic: Slower, finds conceptually similar topics, handles paraphrasing

        **Example:**

        ```
        GET /search/meetings/topic?q=economic&limit=10&offset=0
        ```

        **Response Codes:**

        - 200: Success
        - 401: Unauthorized

        Args:
          q: Search query string

          limit: Maximum number of results

          offset: Offset for pagination

          sort_by: Fields available for sorting meetings

          sort_order: Sort order

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/search/meetings/topic",
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

    def search_semantic(
        self,
        *,
        q: str,
        limit: int | Omit = omit,
        threshold: float | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TopicSearchSemanticResponse:
        """
        Search meetings by topic using AI-powered semantic similarity.

        This endpoint uses advanced natural language understanding to find meetings
        based on topic similarity rather than exact keyword matches. Perfect for
        discovering related meetings even when they use different terminology.

        **Authentication:** Required

        **How It Works:**

        1. Your search query is converted to a semantic vector (embedding)
        2. Meeting topics are matched based on conceptual similarity
        3. Results are ranked by relevance score

        **Query Parameters:**

        - `q`: Your search query (required)
          - Example: "trade negotiations"
          - Example: "climate change policy"
          - Works with Chinese: "经济合作"
        - `limit`: Maximum results to return (1-100, default: 10)
        - `threshold`: Minimum similarity score 0-1 (default: 0.5)
          - Lower (0.3-0.5): More results, broader matches
          - Higher (0.6-0.8): Fewer results, more precise matches

        **Response Fields:**

        - All meeting details (id, topic, summary, participants, organizations, etc.)
        - `similarity`: Relevance score (0-1), higher = more relevant

        **Example Request:**

        ```
        GET /search/meetings/topic/semantic?q=economic%20cooperation&limit=5&threshold=0.6
        ```

        **Example Response:**

        ```json
        [
          {
            "id": "uuid",
            "topic": "Regional Economic Partnership",
            "summary": "Discussion on trade agreements...",
            "similarity": 0.87,
            "participants": [...],
            "organizations": [...]
          }
        ]
        ```

        **Tips:**

        - Use natural language queries for best results
        - Works across Chinese and English
        - Finds conceptually similar content even with different wording
        - Much faster than keyword search on large datasets

        **Response Codes:**

        - 200: Success
        - 400: Invalid query (empty text)
        - 401: Unauthorized
        - 500: Search failed

        Args:
          q: Search query string

          limit: Maximum number of results

          threshold: Minimum similarity threshold (0-1)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/search/meetings/topic/semantic",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "q": q,
                        "limit": limit,
                        "threshold": threshold,
                    },
                    topic_search_semantic_params.TopicSearchSemanticParams,
                ),
            ),
            cast_to=TopicSearchSemanticResponse,
        )


class AsyncTopicResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTopicResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTopicResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTopicResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return AsyncTopicResourceWithStreamingResponse(self)

    async def search(
        self,
        *,
        q: str,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        sort_by: Optional[MeetingSortField] | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TopicSearchResponse:
        """
        Search meetings by topic using exact keyword matching.

        Traditional keyword search that finds meetings where the topic contains your
        search term. Fast and precise for exact text matching.

        **Authentication:** Required

        **Search Method:**

        - Case-insensitive substring matching
        - Searches the topic field only
        - Exact text matching (not semantic)

        **Query Parameters:**

        - `q`: Search term (required)
          - Example: "trade" → matches "International Trade Summit"
          - Example: "合作" → matches topics with "合作" in Chinese
        - `limit`: Maximum results (1-100, default: 10)
        - `offset`: Skip first N results for pagination (default: 0)

        **Response:** Returns list of MeetingDetails with full information including
        participants, organizations, locations, and sources.

        **When to Use:**

        - When you know the exact topic keywords
        - For precise, predictable matching
        - When you need fast results

        **Comparison with Semantic Search:**

        - Keyword: Fast, exact matching, requires correct wording
        - Semantic: Slower, finds conceptually similar topics, handles paraphrasing

        **Example:**

        ```
        GET /search/meetings/topic?q=economic&limit=10&offset=0
        ```

        **Response Codes:**

        - 200: Success
        - 401: Unauthorized

        Args:
          q: Search query string

          limit: Maximum number of results

          offset: Offset for pagination

          sort_by: Fields available for sorting meetings

          sort_order: Sort order

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/search/meetings/topic",
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

    async def search_semantic(
        self,
        *,
        q: str,
        limit: int | Omit = omit,
        threshold: float | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TopicSearchSemanticResponse:
        """
        Search meetings by topic using AI-powered semantic similarity.

        This endpoint uses advanced natural language understanding to find meetings
        based on topic similarity rather than exact keyword matches. Perfect for
        discovering related meetings even when they use different terminology.

        **Authentication:** Required

        **How It Works:**

        1. Your search query is converted to a semantic vector (embedding)
        2. Meeting topics are matched based on conceptual similarity
        3. Results are ranked by relevance score

        **Query Parameters:**

        - `q`: Your search query (required)
          - Example: "trade negotiations"
          - Example: "climate change policy"
          - Works with Chinese: "经济合作"
        - `limit`: Maximum results to return (1-100, default: 10)
        - `threshold`: Minimum similarity score 0-1 (default: 0.5)
          - Lower (0.3-0.5): More results, broader matches
          - Higher (0.6-0.8): Fewer results, more precise matches

        **Response Fields:**

        - All meeting details (id, topic, summary, participants, organizations, etc.)
        - `similarity`: Relevance score (0-1), higher = more relevant

        **Example Request:**

        ```
        GET /search/meetings/topic/semantic?q=economic%20cooperation&limit=5&threshold=0.6
        ```

        **Example Response:**

        ```json
        [
          {
            "id": "uuid",
            "topic": "Regional Economic Partnership",
            "summary": "Discussion on trade agreements...",
            "similarity": 0.87,
            "participants": [...],
            "organizations": [...]
          }
        ]
        ```

        **Tips:**

        - Use natural language queries for best results
        - Works across Chinese and English
        - Finds conceptually similar content even with different wording
        - Much faster than keyword search on large datasets

        **Response Codes:**

        - 200: Success
        - 400: Invalid query (empty text)
        - 401: Unauthorized
        - 500: Search failed

        Args:
          q: Search query string

          limit: Maximum number of results

          threshold: Minimum similarity threshold (0-1)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/search/meetings/topic/semantic",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "q": q,
                        "limit": limit,
                        "threshold": threshold,
                    },
                    topic_search_semantic_params.TopicSearchSemanticParams,
                ),
            ),
            cast_to=TopicSearchSemanticResponse,
        )


class TopicResourceWithRawResponse:
    def __init__(self, topic: TopicResource) -> None:
        self._topic = topic

        self.search = to_raw_response_wrapper(
            topic.search,
        )
        self.search_semantic = to_raw_response_wrapper(
            topic.search_semantic,
        )


class AsyncTopicResourceWithRawResponse:
    def __init__(self, topic: AsyncTopicResource) -> None:
        self._topic = topic

        self.search = async_to_raw_response_wrapper(
            topic.search,
        )
        self.search_semantic = async_to_raw_response_wrapper(
            topic.search_semantic,
        )


class TopicResourceWithStreamingResponse:
    def __init__(self, topic: TopicResource) -> None:
        self._topic = topic

        self.search = to_streamed_response_wrapper(
            topic.search,
        )
        self.search_semantic = to_streamed_response_wrapper(
            topic.search_semantic,
        )


class AsyncTopicResourceWithStreamingResponse:
    def __init__(self, topic: AsyncTopicResource) -> None:
        self._topic = topic

        self.search = async_to_streamed_response_wrapper(
            topic.search,
        )
        self.search_semantic = async_to_streamed_response_wrapper(
            topic.search_semantic,
        )
