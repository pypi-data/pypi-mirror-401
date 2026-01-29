# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

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
from ....types.search.documents import html_search_params, html_search_by_url_params, html_search_by_domain_params
from ....types.search.documents.html_search_response import HTMLSearchResponse
from ....types.search.documents.html_search_by_url_response import HTMLSearchByURLResponse
from ....types.search.documents.html_search_by_domain_response import HTMLSearchByDomainResponse

__all__ = ["HTMLResource", "AsyncHTMLResource"]


class HTMLResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> HTMLResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return HTMLResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> HTMLResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return HTMLResourceWithStreamingResponse(self)

    def search(
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
    ) -> HTMLSearchResponse:
        """
        Search HTML documents by content using keyword matching.

        Searches raw HTML content for matching text. Case-insensitive.

        **Authentication:** Required

        **Query Parameters:**

        - `q`: Search term (required)
        - `limit`: Maximum results (1-100, default: 10)
        - `offset`: Skip first N results for pagination (default: 0)

        **Response:** Returns list of HTMLDocumentSearchResult with URL, content, and
        snippet.

        **Performance Notes:**

        - May be slower on large HTML content
        - Very broad searches may timeout

        **Security Warning:** Raw HTML content is returned without sanitization. Client
        applications MUST sanitize HTML before rendering to prevent XSS attacks.

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
            "/search/documents/html",
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
                    html_search_params.HTMLSearchParams,
                ),
            ),
            cast_to=HTMLSearchResponse,
        )

    def search_by_domain(
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
    ) -> HTMLSearchByDomainResponse:
        """
        Search HTML documents by domain name.

        Finds all documents from URLs containing the specified domain. Input is
        validated to prevent SQL injection.

        **Authentication:** Required

        **Query Parameters:**

        - `domain`: Domain to search for (required)
          - Example: "mofcom.gov.cn"
          - Example: "gov.cn"
          - Must contain only alphanumeric characters, dots, and hyphens
        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)

        **Security:** Domain input is validated with regex: ^[a-zA-Z0-9.-]+$

        **Returns:** List of HTML documents from the specified domain

        Args:
          domain: Domain to search for

          end: End index for pagination

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/search/documents/html/by-domain",
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
                    html_search_by_domain_params.HTMLSearchByDomainParams,
                ),
            ),
            cast_to=HTMLSearchByDomainResponse,
        )

    def search_by_url(
        self,
        *,
        url: str,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> HTMLSearchByURLResponse:
        """
        Search HTML documents by URL pattern (partial matching).

        Case-insensitive pattern matching on URL field. Useful for finding all documents
        from a specific path or subdomain.

        **Authentication:** Required

        **Query Parameters:**

        - `url`: URL pattern to search for (required)
          - Example: "mofcom.gov.cn" → finds all URLs containing this domain
          - Example: "/news/" → finds all URLs with /news/ in the path
        - `limit`: Maximum results (1-100, default: 10)
        - `offset`: Skip first N results for pagination (default: 0)

        **Returns:** List of HTML documents with matching URLs

        **Difference from /documents/html/by-url/{url}:**

        - This endpoint: Partial match, multiple results, query parameter
        - That endpoint: Exact match, single result, path parameter

        Args:
          url: URL pattern to search for

          limit: Maximum number of results

          offset: Offset for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/search/documents/html/by-url",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "url": url,
                        "limit": limit,
                        "offset": offset,
                    },
                    html_search_by_url_params.HTMLSearchByURLParams,
                ),
            ),
            cast_to=HTMLSearchByURLResponse,
        )


class AsyncHTMLResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncHTMLResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return AsyncHTMLResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncHTMLResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return AsyncHTMLResourceWithStreamingResponse(self)

    async def search(
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
    ) -> HTMLSearchResponse:
        """
        Search HTML documents by content using keyword matching.

        Searches raw HTML content for matching text. Case-insensitive.

        **Authentication:** Required

        **Query Parameters:**

        - `q`: Search term (required)
        - `limit`: Maximum results (1-100, default: 10)
        - `offset`: Skip first N results for pagination (default: 0)

        **Response:** Returns list of HTMLDocumentSearchResult with URL, content, and
        snippet.

        **Performance Notes:**

        - May be slower on large HTML content
        - Very broad searches may timeout

        **Security Warning:** Raw HTML content is returned without sanitization. Client
        applications MUST sanitize HTML before rendering to prevent XSS attacks.

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
            "/search/documents/html",
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
                    html_search_params.HTMLSearchParams,
                ),
            ),
            cast_to=HTMLSearchResponse,
        )

    async def search_by_domain(
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
    ) -> HTMLSearchByDomainResponse:
        """
        Search HTML documents by domain name.

        Finds all documents from URLs containing the specified domain. Input is
        validated to prevent SQL injection.

        **Authentication:** Required

        **Query Parameters:**

        - `domain`: Domain to search for (required)
          - Example: "mofcom.gov.cn"
          - Example: "gov.cn"
          - Must contain only alphanumeric characters, dots, and hyphens
        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)

        **Security:** Domain input is validated with regex: ^[a-zA-Z0-9.-]+$

        **Returns:** List of HTML documents from the specified domain

        Args:
          domain: Domain to search for

          end: End index for pagination

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/search/documents/html/by-domain",
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
                    html_search_by_domain_params.HTMLSearchByDomainParams,
                ),
            ),
            cast_to=HTMLSearchByDomainResponse,
        )

    async def search_by_url(
        self,
        *,
        url: str,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> HTMLSearchByURLResponse:
        """
        Search HTML documents by URL pattern (partial matching).

        Case-insensitive pattern matching on URL field. Useful for finding all documents
        from a specific path or subdomain.

        **Authentication:** Required

        **Query Parameters:**

        - `url`: URL pattern to search for (required)
          - Example: "mofcom.gov.cn" → finds all URLs containing this domain
          - Example: "/news/" → finds all URLs with /news/ in the path
        - `limit`: Maximum results (1-100, default: 10)
        - `offset`: Skip first N results for pagination (default: 0)

        **Returns:** List of HTML documents with matching URLs

        **Difference from /documents/html/by-url/{url}:**

        - This endpoint: Partial match, multiple results, query parameter
        - That endpoint: Exact match, single result, path parameter

        Args:
          url: URL pattern to search for

          limit: Maximum number of results

          offset: Offset for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/search/documents/html/by-url",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "url": url,
                        "limit": limit,
                        "offset": offset,
                    },
                    html_search_by_url_params.HTMLSearchByURLParams,
                ),
            ),
            cast_to=HTMLSearchByURLResponse,
        )


