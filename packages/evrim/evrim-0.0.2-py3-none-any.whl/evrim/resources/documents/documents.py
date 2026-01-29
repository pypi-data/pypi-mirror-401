# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .html import (
    HTMLResource,
    AsyncHTMLResource,
    HTMLResourceWithRawResponse,
    AsyncHTMLResourceWithRawResponse,
    HTMLResourceWithStreamingResponse,
    AsyncHTMLResourceWithStreamingResponse,
)
from .markdown import (
    MarkdownResource,
    AsyncMarkdownResource,
    MarkdownResourceWithRawResponse,
    AsyncMarkdownResourceWithRawResponse,
    MarkdownResourceWithStreamingResponse,
    AsyncMarkdownResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["DocumentsResource", "AsyncDocumentsResource"]


class DocumentsResource(SyncAPIResource):
    @cached_property
    def markdown(self) -> MarkdownResource:
        return MarkdownResource(self._client)

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


class AsyncDocumentsResource(AsyncAPIResource):
    @cached_property
    def markdown(self) -> AsyncMarkdownResource:
        return AsyncMarkdownResource(self._client)

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


class DocumentsResourceWithRawResponse:
    def __init__(self, documents: DocumentsResource) -> None:
        self._documents = documents

    @cached_property
    def markdown(self) -> MarkdownResourceWithRawResponse:
        return MarkdownResourceWithRawResponse(self._documents.markdown)

    @cached_property
    def html(self) -> HTMLResourceWithRawResponse:
        return HTMLResourceWithRawResponse(self._documents.html)


class AsyncDocumentsResourceWithRawResponse:
    def __init__(self, documents: AsyncDocumentsResource) -> None:
        self._documents = documents

    @cached_property
    def markdown(self) -> AsyncMarkdownResourceWithRawResponse:
        return AsyncMarkdownResourceWithRawResponse(self._documents.markdown)

    @cached_property
    def html(self) -> AsyncHTMLResourceWithRawResponse:
        return AsyncHTMLResourceWithRawResponse(self._documents.html)


class DocumentsResourceWithStreamingResponse:
    def __init__(self, documents: DocumentsResource) -> None:
        self._documents = documents

    @cached_property
    def markdown(self) -> MarkdownResourceWithStreamingResponse:
        return MarkdownResourceWithStreamingResponse(self._documents.markdown)

    @cached_property
    def html(self) -> HTMLResourceWithStreamingResponse:
        return HTMLResourceWithStreamingResponse(self._documents.html)


class AsyncDocumentsResourceWithStreamingResponse:
    def __init__(self, documents: AsyncDocumentsResource) -> None:
        self._documents = documents

    @cached_property
    def markdown(self) -> AsyncMarkdownResourceWithStreamingResponse:
        return AsyncMarkdownResourceWithStreamingResponse(self._documents.markdown)

    @cached_property
    def html(self) -> AsyncHTMLResourceWithStreamingResponse:
        return AsyncHTMLResourceWithStreamingResponse(self._documents.html)
