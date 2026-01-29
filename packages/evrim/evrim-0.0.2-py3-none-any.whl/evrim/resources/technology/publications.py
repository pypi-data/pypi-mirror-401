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
from ...types.technology import PublicationSortField, publication_search_params, publication_get_topics_params
from ...types.technology.publication_sort_field import PublicationSortField
from ...types.technology.technology_publication import TechnologyPublication
from ...types.technology.publication_search_response import PublicationSearchResponse
from ...types.technology.publication_get_topics_response import PublicationGetTopicsResponse

__all__ = ["PublicationsResource", "AsyncPublicationsResource"]


class PublicationsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PublicationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return PublicationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PublicationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return PublicationsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        publication_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TechnologyPublication:
        """
        Get detailed information about a specific technology publication.

        **Publication Fields:**

        - id, title, authors[], abstract
        - journal, year, doi, source_url

        **Response Codes:**

        - 200: Success
        - 401: Unauthorized
        - 404: Publication not found

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not publication_id:
            raise ValueError(f"Expected a non-empty value for `publication_id` but received {publication_id!r}")
        return self._get(
            f"/technology/publications/{publication_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TechnologyPublication,
        )

    def get_topics(
        self,
        publication_id: str,
        *,
        limit: int | Omit = omit,
        min_similarity: float | Omit = omit,
        offset: int | Omit = omit,
        sort_by: str | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PublicationGetTopicsResponse:
        """
        Get all topics matched to a publication with similarity scores.

        Returns topics that are semantically similar to the publication based on the
        publication-topic edge table. Each result includes the matched subarea and
        similarity score.

        **Query Parameters:**

        - min_similarity: Filter by minimum similarity (0.0-1.0)
        - limit: Maximum number of results (1-100)
        - offset: Pagination offset
        - sort_by: Sort by 'similarity' or 'name'
        - sort_order: 'asc' or 'desc'

        **Response Fields:**

        - topic_id, topic_name, topic_description
        - matched_subarea: The subarea that matched
        - similarity: Similarity score (0-1)
        - sub_areas: All subareas for this topic

        **Response Codes:**

        - 200: Success (empty list if no matches)
        - 401: Unauthorized

        Args:
          limit: Maximum results

          min_similarity: Minimum similarity score (0-1)

          offset: Pagination offset

          sort_by: Sort field: similarity or name

          sort_order: Sort order

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not publication_id:
            raise ValueError(f"Expected a non-empty value for `publication_id` but received {publication_id!r}")
        return self._get(
            f"/technology/publications/{publication_id}/topics",
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
                    },
                    publication_get_topics_params.PublicationGetTopicsParams,
                ),
            ),
            cast_to=PublicationGetTopicsResponse,
        )

    def search(
        self,
        *,
        q: str,
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
    ) -> PublicationSearchResponse:
        """
        Keyword search for technology publications.

        **Search Method:**

        - Full-text search on title and abstract (ILIKE)
        - Case-insensitive pattern matching

        **Query Parameters:**

        - `q`: Search query (required)
        - `limit`: Maximum results
        - `offset`: Pagination offset
        - `sort_by`: Sort field (year, title)
        - `sort_order`: Sort order (desc by default)
        - `year_min`, `year_max`: Filter by publication year range

        **Response Codes:**

        - 200: Success
        - 400: Invalid parameters
        - 401: Unauthorized

        Args:
          q: Search query

          limit: Maximum number of results

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
        return self._get(
            "/technology/publications/search",
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
                        "year_max": year_max,
                        "year_min": year_min,
                    },
                    publication_search_params.PublicationSearchParams,
                ),
            ),
            cast_to=PublicationSearchResponse,
        )


class AsyncPublicationsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPublicationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPublicationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPublicationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return AsyncPublicationsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        publication_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TechnologyPublication:
        """
        Get detailed information about a specific technology publication.

        **Publication Fields:**

        - id, title, authors[], abstract
        - journal, year, doi, source_url

        **Response Codes:**

        - 200: Success
        - 401: Unauthorized
        - 404: Publication not found

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not publication_id:
            raise ValueError(f"Expected a non-empty value for `publication_id` but received {publication_id!r}")
        return await self._get(
            f"/technology/publications/{publication_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TechnologyPublication,
        )

    async def get_topics(
        self,
        publication_id: str,
        *,
        limit: int | Omit = omit,
        min_similarity: float | Omit = omit,
        offset: int | Omit = omit,
        sort_by: str | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PublicationGetTopicsResponse:
        """
        Get all topics matched to a publication with similarity scores.

        Returns topics that are semantically similar to the publication based on the
        publication-topic edge table. Each result includes the matched subarea and
        similarity score.

        **Query Parameters:**

        - min_similarity: Filter by minimum similarity (0.0-1.0)
        - limit: Maximum number of results (1-100)
        - offset: Pagination offset
        - sort_by: Sort by 'similarity' or 'name'
        - sort_order: 'asc' or 'desc'

        **Response Fields:**

        - topic_id, topic_name, topic_description
        - matched_subarea: The subarea that matched
        - similarity: Similarity score (0-1)
        - sub_areas: All subareas for this topic

        **Response Codes:**

        - 200: Success (empty list if no matches)
        - 401: Unauthorized

        Args:
          limit: Maximum results

          min_similarity: Minimum similarity score (0-1)

          offset: Pagination offset

          sort_by: Sort field: similarity or name

          sort_order: Sort order

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not publication_id:
            raise ValueError(f"Expected a non-empty value for `publication_id` but received {publication_id!r}")
        return await self._get(
            f"/technology/publications/{publication_id}/topics",
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
                    },
                    publication_get_topics_params.PublicationGetTopicsParams,
                ),
            ),
            cast_to=PublicationGetTopicsResponse,
        )

    async def search(
        self,
        *,
        q: str,
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
    ) -> PublicationSearchResponse:
        """
        Keyword search for technology publications.

        **Search Method:**

        - Full-text search on title and abstract (ILIKE)
        - Case-insensitive pattern matching

        **Query Parameters:**

        - `q`: Search query (required)
        - `limit`: Maximum results
        - `offset`: Pagination offset
        - `sort_by`: Sort field (year, title)
        - `sort_order`: Sort order (desc by default)
        - `year_min`, `year_max`: Filter by publication year range

        **Response Codes:**

        - 200: Success
        - 400: Invalid parameters
        - 401: Unauthorized

        Args:
          q: Search query

          limit: Maximum number of results

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
        return await self._get(
            "/technology/publications/search",
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
                        "year_max": year_max,
                        "year_min": year_min,
                    },
                    publication_search_params.PublicationSearchParams,
                ),
            ),
            cast_to=PublicationSearchResponse,
        )


