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
from ...types.documents import markdown_list_params
from ...types.documents.document import Document
from ...types.documents.markdown_list_response import MarkdownListResponse

__all__ = ["MarkdownResource", "AsyncMarkdownResource"]


class MarkdownResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> MarkdownResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return MarkdownResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MarkdownResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return MarkdownResourceWithStreamingResponse(self)

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
    ) -> MarkdownListResponse:
        """
        Get paginated list of markdown documents.

        Returns documents in the system with their URLs and content in markdown format.
        Documents are the source materials that provide context and information about
        meetings, participants, and organizations.

        **Authentication:** Required

        **Query Parameters:**

        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)

        **Document Fields:**

        - URL: Source location of the document
        - Markdown: Document content in markdown format

        **Use Cases:**

        - Browse available source documents
        - Access document content for analysis
        - Integration with content management systems

        **Note:** For searching documents by content, use the search endpoints:

        - `/search/documents/markdown` for keyword search
        - `/search/documents/semantic` for AI-powered semantic search

        Args:
          end: End index for pagination

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/documents/markdown",
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
                    markdown_list_params.MarkdownListParams,
                ),
            ),
            cast_to=MarkdownListResponse,
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
    ) -> Document:
        """
        Get a markdown document by its source URL.

        Retrieves document content and metadata by providing the original URL of the
        source document. This is useful when you know the document's web location.

        **Authentication:** Required

        **Path Parameters:**

        - `url`: Full URL of the document (path parameter)
          - Example: `/documents/markdown/by-url/https://example.com/article.html`
          - URL encoding is handled automatically

        **Response Fields:**

        - URL: Original source URL
        - Markdown: Document content in markdown format

        **Use Cases:**

        - Fetch document by known URL
        - Verify if a URL has been indexed
        - Access document content for specific sources
        - Integration with external systems

        **Response Codes:**

        - 200: Success - document found and returned
        - 404: Document not found (URL not in database)
        - 401: Unauthorized

        **Note:** The URL path parameter accepts full URLs including protocol
        (https://).

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not url:
            raise ValueError(f"Expected a non-empty value for `url` but received {url!r}")
        return self._get(
            f"/documents/markdown/by-url/{url}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Document,
        )


class AsyncMarkdownResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMarkdownResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return AsyncMarkdownResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMarkdownResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return AsyncMarkdownResourceWithStreamingResponse(self)

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
    ) -> MarkdownListResponse:
        """
        Get paginated list of markdown documents.

        Returns documents in the system with their URLs and content in markdown format.
        Documents are the source materials that provide context and information about
        meetings, participants, and organizations.

        **Authentication:** Required

        **Query Parameters:**

        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)

        **Document Fields:**

        - URL: Source location of the document
        - Markdown: Document content in markdown format

        **Use Cases:**

        - Browse available source documents
        - Access document content for analysis
        - Integration with content management systems

        **Note:** For searching documents by content, use the search endpoints:

        - `/search/documents/markdown` for keyword search
        - `/search/documents/semantic` for AI-powered semantic search

        Args:
          end: End index for pagination

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/documents/markdown",
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
                    markdown_list_params.MarkdownListParams,
                ),
            ),
            cast_to=MarkdownListResponse,
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
    ) -> Document:
        """
        Get a markdown document by its source URL.

        Retrieves document content and metadata by providing the original URL of the
        source document. This is useful when you know the document's web location.

        **Authentication:** Required

        **Path Parameters:**

        - `url`: Full URL of the document (path parameter)
          - Example: `/documents/markdown/by-url/https://example.com/article.html`
          - URL encoding is handled automatically

        **Response Fields:**

        - URL: Original source URL
        - Markdown: Document content in markdown format

        **Use Cases:**

        - Fetch document by known URL
        - Verify if a URL has been indexed
        - Access document content for specific sources
        - Integration with external systems

        **Response Codes:**

        - 200: Success - document found and returned
        - 404: Document not found (URL not in database)
        - 401: Unauthorized

        **Note:** The URL path parameter accepts full URLs including protocol
        (https://).

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not url:
            raise ValueError(f"Expected a non-empty value for `url` but received {url!r}")
        return await self._get(
            f"/documents/markdown/by-url/{url}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Document,
        )


class MarkdownResourceWithRawResponse:
    def __init__(self, markdown: MarkdownResource) -> None:
        self._markdown = markdown

        self.list = to_raw_response_wrapper(
            markdown.list,
        )
        self.retrieve_by_url = to_raw_response_wrapper(
            markdown.retrieve_by_url,
        )


class AsyncMarkdownResourceWithRawResponse:
    def __init__(self, markdown: AsyncMarkdownResource) -> None:
        self._markdown = markdown

        self.list = async_to_raw_response_wrapper(
            markdown.list,
        )
        self.retrieve_by_url = async_to_raw_response_wrapper(
            markdown.retrieve_by_url,
        )


class MarkdownResourceWithStreamingResponse:
    def __init__(self, markdown: MarkdownResource) -> None:
        self._markdown = markdown

        self.list = to_streamed_response_wrapper(
            markdown.list,
        )
        self.retrieve_by_url = to_streamed_response_wrapper(
            markdown.retrieve_by_url,
        )


class AsyncMarkdownResourceWithStreamingResponse:
    def __init__(self, markdown: AsyncMarkdownResource) -> None:
        self._markdown = markdown

        self.list = async_to_streamed_response_wrapper(
            markdown.list,
        )
        self.retrieve_by_url = async_to_streamed_response_wrapper(
            markdown.retrieve_by_url,
        )
