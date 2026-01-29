# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ...types import SortOrder, ParticipantSortField
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
from ...types.search import participant_search_params, participant_search_semantic_params
from ...types.sort_order import SortOrder
from ...types.participant_sort_field import ParticipantSortField
from ...types.search.participant_search_response import ParticipantSearchResponse
from ...types.search.participant_search_semantic_response import ParticipantSearchSemanticResponse

__all__ = ["ParticipantsResource", "AsyncParticipantsResource"]


class ParticipantsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ParticipantsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return ParticipantsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ParticipantsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return ParticipantsResourceWithStreamingResponse(self)

    def search(
        self,
        *,
        q: str,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        sort_by: Optional[ParticipantSortField] | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ParticipantSearchResponse:
        """
        Search participants by name using exact keyword matching.

        Traditional keyword search that finds participants where the name contains your
        search term. Searches both Chinese and English name fields.

        **Authentication:** Required

        **Search Method:**

        - Case-insensitive substring matching
        - Searches Chinese names array and English name field
        - Exact text matching (not semantic)

        **Query Parameters:**

        - `q`: Search term (required)
          - Example: "Wang" → matches "Wang Yi", "Wang Wei", etc.
          - Example: "王" → matches participants with "王" in Chinese name
        - `limit`: Maximum results (1-100, default: 10)
        - `offset`: Skip first N results for pagination (default: 0)

        **Response:** Returns list of participants with names, roles, affiliations,
        countries, and meeting counts.

        **When to Use:**

        - When you know the exact name or part of it
        - For precise text matching
        - When you need fast, predictable results

        **Comparison with Semantic Search:**

        - Keyword: Fast, exact matching, requires correct spelling
        - Semantic: Slower, handles variations and romanizations, finds similar names

        **Example:**

        ```
        GET /search/participants?q=minister&limit=20&offset=0&sort_by=name&sort_order=asc
        ```

        **Response Codes:**

        - 200: Success
        - 401: Unauthorized

        Args:
          q: Search query string

          limit: Maximum number of results

          offset: Offset for pagination

          sort_by: Fields available for sorting participants

          sort_order: Sort order

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/search/participants",
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
                    participant_search_params.ParticipantSearchParams,
                ),
            ),
            cast_to=ParticipantSearchResponse,
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
    ) -> ParticipantSearchSemanticResponse:
        """
        Search participants by name using AI-powered semantic similarity.

        This endpoint uses natural language understanding to find individuals by name,
        handling name variations, translations, transliterations, and alternative
        spellings much better than exact keyword matching.

        **Authentication:** Required

        **How It Works:**

        1. Your search query is converted to a semantic vector (embedding)
        2. Participant names are matched based on phonetic and semantic similarity
        3. Handles Chinese/English name variations automatically
        4. Returns participants ranked by relevance

        **Query Parameters:**

        - `q`: Participant name or partial name (required)
          - Example: "Wang Wei"
          - Example: "王伟" (finds Chinese and romanized variants)
          - Example: "Foreign Minister"
        - `limit`: Maximum results to return (1-100, default: 10)
        - `threshold`: Minimum similarity score 0-1 (default: 0.5)
          - Lower (0.3-0.5): Find more name variations
          - Higher (0.6-0.8): More exact name matches

        **Response Fields:**

        - Names in multiple languages
        - Roles and positions
        - Affiliations and organizations
        - Associated countries
        - Meeting participation count
        - `similarity`: Relevance score (0-1)

        **Example Request:**

        ```
        GET /search/participants/semantic?q=foreign%20minister&limit=5&threshold=0.6
        ```

        **Example Response:**

        ```json
        [
          {
            "id": "uuid",
            "names": ["王毅"],
            "name_english": "Wang Yi",
            "roles": ["Foreign Minister"],
            "affiliations": ["Ministry of Foreign Affairs"],
            "countries": ["China"],
            "meeting_count": 32,
            "similarity": 0.85
          }
        ]
        ```

        **Advantages Over Keyword Search:**

        - Finds people with different name romanizations
        - Handles Chinese/English name variations
        - Discovers participants by role or title
        - Works with partial names or descriptions

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
            "/search/participants/semantic",
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
                    participant_search_semantic_params.ParticipantSearchSemanticParams,
                ),
            ),
            cast_to=ParticipantSearchSemanticResponse,
        )


class AsyncParticipantsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncParticipantsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return AsyncParticipantsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncParticipantsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return AsyncParticipantsResourceWithStreamingResponse(self)

    async def search(
        self,
        *,
        q: str,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        sort_by: Optional[ParticipantSortField] | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ParticipantSearchResponse:
        """
        Search participants by name using exact keyword matching.

        Traditional keyword search that finds participants where the name contains your
        search term. Searches both Chinese and English name fields.

        **Authentication:** Required

        **Search Method:**

        - Case-insensitive substring matching
        - Searches Chinese names array and English name field
        - Exact text matching (not semantic)

        **Query Parameters:**

        - `q`: Search term (required)
          - Example: "Wang" → matches "Wang Yi", "Wang Wei", etc.
          - Example: "王" → matches participants with "王" in Chinese name
        - `limit`: Maximum results (1-100, default: 10)
        - `offset`: Skip first N results for pagination (default: 0)

        **Response:** Returns list of participants with names, roles, affiliations,
        countries, and meeting counts.

        **When to Use:**

        - When you know the exact name or part of it
        - For precise text matching
        - When you need fast, predictable results

        **Comparison with Semantic Search:**

        - Keyword: Fast, exact matching, requires correct spelling
        - Semantic: Slower, handles variations and romanizations, finds similar names

        **Example:**

        ```
        GET /search/participants?q=minister&limit=20&offset=0&sort_by=name&sort_order=asc
        ```

        **Response Codes:**

        - 200: Success
        - 401: Unauthorized

        Args:
          q: Search query string

          limit: Maximum number of results

          offset: Offset for pagination

          sort_by: Fields available for sorting participants

          sort_order: Sort order

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/search/participants",
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
                    participant_search_params.ParticipantSearchParams,
                ),
            ),
            cast_to=ParticipantSearchResponse,
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
    ) -> ParticipantSearchSemanticResponse:
        """
        Search participants by name using AI-powered semantic similarity.

        This endpoint uses natural language understanding to find individuals by name,
        handling name variations, translations, transliterations, and alternative
        spellings much better than exact keyword matching.

        **Authentication:** Required

        **How It Works:**

        1. Your search query is converted to a semantic vector (embedding)
        2. Participant names are matched based on phonetic and semantic similarity
        3. Handles Chinese/English name variations automatically
        4. Returns participants ranked by relevance

        **Query Parameters:**

        - `q`: Participant name or partial name (required)
          - Example: "Wang Wei"
          - Example: "王伟" (finds Chinese and romanized variants)
          - Example: "Foreign Minister"
        - `limit`: Maximum results to return (1-100, default: 10)
        - `threshold`: Minimum similarity score 0-1 (default: 0.5)
          - Lower (0.3-0.5): Find more name variations
          - Higher (0.6-0.8): More exact name matches

        **Response Fields:**

        - Names in multiple languages
        - Roles and positions
        - Affiliations and organizations
        - Associated countries
        - Meeting participation count
        - `similarity`: Relevance score (0-1)

        **Example Request:**

        ```
        GET /search/participants/semantic?q=foreign%20minister&limit=5&threshold=0.6
        ```

        **Example Response:**

        ```json
        [
          {
            "id": "uuid",
            "names": ["王毅"],
            "name_english": "Wang Yi",
            "roles": ["Foreign Minister"],
            "affiliations": ["Ministry of Foreign Affairs"],
            "countries": ["China"],
            "meeting_count": 32,
            "similarity": 0.85
          }
        ]
        ```

        **Advantages Over Keyword Search:**

        - Finds people with different name romanizations
        - Handles Chinese/English name variations
        - Discovers participants by role or title
        - Works with partial names or descriptions

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
            "/search/participants/semantic",
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
                    participant_search_semantic_params.ParticipantSearchSemanticParams,
                ),
            ),
            cast_to=ParticipantSearchSemanticResponse,
        )


class ParticipantsResourceWithRawResponse:
    def __init__(self, participants: ParticipantsResource) -> None:
        self._participants = participants

        self.search = to_raw_response_wrapper(
            participants.search,
        )
        self.search_semantic = to_raw_response_wrapper(
            participants.search_semantic,
        )


class AsyncParticipantsResourceWithRawResponse:
    def __init__(self, participants: AsyncParticipantsResource) -> None:
        self._participants = participants

        self.search = async_to_raw_response_wrapper(
            participants.search,
        )
        self.search_semantic = async_to_raw_response_wrapper(
            participants.search_semantic,
        )


class ParticipantsResourceWithStreamingResponse:
    def __init__(self, participants: ParticipantsResource) -> None:
        self._participants = participants

        self.search = to_streamed_response_wrapper(
            participants.search,
        )
        self.search_semantic = to_streamed_response_wrapper(
            participants.search_semantic,
        )


class AsyncParticipantsResourceWithStreamingResponse:
    def __init__(self, participants: AsyncParticipantsResource) -> None:
        self._participants = participants

        self.search = async_to_streamed_response_wrapper(
            participants.search,
        )
        self.search_semantic = async_to_streamed_response_wrapper(
            participants.search_semantic,
        )