class PublicationsResourceWithRawResponse:
    def __init__(self, publications: PublicationsResource) -> None:
        self._publications = publications

        self.retrieve = to_raw_response_wrapper(
            publications.retrieve,
        )
        self.get_topics = to_raw_response_wrapper(
            publications.get_topics,
        )
        self.search = to_raw_response_wrapper(
            publications.search,
        )


class AsyncPublicationsResourceWithRawResponse:
    def __init__(self, publications: AsyncPublicationsResource) -> None:
        self._publications = publications

        self.retrieve = async_to_raw_response_wrapper(
            publications.retrieve,
        )
        self.get_topics = async_to_raw_response_wrapper(
            publications.get_topics,
        )
        self.search = async_to_raw_response_wrapper(
            publications.search,
        )


class PublicationsResourceWithStreamingResponse:
    def __init__(self, publications: PublicationsResource) -> None:
        self._publications = publications

        self.retrieve = to_streamed_response_wrapper(
            publications.retrieve,
        )
        self.get_topics = to_streamed_response_wrapper(
            publications.get_topics,
        )
        self.search = to_streamed_response_wrapper(
            publications.search,
        )


class AsyncPublicationsResourceWithStreamingResponse:
    def __init__(self, publications: AsyncPublicationsResource) -> None:
        self._publications = publications

        self.retrieve = async_to_streamed_response_wrapper(
            publications.retrieve,
        )
        self.get_topics = async_to_streamed_response_wrapper(
            publications.get_topics,
        )
        self.search = async_to_streamed_response_wrapper(
            publications.search,
        )
