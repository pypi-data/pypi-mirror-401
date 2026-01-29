# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .html import (
    HTMLResource,
    AsyncHTMLResource,
    HTMLResourceWithRawResponse,
    AsyncHTMLResourceWithRawResponse,
    HTMLResourceWithStreamingResponse,
    AsyncHTMLResourceWithStreamingResponse,
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
from ....types.search import document_search_markdown_params, document_search_semantic_params
from ....types.search.document_search_markdown_response import DocumentSearchMarkdownResponse
from ....types.search.document_search_semantic_response import DocumentSearchSemanticResponse

__all__ = ["DocumentsResource", "AsyncDocumentsResource"]


class DocumentsResource(SyncAPIResource):
    @cached_property
    def html(self) -> HTMLResource:
        return HTMLResource(self._client)

    @cached_property
    def with_raw_response(self) -> DocumentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return DocumentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DocumentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return DocumentsResourceWithStreamingResponse(self)

    def search_markdown(
        self,
        *,
        q: str,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DocumentSearchMarkdownResponse:
        """
        Search markdown documents by content using exact keyword matching.

        Traditional keyword search that finds documents where the markdown content
        contains your search term. Works with Chinese and English text.

        **Authentication:** Required

        **Search Method:**

        - Case-insensitive substring matching (LIKE query)
        - Searches the full markdown content
        - Exact text matching (not semantic)

        **Query Parameters:**

        - `q`: Search term (required)
          - Example: "climate policy" → matches documents containing this phrase
          - Example: "环境保护" → matches documents with "环境保护" in Chinese
        - `limit`: Maximum results (1-100, default: 10)
        - `offset`: Skip first N results for pagination (default: 0)

        **Response:** Returns list of DocumentSearchResult with URL, markdown content,
        and matching snippet.

        **When to Use:**

        - When you know exact phrases or terms
        - For precise text matching
        - When you need specific terminology

        **Performance Notes:**

        - May be slower on large datasets (full-table scan)
        - Very broad searches may timeout
        - For better performance, use semantic search

        **Comparison with Semantic Search:**

        - Keyword: Fast for specific terms, may timeout on broad searches
        - Semantic: Optimized for large datasets, finds conceptual matches

        **Example:**

        ```
        GET /search/documents/markdown?q=trade%20agreement&limit=10&offset=0
        ```

        **Error Handling:**

        - 504: Query timeout (search too broad) - try more specific terms
        - 500: Database error

        **Recommendation:** For large document searches or conceptual queries, use
        `/search/documents/semantic` for better performance and results.

        Args:
          q: Search query string

          limit: Maximum number of results

          offset: Offset for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/search/documents/markdown",
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
                    },
                    document_search_markdown_params.DocumentSearchMarkdownParams,
                ),
            ),
            cast_to=DocumentSearchMarkdownResponse,
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
    ) -> DocumentSearchSemanticResponse:
        """
        Search documents using AI-powered semantic similarity.

        This endpoint uses advanced natural language understanding to find documents
        based on meaning rather than exact keyword matches. It's optimized for both
        Chinese and English text.

        **Authentication:** Required

        **How It Works:**

        1. Your search query is converted to a semantic vector (embedding)
        2. Documents are matched based on conceptual similarity
        3. Results are ranked by relevance score

        **Query Parameters:**

        - `q`: Your search query (required)
          - Example: "economic development policies"
          - Example: "气候变化讨论"
        - `limit`: Maximum results to return (1-100, default: 10)
        - `threshold`: Minimum similarity score 0-1 (default: 0.5)
          - Lower threshold (0.3-0.5): More results, less precise
          - Higher threshold (0.6-0.8): Fewer results, more precise

        **Response Fields:**

        - `url`: Document URL
        - `markdown`: Document content
        - `similarity`: Relevance score (0-1)

        **Example Request:**

        ```
        GET /search/documents/semantic?q=climate%20policy&limit=5&threshold=0.6
        ```

        **Example Response:**

        ```json
        [
          {
            "url": "https://example.com/doc1",
            "markdown": "Document content...",
            "similarity": 0.85
          }
        ]
        ```

        **Tips:**

        - Use natural language queries for best results
        - Works with Chinese, English, and mixed-language queries
        - Finds conceptually similar content even with different wording
        - Much faster than keyword search for large datasets

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
            "/search/documents/semantic",
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
                    document_search_semantic_params.DocumentSearchSemanticParams,
                ),
            ),
            cast_to=DocumentSearchSemanticResponse,
        )


