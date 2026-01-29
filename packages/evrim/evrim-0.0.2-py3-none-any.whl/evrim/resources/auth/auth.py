# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...types import auth_get_token_params, auth_refresh_token_params
from ..._types import Body, Query, Headers, NotGiven, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from .mcp_tokens import (
    McpTokensResource,
    AsyncMcpTokensResource,
    McpTokensResourceWithRawResponse,
    AsyncMcpTokensResourceWithRawResponse,
    McpTokensResourceWithStreamingResponse,
    AsyncMcpTokensResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.auth_response import AuthResponse

__all__ = ["AuthResource", "AsyncAuthResource"]


class AuthResource(SyncAPIResource):
    @cached_property
    def mcp_tokens(self) -> McpTokensResource:
        return McpTokensResource(self._client)

    @cached_property
    def with_raw_response(self) -> AuthResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return AuthResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AuthResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return AuthResourceWithStreamingResponse(self)

    def get_token(
        self,
        *,
        email: str,
        password: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AuthResponse:
        """
        Get authentication token for existing user.

        Sign in with email and password to receive JWT access token.

        **Request Body:**

        ```json
        {
          "email": "user@example.com",
          "password": "your-password"
        }
        ```

        **Response:**

        ```json
        {
          "access_token": "...",
          "refresh_token": "...",
          "token_type": "bearer",
          "expires_in": 3600,
          "user": {
            "id": "user-id",
            "email": "user@example.com"
          }
        }
        ```

        **Use the token:** Include in Authorization header:
        `Authorization: Bearer <access_token>`

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/auth/token",
            body=maybe_transform(
                {
                    "email": email,
                    "password": password,
                },
                auth_get_token_params.AuthGetTokenParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AuthResponse,
        )

    def refresh_token(
        self,
        *,
        refresh_token: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AuthResponse:
        """
        Refresh access token using refresh token.

        Get a new access token without re-entering credentials. Use this endpoint when
        your access token expires to maintain continuous authentication.

        **Authentication:** Not Required (uses refresh token instead)

        **Request Body:**

        ```json
        {
          "refresh_token": "your-refresh-token-here"
        }
        ```

        **Response:**

        ```json
        {
          "access_token": "new-access-token...",
          "refresh_token": "new-refresh-token...",
          "token_type": "bearer",
          "expires_in": 3600,
          "user": {
            "id": "user-id",
            "email": "user@example.com"
          }
        }
        ```

        **How It Works:**

        1. Client detects access token is expired (or about to expire)
        2. Client calls this endpoint with the refresh token
        3. Receives new access token and new refresh token
        4. Continues making API requests with new access token

        **Important Notes:**

        - **Refresh tokens are single-use**: Each refresh returns a NEW refresh token
        - **Store the new refresh token**: Replace the old one in your storage
        - **Refresh tokens expire**: Default is 30 days (configurable in Supabase)
        - **Rate limited**: 10 refreshes per minute to prevent abuse

        **Token Rotation:** Supabase uses refresh token rotation for security. Each time
        you refresh:

        - Old refresh token becomes invalid
        - New refresh token is issued
        - This prevents refresh token reuse if compromised

        **Best Practices:**

        - Refresh before access token expires (e.g., when 80% of time has passed)
        - Store new refresh token securely after each refresh
        - Handle 401 errors by attempting refresh before re-authenticating

        **Example Flow:**

        ```
        1. Login → Get tokens (access + refresh)
        2. Use access token for API calls
        3. Access token expires after 1 hour
        4. Call /auth/refresh with refresh token
        5. Get new tokens
        6. Continue using new access token
        7. Repeat steps 3-6 as needed
        ```

        **For MCP Clients:** Implement automatic token refresh in your auth manager to
        handle token expiration transparently.

        **Response Codes:**

        - 200: Success - new tokens issued
        - 401: Invalid or expired refresh token
        - 429: Rate limit exceeded (too many refresh attempts)

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/auth/refresh",
            body=maybe_transform({"refresh_token": refresh_token}, auth_refresh_token_params.AuthRefreshTokenParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AuthResponse,
        )


class AsyncAuthResource(AsyncAPIResource):
    @cached_property
    def mcp_tokens(self) -> AsyncMcpTokensResource:
        return AsyncMcpTokensResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncAuthResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAuthResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAuthResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return AsyncAuthResourceWithStreamingResponse(self)

    async def get_token(
        self,
        *,
        email: str,
        password: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AuthResponse:
        """
        Get authentication token for existing user.

        Sign in with email and password to receive JWT access token.

        **Request Body:**

        ```json
        {
          "email": "user@example.com",
          "password": "your-password"
        }
        ```

        **Response:**

        ```json
        {
          "access_token": "...",
          "refresh_token": "...",
          "token_type": "bearer",
          "expires_in": 3600,
          "user": {
            "id": "user-id",
            "email": "user@example.com"
          }
        }
        ```

        **Use the token:** Include in Authorization header:
        `Authorization: Bearer <access_token>`

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/auth/token",
            body=await async_maybe_transform(
                {
                    "email": email,
                    "password": password,
                },
                auth_get_token_params.AuthGetTokenParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AuthResponse,
        )

    async def refresh_token(
        self,
        *,
        refresh_token: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AuthResponse:
        """
        Refresh access token using refresh token.

        Get a new access token without re-entering credentials. Use this endpoint when
        your access token expires to maintain continuous authentication.

        **Authentication:** Not Required (uses refresh token instead)

        **Request Body:**

        ```json
        {
          "refresh_token": "your-refresh-token-here"
        }
        ```

        **Response:**

        ```json
        {
          "access_token": "new-access-token...",
          "refresh_token": "new-refresh-token...",
          "token_type": "bearer",
          "expires_in": 3600,
          "user": {
            "id": "user-id",
            "email": "user@example.com"
          }
        }
        ```

        **How It Works:**

        1. Client detects access token is expired (or about to expire)
        2. Client calls this endpoint with the refresh token
        3. Receives new access token and new refresh token
        4. Continues making API requests with new access token

        **Important Notes:**

        - **Refresh tokens are single-use**: Each refresh returns a NEW refresh token
        - **Store the new refresh token**: Replace the old one in your storage
        - **Refresh tokens expire**: Default is 30 days (configurable in Supabase)
        - **Rate limited**: 10 refreshes per minute to prevent abuse

        **Token Rotation:** Supabase uses refresh token rotation for security. Each time
        you refresh:

        - Old refresh token becomes invalid
        - New refresh token is issued
        - This prevents refresh token reuse if compromised

        **Best Practices:**

        - Refresh before access token expires (e.g., when 80% of time has passed)
        - Store new refresh token securely after each refresh
        - Handle 401 errors by attempting refresh before re-authenticating

        **Example Flow:**

        ```
        1. Login → Get tokens (access + refresh)
        2. Use access token for API calls
        3. Access token expires after 1 hour
        4. Call /auth/refresh with refresh token
        5. Get new tokens
        6. Continue using new access token
        7. Repeat steps 3-6 as needed
        ```

        **For MCP Clients:** Implement automatic token refresh in your auth manager to
        handle token expiration transparently.

        **Response Codes:**

        - 200: Success - new tokens issued
        - 401: Invalid or expired refresh token
        - 429: Rate limit exceeded (too many refresh attempts)

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/auth/refresh",
            body=await async_maybe_transform(
                {"refresh_token": refresh_token}, auth_refresh_token_params.AuthRefreshTokenParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AuthResponse,
        )


class AuthResourceWithRawResponse:
    def __init__(self, auth: AuthResource) -> None:
        self._auth = auth

        self.get_token = to_raw_response_wrapper(
            auth.get_token,
        )
        self.refresh_token = to_raw_response_wrapper(
            auth.refresh_token,
        )

    @cached_property
    def mcp_tokens(self) -> McpTokensResourceWithRawResponse:
        return McpTokensResourceWithRawResponse(self._auth.mcp_tokens)


class AsyncAuthResourceWithRawResponse:
    def __init__(self, auth: AsyncAuthResource) -> None:
        self._auth = auth

        self.get_token = async_to_raw_response_wrapper(
            auth.get_token,
        )
        self.refresh_token = async_to_raw_response_wrapper(
            auth.refresh_token,
        )

    @cached_property
    def mcp_tokens(self) -> AsyncMcpTokensResourceWithRawResponse:
        return AsyncMcpTokensResourceWithRawResponse(self._auth.mcp_tokens)


class AuthResourceWithStreamingResponse:
    def __init__(self, auth: AuthResource) -> None:
        self._auth = auth

        self.get_token = to_streamed_response_wrapper(
            auth.get_token,
        )
        self.refresh_token = to_streamed_response_wrapper(
            auth.refresh_token,
        )

    @cached_property
    def mcp_tokens(self) -> McpTokensResourceWithStreamingResponse:
        return McpTokensResourceWithStreamingResponse(self._auth.mcp_tokens)


class AsyncAuthResourceWithStreamingResponse:
    def __init__(self, auth: AsyncAuthResource) -> None:
        self._auth = auth

        self.get_token = async_to_streamed_response_wrapper(
            auth.get_token,
        )
        self.refresh_token = async_to_streamed_response_wrapper(
            auth.refresh_token,
        )

    @cached_property
    def mcp_tokens(self) -> AsyncMcpTokensResourceWithStreamingResponse:
        return AsyncMcpTokensResourceWithStreamingResponse(self._auth.mcp_tokens)