class HTMLResourceWithRawResponse:
    def __init__(self, html: HTMLResource) -> None:
        self._html = html

        self.search = to_raw_response_wrapper(
            html.search,
        )
        self.search_by_domain = to_raw_response_wrapper(
            html.search_by_domain,
        )
        self.search_by_url = to_raw_response_wrapper(
            html.search_by_url,
        )


class AsyncHTMLResourceWithRawResponse:
    def __init__(self, html: AsyncHTMLResource) -> None:
        self._html = html

        self.search = async_to_raw_response_wrapper(
            html.search,
        )
        self.search_by_domain = async_to_raw_response_wrapper(
            html.search_by_domain,
        )
        self.search_by_url = async_to_raw_response_wrapper(
            html.search_by_url,
        )


class HTMLResourceWithStreamingResponse:
    def __init__(self, html: HTMLResource) -> None:
        self._html = html

        self.search = to_streamed_response_wrapper(
            html.search,
        )
        self.search_by_domain = to_streamed_response_wrapper(
            html.search_by_domain,
        )
        self.search_by_url = to_streamed_response_wrapper(
            html.search_by_url,
        )


class AsyncHTMLResourceWithStreamingResponse:
    def __init__(self, html: AsyncHTMLResource) -> None:
        self._html = html

        self.search = async_to_streamed_response_wrapper(
            html.search,
        )
        self.search_by_domain = async_to_streamed_response_wrapper(
            html.search_by_domain,
        )
        self.search_by_url = async_to_streamed_response_wrapper(
            html.search_by_url,
        )
