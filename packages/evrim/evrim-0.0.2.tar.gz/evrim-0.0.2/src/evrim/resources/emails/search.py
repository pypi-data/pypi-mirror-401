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
from ...types.emails import search_by_slug_params, search_by_domain_params, search_by_source_domain_params
from ...types.emails.search_by_slug_response import SearchBySlugResponse
from ...types.emails.search_by_domain_response import SearchByDomainResponse
from ...types.emails.search_by_source_domain_response import SearchBySourceDomainResponse

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
        Search emails by domain with exact match.

        Finds all email addresses that match the specified domain exactly.

        **Authentication:** Required

        **Query Parameters:**

        - `domain`: Domain name to search for (e.g., 'mofcom.gov.cn')
        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)

        **Examples:**

        - `domain=mofcom.gov.cn` matches 'user@mofcom.gov.cn'
        - `domain=example.com` matches 'admin@example.com'

        **Response:** Returns list of Email objects matching the domain.

        Args:
          domain: Domain to search (e.g., 'mofcom.gov.cn')

          end: End index for pagination

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/emails/search/domain",
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

    def by_slug(
        self,
        *,
        slug: str,
        end: int | Omit = omit,
        start: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SearchBySlugResponse:
        """
        Search emails by username/slug with case-insensitive partial match.

        Finds email addresses where the username part (before @) starts with the
        specified slug, case-insensitive.

        **Authentication:** Required

        **Query Parameters:**

        - `slug`: Username/slug to search for (e.g., 'john')
        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)

        **Examples:**

        - `slug=john` matches 'john.doe@example.com', 'JOHN@test.com'
        - `slug=admin` matches 'admin@company.com', 'Admin.User@test.com'

        **Response:** Returns list of Email objects matching the slug pattern.

        Args:
          slug: Username/slug to search (e.g., 'john')

          end: End index for pagination

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/emails/search/slug",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "slug": slug,
                        "end": end,
                        "start": start,
                    },
                    search_by_slug_params.SearchBySlugParams,
                ),
            ),
            cast_to=SearchBySlugResponse,
        )

    def by_source_domain(
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
    ) -> SearchBySourceDomainResponse:
        """
        Search emails by domain in their source URLs array.

        Finds all emails that were extracted from pages containing the specified domain
        in their source URLs.

        **Authentication:** Required

        **Query Parameters:**

        - `domain`: Domain name to search in source URLs (e.g., 'example.com')
        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)

        **Example:**

        - `domain=example.com` finds emails found on pages from 'example.com'

        **Response:** Returns list of Email objects where source URLs contain the
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
            "/emails/search/source-domain",
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
                    search_by_source_domain_params.SearchBySourceDomainParams,
                ),
            ),
            cast_to=SearchBySourceDomainResponse,
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
        Search emails by domain with exact match.

        Finds all email addresses that match the specified domain exactly.

        **Authentication:** Required

        **Query Parameters:**

        - `domain`: Domain name to search for (e.g., 'mofcom.gov.cn')
        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)

        **Examples:**

        - `domain=mofcom.gov.cn` matches 'user@mofcom.gov.cn'
        - `domain=example.com` matches 'admin@example.com'

        **Response:** Returns list of Email objects matching the domain.

        Args:
          domain: Domain to search (e.g., 'mofcom.gov.cn')

          end: End index for pagination

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/emails/search/domain",
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

    async def by_slug(
        self,
        *,
        slug: str,
        end: int | Omit = omit,
        start: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SearchBySlugResponse:
        """
        Search emails by username/slug with case-insensitive partial match.

        Finds email addresses where the username part (before @) starts with the
        specified slug, case-insensitive.

        **Authentication:** Required

        **Query Parameters:**

        - `slug`: Username/slug to search for (e.g., 'john')
        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)

        **Examples:**

        - `slug=john` matches 'john.doe@example.com', 'JOHN@test.com'
        - `slug=admin` matches 'admin@company.com', 'Admin.User@test.com'

        **Response:** Returns list of Email objects matching the slug pattern.

        Args:
          slug: Username/slug to search (e.g., 'john')

          end: End index for pagination

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/emails/search/slug",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "slug": slug,
                        "end": end,
                        "start": start,
                    },
                    search_by_slug_params.SearchBySlugParams,
                ),
            ),
            cast_to=SearchBySlugResponse,
        )

    async def by_source_domain(
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
    ) -> SearchBySourceDomainResponse:
        """
        Search emails by domain in their source URLs array.

        Finds all emails that were extracted from pages containing the specified domain
        in their source URLs.

        **Authentication:** Required

        **Query Parameters:**

        - `domain`: Domain name to search in source URLs (e.g., 'example.com')
        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)

        **Example:**

        - `domain=example.com` finds emails found on pages from 'example.com'

        **Response:** Returns list of Email objects where source URLs contain the
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
            "/emails/search/source-domain",
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
                    search_by_source_domain_params.SearchBySourceDomainParams,
                ),
            ),
            cast_to=SearchBySourceDomainResponse,
        )


class SearchResourceWithRawResponse:
    def __init__(self, search: SearchResource) -> None:
        self._search = search

        self.by_domain = to_raw_response_wrapper(
            search.by_domain,
        )
        self.by_slug = to_raw_response_wrapper(
            search.by_slug,
        )
        self.by_source_domain = to_raw_response_wrapper(
            search.by_source_domain,
        )


class AsyncSearchResourceWithRawResponse:
    def __init__(self, search: AsyncSearchResource) -> None:
        self._search = search

        self.by_domain = async_to_raw_response_wrapper(
            search.by_domain,
        )
        self.by_slug = async_to_raw_response_wrapper(
            search.by_slug,
        )
        self.by_source_domain = async_to_raw_response_wrapper(
            search.by_source_domain,
        )


class SearchResourceWithStreamingResponse:
    def __init__(self, search: SearchResource) -> None:
        self._search = search

        self.by_domain = to_streamed_response_wrapper(
            search.by_domain,
        )
        self.by_slug = to_streamed_response_wrapper(
            search.by_slug,
        )
        self.by_source_domain = to_streamed_response_wrapper(
            search.by_source_domain,
        )


class AsyncSearchResourceWithStreamingResponse:
    def __init__(self, search: AsyncSearchResource) -> None:
        self._search = search

        self.by_domain = async_to_streamed_response_wrapper(
            search.by_domain,
        )
        self.by_slug = async_to_streamed_response_wrapper(
            search.by_slug,
        )
        self.by_source_domain = async_to_streamed_response_wrapper(
            search.by_source_domain,
        )
