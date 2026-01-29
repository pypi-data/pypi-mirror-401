# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import source_list_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.source import Source
from ..types.source_list_response import SourceListResponse

__all__ = ["SourcesResource", "AsyncSourcesResource"]


class SourcesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SourcesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return SourcesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SourcesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return SourcesResourceWithStreamingResponse(self)

    def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Source:
        """
        Get a single source by ID.

        Retrieve detailed information about a specific source document.

        **Authentication:** Required

        **Path Parameters:**

        - `id`: UUID of the source

        **Returns:** Source object with URL, publication date, and metadata

        **Response Codes:**

        - 200: Success
        - 404: Source not found
        - 401: Unauthorized (invalid token)

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/sources/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Source,
        )

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
    ) -> SourceListResponse:
        """
        Get paginated list of sources.

        Sources represent the origin documents or references for meetings and data. Each
        source includes a URL and publication date.

        **Authentication:** Required

        **Pagination:**

        - Default: Returns 10 items (index 0-9)
        - Use `start` and `end` parameters to paginate through results
        - Example: `?start=10&end=19` returns items 10-19

        **Example Response:**

        ```json
        [
          {
            "id": "uuid-here",
            "url": "https://example.com/article",
            "date_published": "2024-01-15",
            "created_at": "2024-01-16T10:00:00",
            "updated_at": "2024-01-16T10:00:00"
          }
        ]
        ```

        Args:
          end: End index for pagination

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/sources",
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
                    source_list_params.SourceListParams,
                ),
            ),
            cast_to=SourceListResponse,
        )


class AsyncSourcesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSourcesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSourcesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSourcesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return AsyncSourcesResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Source:
        """
        Get a single source by ID.

        Retrieve detailed information about a specific source document.

        **Authentication:** Required

        **Path Parameters:**

        - `id`: UUID of the source

        **Returns:** Source object with URL, publication date, and metadata

        **Response Codes:**

        - 200: Success
        - 404: Source not found
        - 401: Unauthorized (invalid token)

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/sources/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Source,
        )

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
    ) -> SourceListResponse:
        """
        Get paginated list of sources.

        Sources represent the origin documents or references for meetings and data. Each
        source includes a URL and publication date.

        **Authentication:** Required

        **Pagination:**

        - Default: Returns 10 items (index 0-9)
        - Use `start` and `end` parameters to paginate through results
        - Example: `?start=10&end=19` returns items 10-19

        **Example Response:**

        ```json
        [
          {
            "id": "uuid-here",
            "url": "https://example.com/article",
            "date_published": "2024-01-15",
            "created_at": "2024-01-16T10:00:00",
            "updated_at": "2024-01-16T10:00:00"
          }
        ]
        ```

        Args:
          end: End index for pagination

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/sources",
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
                    source_list_params.SourceListParams,
                ),
            ),
            cast_to=SourceListResponse,
        )


class SourcesResourceWithRawResponse:
    def __init__(self, sources: SourcesResource) -> None:
        self._sources = sources

        self.retrieve = to_raw_response_wrapper(
            sources.retrieve,
        )
        self.list = to_raw_response_wrapper(
            sources.list,
        )


class AsyncSourcesResourceWithRawResponse:
    def __init__(self, sources: AsyncSourcesResource) -> None:
        self._sources = sources

        self.retrieve = async_to_raw_response_wrapper(
            sources.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            sources.list,
        )


class SourcesResourceWithStreamingResponse:
    def __init__(self, sources: SourcesResource) -> None:
        self._sources = sources

        self.retrieve = to_streamed_response_wrapper(
            sources.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            sources.list,
        )


class AsyncSourcesResourceWithStreamingResponse:
    def __init__(self, sources: AsyncSourcesResource) -> None:
        self._sources = sources

        self.retrieve = async_to_streamed_response_wrapper(
            sources.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            sources.list,
        )
