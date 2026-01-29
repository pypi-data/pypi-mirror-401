# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .search import (
    SearchResource,
    AsyncSearchResource,
    SearchResourceWithRawResponse,
    AsyncSearchResourceWithRawResponse,
    SearchResourceWithStreamingResponse,
    AsyncSearchResourceWithStreamingResponse,
)
from ...types import zhihu_list_params
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
from ...types.zhihu.zhihu import Zhihu
from ...types.zhihu_list_response import ZhihuListResponse

__all__ = ["ZhihuResource", "AsyncZhihuResource"]


class ZhihuResource(SyncAPIResource):
    @cached_property
    def search(self) -> SearchResource:
        return SearchResource(self._client)

    @cached_property
    def with_raw_response(self) -> ZhihuResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return ZhihuResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ZhihuResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return ZhihuResourceWithStreamingResponse(self)

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
    ) -> Zhihu:
        """
        Get a specific Zhihu link by ID.

        **Authentication:** Required

        **Response Codes:**

        - 200: Success
        - 404: Zhihu link not found
        - 401: Unauthorized

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/zhihu/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Zhihu,
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
    ) -> ZhihuListResponse:
        """
        Get paginated list of Zhihu links.

        Returns Zhihu Q&A platform links extracted from source documents.

        **Authentication:** Required

        **Query Parameters:**

        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)

        Args:
          end: End index for pagination

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/zhihu",
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
                    zhihu_list_params.ZhihuListParams,
                ),
            ),
            cast_to=ZhihuListResponse,
        )


class AsyncZhihuResource(AsyncAPIResource):
    @cached_property
    def search(self) -> AsyncSearchResource:
        return AsyncSearchResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncZhihuResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return AsyncZhihuResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncZhihuResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return AsyncZhihuResourceWithStreamingResponse(self)

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
    ) -> Zhihu:
        """
        Get a specific Zhihu link by ID.

        **Authentication:** Required

        **Response Codes:**

        - 200: Success
        - 404: Zhihu link not found
        - 401: Unauthorized

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/zhihu/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Zhihu,
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
    ) -> ZhihuListResponse:
        """
        Get paginated list of Zhihu links.

        Returns Zhihu Q&A platform links extracted from source documents.

        **Authentication:** Required

        **Query Parameters:**

        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)

        Args:
          end: End index for pagination

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/zhihu",
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
                    zhihu_list_params.ZhihuListParams,
                ),
            ),
            cast_to=ZhihuListResponse,
        )


class ZhihuResourceWithRawResponse:
    def __init__(self, zhihu: ZhihuResource) -> None:
        self._zhihu = zhihu

        self.retrieve = to_raw_response_wrapper(
            zhihu.retrieve,
        )
        self.list = to_raw_response_wrapper(
            zhihu.list,
        )

    @cached_property
    def search(self) -> SearchResourceWithRawResponse:
        return SearchResourceWithRawResponse(self._zhihu.search)


class AsyncZhihuResourceWithRawResponse:
    def __init__(self, zhihu: AsyncZhihuResource) -> None:
        self._zhihu = zhihu

        self.retrieve = async_to_raw_response_wrapper(
            zhihu.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            zhihu.list,
        )

    @cached_property
    def search(self) -> AsyncSearchResourceWithRawResponse:
        return AsyncSearchResourceWithRawResponse(self._zhihu.search)


class ZhihuResourceWithStreamingResponse:
    def __init__(self, zhihu: ZhihuResource) -> None:
        self._zhihu = zhihu

        self.retrieve = to_streamed_response_wrapper(
            zhihu.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            zhihu.list,
        )

    @cached_property
    def search(self) -> SearchResourceWithStreamingResponse:
        return SearchResourceWithStreamingResponse(self._zhihu.search)


class AsyncZhihuResourceWithStreamingResponse:
    def __init__(self, zhihu: AsyncZhihuResource) -> None:
        self._zhihu = zhihu

        self.retrieve = async_to_streamed_response_wrapper(
            zhihu.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            zhihu.list,
        )

    @cached_property
    def search(self) -> AsyncSearchResourceWithStreamingResponse:
        return AsyncSearchResourceWithStreamingResponse(self._zhihu.search)