class AsyncDocumentsResource(AsyncAPIResource):
    @cached_property
    def html(self) -> AsyncHTMLResource:
        return AsyncHTMLResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncDocumentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDocumentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDocumentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return AsyncDocumentsResourceWithStreamingResponse(self)

    async def search_markdown(
        self,
        *,
        q: str,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DocumentSearchMarkdownResponse:
        """
        Search markdown documents by content using exact keyword matching.

        Traditional keyword search that finds documents where the markdown content
        contains your search term. Works with Chinese and English text.

        **Authentication:** Required

        **Search Method:**

        - Case-insensitive substring matching (LIKE query)
        - Searches the full markdown content
        - Exact text matching (not semantic)

        **Query Parameters:**

        - `q`: Search term (required)
          - Example: "climate policy" → matches documents containing this phrase
          - Example: "环境保护" → matches documents with "环境保护" in Chinese
        - `limit`: Maximum results (1-100, default: 10)
        - `offset`: Skip first N results for pagination (default: 0)

        **Response:** Returns list of DocumentSearchResult with URL, markdown content,
        and matching snippet.

        **When to Use:**

        - When you know exact phrases or terms
        - For precise text matching
        - When you need specific terminology

        **Performance Notes:**

        - May be slower on large datasets (full-table scan)
        - Very broad searches may timeout
        - For better performance, use semantic search

        **Comparison with Semantic Search:**

        - Keyword: Fast for specific terms, may timeout on broad searches
        - Semantic: Optimized for large datasets, finds conceptual matches

        **Example:**

        ```
        GET /search/documents/markdown?q=trade%20agreement&limit=10&offset=0
        ```

        **Error Handling:**

        - 504: Query timeout (search too broad) - try more specific terms
        - 500: Database error

        **Recommendation:** For large document searches or conceptual queries, use
        `/search/documents/semantic` for better performance and results.

        Args:
          q: Search query string

          limit: Maximum number of results

          offset: Offset for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/search/documents/markdown",
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
                    },
                    document_search_markdown_params.DocumentSearchMarkdownParams,
                ),
            ),
            cast_to=DocumentSearchMarkdownResponse,
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
    ) -> DocumentSearchSemanticResponse:
        """
        Search documents using AI-powered semantic similarity.

        This endpoint uses advanced natural language understanding to find documents
        based on meaning rather than exact keyword matches. It's optimized for both
        Chinese and English text.

        **Authentication:** Required

        **How It Works:**

        1. Your search query is converted to a semantic vector (embedding)
        2. Documents are matched based on conceptual similarity
        3. Results are ranked by relevance score

        **Query Parameters:**

        - `q`: Your search query (required)
          - Example: "economic development policies"
          - Example: "气候变化讨论"
        - `limit`: Maximum results to return (1-100, default: 10)
        - `threshold`: Minimum similarity score 0-1 (default: 0.5)
          - Lower threshold (0.3-0.5): More results, less precise
          - Higher threshold (0.6-0.8): Fewer results, more precise

        **Response Fields:**

        - `url`: Document URL
        - `markdown`: Document content
        - `similarity`: Relevance score (0-1)

        **Example Request:**

        ```
        GET /search/documents/semantic?q=climate%20policy&limit=5&threshold=0.6
        ```

        **Example Response:**

        ```json
        [
          {
            "url": "https://example.com/doc1",
            "markdown": "Document content...",
            "similarity": 0.85
          }
        ]
        ```

        **Tips:**

        - Use natural language queries for best results
        - Works with Chinese, English, and mixed-language queries
        - Finds conceptually similar content even with different wording
        - Much faster than keyword search for large datasets

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
            "/search/documents/semantic",
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
                    document_search_semantic_params.DocumentSearchSemanticParams,
                ),
            ),
            cast_to=DocumentSearchSemanticResponse,
        )


class DocumentsResourceWithRawResponse:
    def __init__(self, documents: DocumentsResource) -> None:
        self._documents = documents

        self.search_markdown = to_raw_response_wrapper(
            documents.search_markdown,
        )
        self.search_semantic = to_raw_response_wrapper(
            documents.search_semantic,
        )

    @cached_property
    def html(self) -> HTMLResourceWithRawResponse:
        return HTMLResourceWithRawResponse(self._documents.html)


class AsyncDocumentsResourceWithRawResponse:
    def __init__(self, documents: AsyncDocumentsResource) -> None:
        self._documents = documents

        self.search_markdown = async_to_raw_response_wrapper(
            documents.search_markdown,
        )
        self.search_semantic = async_to_raw_response_wrapper(
            documents.search_semantic,
        )

    @cached_property
    def html(self) -> AsyncHTMLResourceWithRawResponse:
        return AsyncHTMLResourceWithRawResponse(self._documents.html)


class DocumentsResourceWithStreamingResponse:
    def __init__(self, documents: DocumentsResource) -> None:
        self._documents = documents

        self.search_markdown = to_streamed_response_wrapper(
            documents.search_markdown,
        )
        self.search_semantic = to_streamed_response_wrapper(
            documents.search_semantic,
        )

    @cached_property
    def html(self) -> HTMLResourceWithStreamingResponse:
        return HTMLResourceWithStreamingResponse(self._documents.html)


class AsyncDocumentsResourceWithStreamingResponse:
    def __init__(self, documents: AsyncDocumentsResource) -> None:
        self._documents = documents

        self.search_markdown = async_to_streamed_response_wrapper(
            documents.search_markdown,
        )
        self.search_semantic = async_to_streamed_response_wrapper(
            documents.search_semantic,
        )

    @cached_property
    def html(self) -> AsyncHTMLResourceWithStreamingResponse:
        return AsyncHTMLResourceWithStreamingResponse(self._documents.html)
