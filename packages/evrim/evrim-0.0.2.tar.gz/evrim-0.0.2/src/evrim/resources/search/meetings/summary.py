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
from ....types.search.meetings import summary_search_params, summary_search_semantic_params
from ....types.meeting_sort_field import MeetingSortField
from ....types.search.meetings.summary_search_response import SummarySearchResponse
from ....types.search.meetings.summary_search_semantic_response import SummarySearchSemanticResponse

__all__ = ["SummaryResource", "AsyncSummaryResource"]


class SummaryResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SummaryResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return SummaryResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SummaryResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return SummaryResourceWithStreamingResponse(self)

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
    ) -> SummarySearchResponse:
        """
        Search meetings by summary content using exact keyword matching.

        Traditional keyword search that finds meetings where the summary contains your
        search term. Searches the detailed meeting summary text.

        **Authentication:** Required

        **Search Method:**

        - Case-insensitive substring matching
        - Searches the summary field only
        - Exact text matching (not semantic)

        **Query Parameters:**

        - `q`: Search term (required)
          - Example: "infrastructure" → matches summaries mentioning infrastructure
          - Example: "协议" → matches summaries with "协议" in Chinese
        - `limit`: Maximum results (1-100, default: 10)
        - `offset`: Skip first N results for pagination (default: 0)

        **Response:** Returns list of MeetingDetails with complete information including
        participants, organizations, locations, and sources.

        **When to Use:**

        - When you know specific phrases or terms in the summary
        - For exact text matching in meeting content
        - When you need fast, predictable results

        **Comparison with Semantic Search:**

        - Keyword: Fast, exact matching, finds specific phrases
        - Semantic: Slower, finds conceptually similar content, understands meaning

        **Example:**

        ```
        GET /search/meetings/summary?q=policy%20discussion&limit=10&offset=0
        ```

        **Tips:**

        - Summaries contain more detail than topics
        - Use specific terms for better results
        - Combine with topic search for comprehensive discovery

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
            "/search/meetings/summary",
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
                    summary_search_params.SummarySearchParams,
                ),
            ),
            cast_to=SummarySearchResponse,
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
    ) -> SummarySearchSemanticResponse:
        """
        Search meetings by summary content using AI-powered semantic similarity.

        This endpoint searches through meeting summaries using natural language
        understanding to find conceptually related meetings, even when different words
        are used. Perfect for discovering meetings by their detailed content.

        **Authentication:** Required

        **How It Works:**

        1. Your search query is converted to a semantic vector (embedding)
        2. Meeting summaries are matched based on conceptual meaning
        3. Results are ranked by relevance score

        **Query Parameters:**

        - `q`: Your search query (required)
          - Example: "discussions about technology transfer"
          - Example: "infrastructure development plans"
          - Works with Chinese: "技术转让讨论"
        - `limit`: Maximum results to return (1-100, default: 10)
        - `threshold`: Minimum similarity score 0-1 (default: 0.5)
          - Lower (0.3-0.5): Broader matches, more results
          - Higher (0.6-0.8): Precise matches, fewer results

        **Response Fields:**

        - Complete meeting details with participants, organizations, locations
        - `similarity`: Relevance score (0-1), higher = more relevant

        **Example Request:**

        ```
        GET /search/meetings/summary/semantic?q=infrastructure%20projects&limit=10&threshold=0.5
        ```

        **Example Response:**

        ```json
        [
          {
            "id": "uuid",
            "topic": "Infrastructure Development",
            "summary": "Detailed discussion of infrastructure projects...",
            "similarity": 0.82,
            "participants": [...],
            "organizations": [...]
          }
        ]
        ```

        **When to Use:**

        - Search by meeting content/outcomes rather than just topic
        - Find meetings with similar discussions or decisions
        - Discover related meetings across different terminology

        **Tips:**

        - Summaries contain more detail than topics, providing richer search results
        - Use descriptive queries for best results
        - Multilingual support for Chinese and English

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
            "/search/meetings/summary/semantic",
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
                    summary_search_semantic_params.SummarySearchSemanticParams,
                ),
            ),
            cast_to=SummarySearchSemanticResponse,
        )


class AsyncSummaryResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSummaryResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSummaryResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSummaryResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return AsyncSummaryResourceWithStreamingResponse(self)

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
    ) -> SummarySearchResponse:
        """
        Search meetings by summary content using exact keyword matching.

        Traditional keyword search that finds meetings where the summary contains your
        search term. Searches the detailed meeting summary text.

        **Authentication:** Required

        **Search Method:**

        - Case-insensitive substring matching
        - Searches the summary field only
        - Exact text matching (not semantic)

        **Query Parameters:**

        - `q`: Search term (required)
          - Example: "infrastructure" → matches summaries mentioning infrastructure
          - Example: "协议" → matches summaries with "协议" in Chinese
        - `limit`: Maximum results (1-100, default: 10)
        - `offset`: Skip first N results for pagination (default: 0)

        **Response:** Returns list of MeetingDetails with complete information including
        participants, organizations, locations, and sources.

        **When to Use:**

        - When you know specific phrases or terms in the summary
        - For exact text matching in meeting content
        - When you need fast, predictable results

        **Comparison with Semantic Search:**

        - Keyword: Fast, exact matching, finds specific phrases
        - Semantic: Slower, finds conceptually similar content, understands meaning

        **Example:**

        ```
        GET /search/meetings/summary?q=policy%20discussion&limit=10&offset=0
        ```

        **Tips:**

        - Summaries contain more detail than topics
        - Use specific terms for better results
        - Combine with topic search for comprehensive discovery

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
            "/search/meetings/summary",
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
                    summary_search_params.SummarySearchParams,
                ),
            ),
            cast_to=SummarySearchResponse,
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
    ) -> SummarySearchSemanticResponse:
        """
        Search meetings by summary content using AI-powered semantic similarity.

        This endpoint searches through meeting summaries using natural language
        understanding to find conceptually related meetings, even when different words
        are used. Perfect for discovering meetings by their detailed content.

        **Authentication:** Required

        **How It Works:**

        1. Your search query is converted to a semantic vector (embedding)
        2. Meeting summaries are matched based on conceptual meaning
        3. Results are ranked by relevance score

        **Query Parameters:**

        - `q`: Your search query (required)
          - Example: "discussions about technology transfer"
          - Example: "infrastructure development plans"
          - Works with Chinese: "技术转让讨论"
        - `limit`: Maximum results to return (1-100, default: 10)
        - `threshold`: Minimum similarity score 0-1 (default: 0.5)
          - Lower (0.3-0.5): Broader matches, more results
          - Higher (0.6-0.8): Precise matches, fewer results

        **Response Fields:**

        - Complete meeting details with participants, organizations, locations
        - `similarity`: Relevance score (0-1), higher = more relevant

        **Example Request:**

        ```
        GET /search/meetings/summary/semantic?q=infrastructure%20projects&limit=10&threshold=0.5
        ```

        **Example Response:**

        ```json
        [
          {
            "id": "uuid",
            "topic": "Infrastructure Development",
            "summary": "Detailed discussion of infrastructure projects...",
            "similarity": 0.82,
            "participants": [...],
            "organizations": [...]
          }
        ]
        ```

        **When to Use:**

        - Search by meeting content/outcomes rather than just topic
        - Find meetings with similar discussions or decisions
        - Discover related meetings across different terminology

        **Tips:**

        - Summaries contain more detail than topics, providing richer search results
        - Use descriptive queries for best results
        - Multilingual support for Chinese and English

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
            "/search/meetings/summary/semantic",
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
                    summary_search_semantic_params.SummarySearchSemanticParams,
                ),
            ),
            cast_to=SummarySearchSemanticResponse,
        )


class SummaryResourceWithRawResponse:
    def __init__(self, summary: SummaryResource) -> None:
        self._summary = summary

        self.search = to_raw_response_wrapper(
            summary.search,
        )
        self.search_semantic = to_raw_response_wrapper(
            summary.search_semantic,
        )


class AsyncSummaryResourceWithRawResponse:
    def __init__(self, summary: AsyncSummaryResource) -> None:
        self._summary = summary

        self.search = async_to_raw_response_wrapper(
            summary.search,
        )
        self.search_semantic = async_to_raw_response_wrapper(
            summary.search_semantic,
        )


class SummaryResourceWithStreamingResponse:
    def __init__(self, summary: SummaryResource) -> None:
        self._summary = summary

        self.search = to_streamed_response_wrapper(
            summary.search,
        )
        self.search_semantic = to_streamed_response_wrapper(
            summary.search_semantic,
        )


class AsyncSummaryResourceWithStreamingResponse:
    def __init__(self, summary: AsyncSummaryResource) -> None:
        self._summary = summary

        self.search = async_to_streamed_response_wrapper(
            summary.search,
        )
        self.search_semantic = async_to_streamed_response_wrapper(
            summary.search_semantic,
        )
