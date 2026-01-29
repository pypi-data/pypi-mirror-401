# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

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
from ...types.phones import search_query_params, search_by_domain_params
from ...types.phones.search_query_response import SearchQueryResponse
from ...types.phones.search_by_domain_response import SearchByDomainResponse

__all__ = ["SearchResource", "AsyncSearchResource"]


class SearchResource(SyncAPIResource):
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

    def by_domain(
        self,
        *,
        domain: str,
        end: int | Omit = omit,
        start: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SearchByDomainResponse:
        """
        Search phones by domain in their source URLs array.

        Finds all phone numbers that were extracted from pages containing the specified
        domain in their source URLs.

        **Authentication:** Required

        **Query Parameters:**

        - `domain`: Domain name to search in source URLs (e.g., 'example.com')
        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)

        **Response:** Returns list of Phone objects where source URLs contain the
        domain.

        Args:
          domain: Domain to search in source URLs (e.g., 'example.com')

          end: End index for pagination

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/phones/search/source-domain",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "domain": domain,
                        "end": end,
                        "start": start,
                    },
                    search_by_domain_params.SearchByDomainParams,
                ),
            ),
            cast_to=SearchByDomainResponse,
        )

    def query(
        self,
        *,
        query: str,
        end: int | Omit = omit,
        start: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SearchQueryResponse:
        """
        Search phone numbers with partial match anywhere in the number.

        Finds phone numbers that contain the search query anywhere in the number.

        **Authentication:** Required

        **Query Parameters:**

        - `query`: Phone number or partial number to search for
        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)

        **Examples:**

        - `query=555` matches '123-555-1234', '555-1234', '1234555'
        - `query=010` matches '010-12345678', '12010345'

        **Response:** Returns list of Phone objects matching the search pattern.

        Args:
          query: Phone number to search for

          end: End index for pagination

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/phones/search",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "query": query,
                        "end": end,
                        "start": start,
                    },
                    search_query_params.SearchQueryParams,
                ),
            ),
            cast_to=SearchQueryResponse,
        )


class AsyncSearchResource(AsyncAPIResource):
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

    async def by_domain(
        self,
        *,
        domain: str,
        end: int | Omit = omit,
        start: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SearchByDomainResponse:
        """
        Search phones by domain in their source URLs array.

        Finds all phone numbers that were extracted from pages containing the specified
        domain in their source URLs.

        **Authentication:** Required

        **Query Parameters:**

        - `domain`: Domain name to search in source URLs (e.g., 'example.com')
        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)

        **Response:** Returns list of Phone objects where source URLs contain the
        domain.

        Args:
          domain: Domain to search in source URLs (e.g., 'example.com')

          end: End index for pagination

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/phones/search/source-domain",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "domain": domain,
                        "end": end,
                        "start": start,
                    },
                    search_by_domain_params.SearchByDomainParams,
                ),
            ),
            cast_to=SearchByDomainResponse,
        )

    async def query(
        self,
        *,
        query: str,
        end: int | Omit = omit,
        start: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SearchQueryResponse:
        """
        Search phone numbers with partial match anywhere in the number.

        Finds phone numbers that contain the search query anywhere in the number.

        **Authentication:** Required

        **Query Parameters:**

        - `query`: Phone number or partial number to search for
        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)

        **Examples:**

        - `query=555` matches '123-555-1234', '555-1234', '1234555'
        - `query=010` matches '010-12345678', '12010345'

        **Response:** Returns list of Phone objects matching the search pattern.

        Args:
          query: Phone number to search for

          end: End index for pagination

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/phones/search",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "query": query,
                        "end": end,
                        "start": start,
                    },
                    search_query_params.SearchQueryParams,
                ),
            ),
            cast_to=SearchQueryResponse,
        )


class SearchResourceWithRawResponse:
    def __init__(self, search: SearchResource) -> None:
        self._search = search

        self.by_domain = to_raw_response_wrapper(
            search.by_domain,
        )
        self.query = to_raw_response_wrapper(
            search.query,
        )


class AsyncSearchResourceWithRawResponse:
    def __init__(self, search: AsyncSearchResource) -> None:
        self._search = search

        self.by_domain = async_to_raw_response_wrapper(
            search.by_domain,
        )
        self.query = async_to_raw_response_wrapper(
            search.query,
        )


class SearchResourceWithStreamingResponse:
    def __init__(self, search: SearchResource) -> None:
        self._search = search

        self.by_domain = to_streamed_response_wrapper(
            search.by_domain,
        )
        self.query = to_streamed_response_wrapper(
            search.query,
        )


class AsyncSearchResourceWithStreamingResponse:
    def __init__(self, search: AsyncSearchResource) -> None:
        self._search = search

        self.by_domain = async_to_streamed_response_wrapper(
            search.by_domain,
        )
        self.query = async_to_streamed_response_wrapper(
            search.query,
        )
