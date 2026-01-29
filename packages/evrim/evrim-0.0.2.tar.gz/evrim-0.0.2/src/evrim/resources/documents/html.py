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
from ...types.documents import html_list_params
from ...types.documents.html_document import HTMLDocument
from ...types.documents.html_list_response import HTMLListResponse

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

    def list(
        self,
        *,
        end: int | Omit = omit,
        start: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> HTMLListResponse:
        """
        Get paginated list of HTML documents.

        Returns raw HTML content from Chinese government (.gov.cn) websites.

        **Authentication:** Required

        **Query Parameters:**

        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)

        **Document Fields:**

        - url: Source URL of the document
        - content: Raw HTML content (as-is, not processed)
        - created_at: Timestamp when record was created
        - updated_at: Timestamp when record was last updated

        **Security Warning:** Raw HTML content is returned without sanitization. Client
        applications MUST sanitize HTML before rendering to prevent XSS attacks. Never
        directly render raw HTML from this API in a browser context.

        Args:
          end: End index for pagination

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/documents/html",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "end": end,
                        "start": start,
                    },
                    html_list_params.HTMLListParams,
                ),
            ),
            cast_to=HTMLListResponse,
        )

    def retrieve_by_url(
        self,
        url: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> HTMLDocument:
        """
        Get a specific HTML document by its exact URL.

        **Authentication:** Required

        **Path Parameters:**

        - `url`: The complete URL of the document (case-sensitive, exact match)

        **Returns:** HTML document with raw content

        **Example:**

        ```
        GET /documents/html/by-url/https://example.gov.cn/page.html
        ```

        **Security Warning:** Raw HTML content is returned without sanitization. Client
        applications MUST sanitize HTML before rendering to prevent XSS attacks.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not url:
            raise ValueError(f"Expected a non-empty value for `url` but received {url!r}")
        return self._get(
            f"/documents/html/by-url/{url}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=HTMLDocument,
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

    async def list(
        self,
        *,
        end: int | Omit = omit,
        start: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> HTMLListResponse:
        """
        Get paginated list of HTML documents.

        Returns raw HTML content from Chinese government (.gov.cn) websites.

        **Authentication:** Required

        **Query Parameters:**

        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)

        **Document Fields:**

        - url: Source URL of the document
        - content: Raw HTML content (as-is, not processed)
        - created_at: Timestamp when record was created
        - updated_at: Timestamp when record was last updated

        **Security Warning:** Raw HTML content is returned without sanitization. Client
        applications MUST sanitize HTML before rendering to prevent XSS attacks. Never
        directly render raw HTML from this API in a browser context.

        Args:
          end: End index for pagination

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/documents/html",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "end": end,
                        "start": start,
                    },
                    html_list_params.HTMLListParams,
                ),
            ),
            cast_to=HTMLListResponse,
        )

    async def retrieve_by_url(
        self,
        url: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> HTMLDocument:
        """
        Get a specific HTML document by its exact URL.

        **Authentication:** Required

        **Path Parameters:**

        - `url`: The complete URL of the document (case-sensitive, exact match)

        **Returns:** HTML document with raw content

        **Example:**

        ```
        GET /documents/html/by-url/https://example.gov.cn/page.html
        ```

        **Security Warning:** Raw HTML content is returned without sanitization. Client
        applications MUST sanitize HTML before rendering to prevent XSS attacks.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not url:
            raise ValueError(f"Expected a non-empty value for `url` but received {url!r}")
        return await self._get(
            f"/documents/html/by-url/{url}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=HTMLDocument,
        )


class HTMLResourceWithRawResponse:
    def __init__(self, html: HTMLResource) -> None:
        self._html = html

        self.list = to_raw_response_wrapper(
            html.list,
        )
        self.retrieve_by_url = to_raw_response_wrapper(
            html.retrieve_by_url,
        )


class AsyncHTMLResourceWithRawResponse:
    def __init__(self, html: AsyncHTMLResource) -> None:
        self._html = html

        self.list = async_to_raw_response_wrapper(
            html.list,
        )
        self.retrieve_by_url = async_to_raw_response_wrapper(
            html.retrieve_by_url,
        )


class HTMLResourceWithStreamingResponse:
    def __init__(self, html: HTMLResource) -> None:
        self._html = html

        self.list = to_streamed_response_wrapper(
            html.list,
        )
        self.retrieve_by_url = to_streamed_response_wrapper(
            html.retrieve_by_url,
        )


class AsyncHTMLResourceWithStreamingResponse:
    def __init__(self, html: AsyncHTMLResource) -> None:
        self._html = html

        self.list = async_to_streamed_response_wrapper(
            html.list,
        )
        self.retrieve_by_url = async_to_streamed_response_wrapper(
            html.retrieve_by_url,
        )
