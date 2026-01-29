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
from ...types import weibo_list_params
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
from ...types.weibo.weibo import Weibo
from ...types.weibo_list_response import WeiboListResponse

__all__ = ["WeiboResource", "AsyncWeiboResource"]


class WeiboResource(SyncAPIResource):
    @cached_property
    def search(self) -> SearchResource:
        return SearchResource(self._client)

    @cached_property
    def with_raw_response(self) -> WeiboResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return WeiboResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> WeiboResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return WeiboResourceWithStreamingResponse(self)

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
    ) -> Weibo:
        """
        Get a specific Weibo link by ID.

        **Authentication:** Required

        **Response Codes:**

        - 200: Success
        - 404: Weibo link not found
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
            f"/weibo/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Weibo,
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
    ) -> WeiboListResponse:
        """
        Get paginated list of Weibo links.

        Returns Weibo social media links extracted from source documents.

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
            "/weibo",
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
                    weibo_list_params.WeiboListParams,
                ),
            ),
            cast_to=WeiboListResponse,
        )


class AsyncWeiboResource(AsyncAPIResource):
    @cached_property
    def search(self) -> AsyncSearchResource:
        return AsyncSearchResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncWeiboResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return AsyncWeiboResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncWeiboResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return AsyncWeiboResourceWithStreamingResponse(self)

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
    ) -> Weibo:
        """
        Get a specific Weibo link by ID.

        **Authentication:** Required

        **Response Codes:**

        - 200: Success
        - 404: Weibo link not found
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
            f"/weibo/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Weibo,
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
    ) -> WeiboListResponse:
        """
        Get paginated list of Weibo links.

        Returns Weibo social media links extracted from source documents.

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
            "/weibo",
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
                    weibo_list_params.WeiboListParams,
                ),
            ),
            cast_to=WeiboListResponse,
        )


class WeiboResourceWithRawResponse:
    def __init__(self, weibo: WeiboResource) -> None:
        self._weibo = weibo

        self.retrieve = to_raw_response_wrapper(
            weibo.retrieve,
        )
        self.list = to_raw_response_wrapper(
            weibo.list,
        )

    @cached_property
    def search(self) -> SearchResourceWithRawResponse:
        return SearchResourceWithRawResponse(self._weibo.search)


class AsyncWeiboResourceWithRawResponse:
    def __init__(self, weibo: AsyncWeiboResource) -> None:
        self._weibo = weibo

        self.retrieve = async_to_raw_response_wrapper(
            weibo.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            weibo.list,
        )

    @cached_property
    def search(self) -> AsyncSearchResourceWithRawResponse:
        return AsyncSearchResourceWithRawResponse(self._weibo.search)


class WeiboResourceWithStreamingResponse:
    def __init__(self, weibo: WeiboResource) -> None:
        self._weibo = weibo

        self.retrieve = to_streamed_response_wrapper(
            weibo.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            weibo.list,
        )

    @cached_property
    def search(self) -> SearchResourceWithStreamingResponse:
        return SearchResourceWithStreamingResponse(self._weibo.search)


class AsyncWeiboResourceWithStreamingResponse:
    def __init__(self, weibo: AsyncWeiboResource) -> None:
        self._weibo = weibo

        self.retrieve = async_to_streamed_response_wrapper(
            weibo.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            weibo.list,
        )

    @cached_property
    def search(self) -> AsyncSearchResourceWithStreamingResponse:
        return AsyncSearchResourceWithStreamingResponse(self._weibo.search)
