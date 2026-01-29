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
from ...types.auth import mcp_token_list_params, mcp_token_create_params
from ..._base_client import make_request_options
from ...types.auth.mcp_token_list_response import McpTokenListResponse
from ...types.auth.mcp_token_create_response import McpTokenCreateResponse

__all__ = ["McpTokensResource", "AsyncMcpTokensResource"]


class McpTokensResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> McpTokensResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return McpTokensResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> McpTokensResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return McpTokensResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        expiry_days: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> McpTokenCreateResponse:
        """
        Create a long-lived MCP (Model Context Protocol) token for API access.

            MCP tokens are designed for programmatic API access by AI assistants and other automated clients.
            Unlike JWT tokens, MCP tokens are long-lived (90-365 days) and don't require refresh workflows.

            **Security Notes:**
            - The token string is only shown once upon creation - save it securely
            - Tokens can be revoked at any time via the DELETE endpoint
            - Each token is tied to your user account with full API access
            - Rate limiting still applies (IP-based)

            **Usage:**
            Use the token in the Authorization header: `Bearer mcp_...`

        Args:
          name: User-friendly name for the token

          expiry_days: Number of days until token expires

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/auth/mcp-tokens",
            body=maybe_transform(
                {
                    "name": name,
                    "expiry_days": expiry_days,
                },
                mcp_token_create_params.McpTokenCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=McpTokenCreateResponse,
        )

    def list(
        self,
        *,
        include_revoked: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> McpTokenListResponse:
        """
        List all MCP tokens for the authenticated user.

            Returns metadata about tokens including:
            - Token prefix (first 12 characters for identification)
            - Name and creation date
            - Expiration and last used timestamps
            - Revocation status

            **Note:** The actual token strings are never shown after creation.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/auth/mcp-tokens",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"include_revoked": include_revoked}, mcp_token_list_params.McpTokenListParams),
            ),
            cast_to=McpTokenListResponse,
        )

    def revoke(
        self,
        token_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Revoke an MCP token, immediately invalidating it.

            Revoked tokens:
            - Can no longer be used for authentication
            - Cannot be un-revoked
            - Are soft-deleted (remain in database for audit purposes)

            You can only revoke your own tokens.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not token_id:
            raise ValueError(f"Expected a non-empty value for `token_id` but received {token_id!r}")
        return self._delete(
            f"/auth/mcp-tokens/{token_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncMcpTokensResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMcpTokensResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return AsyncMcpTokensResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMcpTokensResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return AsyncMcpTokensResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        expiry_days: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> McpTokenCreateResponse:
        """
        Create a long-lived MCP (Model Context Protocol) token for API access.

            MCP tokens are designed for programmatic API access by AI assistants and other automated clients.
            Unlike JWT tokens, MCP tokens are long-lived (90-365 days) and don't require refresh workflows.

            **Security Notes:**
            - The token string is only shown once upon creation - save it securely
            - Tokens can be revoked at any time via the DELETE endpoint
            - Each token is tied to your user account with full API access
            - Rate limiting still applies (IP-based)

            **Usage:**
            Use the token in the Authorization header: `Bearer mcp_...`

        Args:
          name: User-friendly name for the token

          expiry_days: Number of days until token expires

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/auth/mcp-tokens",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "expiry_days": expiry_days,
                },
                mcp_token_create_params.McpTokenCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=McpTokenCreateResponse,
        )

    async def list(
        self,
        *,
        include_revoked: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> McpTokenListResponse:
        """
        List all MCP tokens for the authenticated user.

            Returns metadata about tokens including:
            - Token prefix (first 12 characters for identification)
            - Name and creation date
            - Expiration and last used timestamps
            - Revocation status

            **Note:** The actual token strings are never shown after creation.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/auth/mcp-tokens",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"include_revoked": include_revoked}, mcp_token_list_params.McpTokenListParams
                ),
            ),
            cast_to=McpTokenListResponse,
        )

    async def revoke(
        self,
        token_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Revoke an MCP token, immediately invalidating it.

            Revoked tokens:
            - Can no longer be used for authentication
            - Cannot be un-revoked
            - Are soft-deleted (remain in database for audit purposes)

            You can only revoke your own tokens.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not token_id:
            raise ValueError(f"Expected a non-empty value for `token_id` but received {token_id!r}")
        return await self._delete(
            f"/auth/mcp-tokens/{token_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class McpTokensResourceWithRawResponse:
    def __init__(self, mcp_tokens: McpTokensResource) -> None:
        self._mcp_tokens = mcp_tokens

        self.create = to_raw_response_wrapper(
            mcp_tokens.create,
        )
        self.list = to_raw_response_wrapper(
            mcp_tokens.list,
        )
        self.revoke = to_raw_response_wrapper(
            mcp_tokens.revoke,
        )


class AsyncMcpTokensResourceWithRawResponse:
    def __init__(self, mcp_tokens: AsyncMcpTokensResource) -> None:
        self._mcp_tokens = mcp_tokens

        self.create = async_to_raw_response_wrapper(
            mcp_tokens.create,
        )
        self.list = async_to_raw_response_wrapper(
            mcp_tokens.list,
        )
        self.revoke = async_to_raw_response_wrapper(
            mcp_tokens.revoke,
        )


class McpTokensResourceWithStreamingResponse:
    def __init__(self, mcp_tokens: McpTokensResource) -> None:
        self._mcp_tokens = mcp_tokens

        self.create = to_streamed_response_wrapper(
            mcp_tokens.create,
        )
        self.list = to_streamed_response_wrapper(
            mcp_tokens.list,
        )
        self.revoke = to_streamed_response_wrapper(
            mcp_tokens.revoke,
        )


class AsyncMcpTokensResourceWithStreamingResponse:
    def __init__(self, mcp_tokens: AsyncMcpTokensResource) -> None:
        self._mcp_tokens = mcp_tokens

        self.create = async_to_streamed_response_wrapper(
            mcp_tokens.create,
        )
        self.list = async_to_streamed_response_wrapper(
            mcp_tokens.list,
        )
        self.revoke = async_to_streamed_response_wrapper(
            mcp_tokens.revoke,
        )
