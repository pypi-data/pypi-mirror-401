# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ...types import SortOrder, OrganizationSortField
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
from ...types.search import organization_search_params, organization_search_semantic_params
from ...types.sort_order import SortOrder
from ...types.organization_sort_field import OrganizationSortField
from ...types.search.organization_search_response import OrganizationSearchResponse
from ...types.search.organization_search_semantic_response import OrganizationSearchSemanticResponse

__all__ = ["OrganizationsResource", "AsyncOrganizationsResource"]


class OrganizationsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> OrganizationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return OrganizationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> OrganizationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return OrganizationsResourceWithStreamingResponse(self)

    def search(
        self,
        *,
        q: str,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        sort_by: Optional[OrganizationSortField] | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrganizationSearchResponse:
        """
        Search organizations by name using exact keyword matching.

        Traditional keyword search that finds organizations where the name contains your
        search term. Searches both Chinese and English name fields.

        **Authentication:** Required

        **Search Method:**

        - Case-insensitive substring matching
        - Searches Chinese names array and English name field
        - Exact text matching (not semantic)

        **Query Parameters:**

        - `q`: Search term (required)
          - Example: "Commerce" → matches "Ministry of Commerce"
          - Example: "商务" → matches organizations with "商务" in Chinese name
        - `limit`: Maximum results (1-100, default: 10)
        - `offset`: Skip first N results for pagination (default: 0)

        **Response:** Returns list of organizations with names, types, countries, and
        meeting counts.

        **When to Use:**

        - When you know the exact name or part of it
        - For precise text matching
        - When semantic search returns too many results

        **Comparison with Semantic Search:**

        - Keyword: Fast, exact matching, requires knowing exact wording
        - Semantic: Slower, finds similar concepts, handles variations

        **Example:**

        ```
        GET /search/organizations?q=ministry&limit=20&offset=0&sort_by=name&sort_order=asc
        ```

        **Response Codes:**

        - 200: Success
        - 401: Unauthorized

        Args:
          q: Search query string

          limit: Maximum number of results

          offset: Offset for pagination

          sort_by: Fields available for sorting organizations

          sort_order: Sort order

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/search/organizations",
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
                    organization_search_params.OrganizationSearchParams,
                ),
            ),
            cast_to=OrganizationSearchResponse,
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
    ) -> OrganizationSearchSemanticResponse:
        """
        Search organizations by name using AI-powered semantic similarity.

        This endpoint uses natural language understanding to find organizations by name,
        handling variations, translations, abbreviations, and alternative names much
        better than exact keyword matching.

        **Authentication:** Required

        **How It Works:**

        1. Your search query is converted to a semantic vector (embedding)
        2. Organization names are matched based on meaning and similarity
        3. Results handle Chinese/English translations automatically
        4. Returns organizations ranked by relevance

        **Query Parameters:**

        - `q`: Organization name or description (required)
          - Example: "Ministry of Commerce"
          - Example: "商务部" (finds Chinese and English variants)
          - Example: "trade ministry"
        - `limit`: Maximum results to return (1-100, default: 10)
        - `threshold`: Minimum similarity score 0-1 (default: 0.5)
          - Lower (0.3-0.5): Find more variants and related organizations
          - Higher (0.6-0.8): More exact name matches

        **Response Fields:**

        - Organization names (Chinese and English)
        - Organization types
        - Associated countries
        - Meeting count
        - `similarity`: Relevance score (0-1)

        **Example Request:**

        ```
        GET /search/organizations/semantic?q=commerce%20ministry&limit=5&threshold=0.6
        ```

        **Example Response:**

        ```json
        [
          {
            "id": "uuid",
            "names": ["商务部"],
            "name_english": "Ministry of Commerce",
            "types": ["Government"],
            "countries": ["China"],
            "meeting_count": 45,
            "similarity": 0.89
          }
        ]
        ```

        **Advantages Over Keyword Search:**

        - Finds organizations even with different naming conventions
        - Handles translations and transliterations
        - Discovers abbreviations and alternative names
        - Works with partial or descriptive names

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
            "/search/organizations/semantic",
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
                    organization_search_semantic_params.OrganizationSearchSemanticParams,
                ),
            ),
            cast_to=OrganizationSearchSemanticResponse,
        )


class AsyncOrganizationsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncOrganizationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return AsyncOrganizationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOrganizationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return AsyncOrganizationsResourceWithStreamingResponse(self)

    async def search(
        self,
        *,
        q: str,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        sort_by: Optional[OrganizationSortField] | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrganizationSearchResponse:
        """
        Search organizations by name using exact keyword matching.

        Traditional keyword search that finds organizations where the name contains your
        search term. Searches both Chinese and English name fields.

        **Authentication:** Required

        **Search Method:**

        - Case-insensitive substring matching
        - Searches Chinese names array and English name field
        - Exact text matching (not semantic)

        **Query Parameters:**

        - `q`: Search term (required)
          - Example: "Commerce" → matches "Ministry of Commerce"
          - Example: "商务" → matches organizations with "商务" in Chinese name
        - `limit`: Maximum results (1-100, default: 10)
        - `offset`: Skip first N results for pagination (default: 0)

        **Response:** Returns list of organizations with names, types, countries, and
        meeting counts.

        **When to Use:**

        - When you know the exact name or part of it
        - For precise text matching
        - When semantic search returns too many results

        **Comparison with Semantic Search:**

        - Keyword: Fast, exact matching, requires knowing exact wording
        - Semantic: Slower, finds similar concepts, handles variations

        **Example:**

        ```
        GET /search/organizations?q=ministry&limit=20&offset=0&sort_by=name&sort_order=asc
        ```

        **Response Codes:**

        - 200: Success
        - 401: Unauthorized

        Args:
          q: Search query string

          limit: Maximum number of results

          offset: Offset for pagination

          sort_by: Fields available for sorting organizations

          sort_order: Sort order

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/search/organizations",
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
                    organization_search_params.OrganizationSearchParams,
                ),
            ),
            cast_to=OrganizationSearchResponse,
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
    ) -> OrganizationSearchSemanticResponse:
        """
        Search organizations by name using AI-powered semantic similarity.

        This endpoint uses natural language understanding to find organizations by name,
        handling variations, translations, abbreviations, and alternative names much
        better than exact keyword matching.

        **Authentication:** Required

        **How It Works:**

        1. Your search query is converted to a semantic vector (embedding)
        2. Organization names are matched based on meaning and similarity
        3. Results handle Chinese/English translations automatically
        4. Returns organizations ranked by relevance

        **Query Parameters:**

        - `q`: Organization name or description (required)
          - Example: "Ministry of Commerce"
          - Example: "商务部" (finds Chinese and English variants)
          - Example: "trade ministry"
        - `limit`: Maximum results to return (1-100, default: 10)
        - `threshold`: Minimum similarity score 0-1 (default: 0.5)
          - Lower (0.3-0.5): Find more variants and related organizations
          - Higher (0.6-0.8): More exact name matches

        **Response Fields:**

        - Organization names (Chinese and English)
        - Organization types
        - Associated countries
        - Meeting count
        - `similarity`: Relevance score (0-1)

        **Example Request:**

        ```
        GET /search/organizations/semantic?q=commerce%20ministry&limit=5&threshold=0.6
        ```

        **Example Response:**

        ```json
        [
          {
            "id": "uuid",
            "names": ["商务部"],
            "name_english": "Ministry of Commerce",
            "types": ["Government"],
            "countries": ["China"],
            "meeting_count": 45,
            "similarity": 0.89
          }
        ]
        ```

        **Advantages Over Keyword Search:**

        - Finds organizations even with different naming conventions
        - Handles translations and transliterations
        - Discovers abbreviations and alternative names
        - Works with partial or descriptive names

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
            "/search/organizations/semantic",
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
                    organization_search_semantic_params.OrganizationSearchSemanticParams,
                ),
            ),
            cast_to=OrganizationSearchSemanticResponse,
        )


class OrganizationsResourceWithRawResponse:
    def __init__(self, organizations: OrganizationsResource) -> None:
        self._organizations = organizations

        self.search = to_raw_response_wrapper(
            organizations.search,
        )
        self.search_semantic = to_raw_response_wrapper(
            organizations.search_semantic,
        )


class AsyncOrganizationsResourceWithRawResponse:
    def __init__(self, organizations: AsyncOrganizationsResource) -> None:
        self._organizations = organizations

        self.search = async_to_raw_response_wrapper(
            organizations.search,
        )
        self.search_semantic = async_to_raw_response_wrapper(
            organizations.search_semantic,
        )


class OrganizationsResourceWithStreamingResponse:
    def __init__(self, organizations: OrganizationsResource) -> None:
        self._organizations = organizations

        self.search = to_streamed_response_wrapper(
            organizations.search,
        )
        self.search_semantic = to_streamed_response_wrapper(
            organizations.search_semantic,
        )


class AsyncOrganizationsResourceWithStreamingResponse:
    def __init__(self, organizations: AsyncOrganizationsResource) -> None:
        self._organizations = organizations

        self.search = async_to_streamed_response_wrapper(
            organizations.search,
        )
        self.search_semantic = async_to_streamed_response_wrapper(
            organizations.search_semantic,
        )
