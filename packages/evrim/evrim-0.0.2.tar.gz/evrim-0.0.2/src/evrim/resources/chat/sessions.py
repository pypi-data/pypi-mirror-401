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
from ...types.chat import session_list_params, session_get_messages_params
from ..._base_client import make_request_options
from ...types.chat.session import Session
from ...types.chat.session_list_response import SessionListResponse
from ...types.chat.session_get_messages_response import SessionGetMessagesResponse

__all__ = ["SessionsResource", "AsyncSessionsResource"]


class SessionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SessionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return SessionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SessionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return SessionsResourceWithStreamingResponse(self)

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
    ) -> Session:
        """
        Get a specific session by ID.

        Returns complete session details including all messages and their responses.
        Users can only access their own sessions.

        **Authentication:** Required

        **Path Parameters:**

        - `id`: UUID of the session (Claude agent session ID)

        **Returns:** Session object with all messages

        **Response Codes:**

        - 200: Success
        - 401: Unauthorized
        - 403: Forbidden (session belongs to another user)
        - 404: Session not found

        **Example:**

        ```
        GET /chat/sessions/123e4567-e89b-12d3-a456-426614174000
        ```

        **Security:** Users can only access sessions they own. Attempting to access
        another user's session will result in a 403 Forbidden error.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/chat/sessions/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Session,
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
    ) -> SessionListResponse:
        """
        Get paginated list of sessions for the authenticated user.

        Returns all sessions for the authenticated user, ordered by most recent first.
        Each session includes all associated messages with their responses.

        **Authentication:** Required

        **Query Parameters:**

        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)

        **Returns:** List of Conversation objects with complete message history

        **Response Codes:**

        - 200: Success
        - 401: Unauthorized

        **Example:**

        ```
        GET /chat/conversations?start=0&end=9
        ```

        **Response Example:**

        ```json
        [
          {
            "id": "uuid",
            "user": {
              "id": "user-uuid",
              "email": "user@example.com"
            },
            "messages": [...],
            "created_at": "2024-01-15T10:00:00Z"
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
            "/chat/sessions",
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
                    session_list_params.SessionListParams,
                ),
            ),
            cast_to=SessionListResponse,
        )

    def delete(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Delete a session and all associated messages and responses.

        Permanently deletes a session along with all its messages and responses. This
        operation cannot be undone. Users can only delete their own sessions.

        **Authentication:** Required

        **Path Parameters:**

        - `id`: UUID of the session to delete

        **Returns:** Success message with deleted session ID

        **Response Codes:**

        - 200: Successfully deleted
        - 401: Unauthorized
        - 403: Forbidden (session belongs to another user)
        - 404: Session not found
        - 500: Internal server error during deletion

        **Example:**

        ```
        DELETE /chat/sessions/123e4567-e89b-12d3-a456-426614174000
        ```

        **Example Response:**

        ```json
        {
          "message": "Session deleted successfully",
          "session_id": "123e4567-e89b-12d3-a456-426614174000"
        }
        ```

        **Security:** Users can only delete sessions they own. The system verifies
        session ownership before performing the deletion. All associated messages and
        responses are automatically deleted through cascading database operations.

        **Warning:** This operation is irreversible. All conversation history in the
        session will be permanently deleted.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._delete(
            f"/chat/sessions/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def get_messages(
        self,
        session_id: str,
        *,
        end: int | Omit = omit,
        start: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionGetMessagesResponse:
        """
        Get all messages in a specific session.

        Returns messages ordered chronologically (oldest first). Each message includes
        the sender information and any associated response.

        **Authentication:** Required

        **Path Parameters:**

        - `session_id`: UUID of the session (Claude agent session ID)

        **Query Parameters:**

        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 99)

        **Returns:** List of Message objects ordered by timestamp

        **Response Codes:**

        - 200: Success
        - 401: Unauthorized
        - 403: Forbidden (session belongs to another user)
        - 404: Session not found

        **Example:**

        ```
        GET /chat/sessions/{id}/messages?start=0&end=99
        ```

        **Response Example:**

        ```json
        [
          {
            "id": "msg-uuid",
            "sender": {
              "id": "user-uuid",
              "email": "user@example.com"
            },
            "content": "Hello, this is a message",
            "timestamp": "2024-01-15T10:00:00Z",
            "response": {
              "id": "resp-uuid",
              "success": true,
              "content": "Response content"
            }
          }
        ]
        ```

        **Security:** Users can only access messages from sessions they own.

        Args:
          end: End index for pagination

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return self._get(
            f"/chat/sessions/{session_id}/messages",
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
                    session_get_messages_params.SessionGetMessagesParams,
                ),
            ),
            cast_to=SessionGetMessagesResponse,
        )


class AsyncSessionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSessionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSessionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSessionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return AsyncSessionsResourceWithStreamingResponse(self)

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
    ) -> Session:
        """
        Get a specific session by ID.

        Returns complete session details including all messages and their responses.
        Users can only access their own sessions.

        **Authentication:** Required

        **Path Parameters:**

        - `id`: UUID of the session (Claude agent session ID)

        **Returns:** Session object with all messages

        **Response Codes:**

        - 200: Success
        - 401: Unauthorized
        - 403: Forbidden (session belongs to another user)
        - 404: Session not found

        **Example:**

        ```
        GET /chat/sessions/123e4567-e89b-12d3-a456-426614174000
        ```

        **Security:** Users can only access sessions they own. Attempting to access
        another user's session will result in a 403 Forbidden error.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/chat/sessions/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Session,
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
    ) -> SessionListResponse:
        """
        Get paginated list of sessions for the authenticated user.

        Returns all sessions for the authenticated user, ordered by most recent first.
        Each session includes all associated messages with their responses.

        **Authentication:** Required

        **Query Parameters:**

        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)

        **Returns:** List of Conversation objects with complete message history

        **Response Codes:**

        - 200: Success
        - 401: Unauthorized

        **Example:**

        ```
        GET /chat/conversations?start=0&end=9
        ```

        **Response Example:**

        ```json
        [
          {
            "id": "uuid",
            "user": {
              "id": "user-uuid",
              "email": "user@example.com"
            },
            "messages": [...],
            "created_at": "2024-01-15T10:00:00Z"
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
            "/chat/sessions",
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
                    session_list_params.SessionListParams,
                ),
            ),
            cast_to=SessionListResponse,
        )

    async def delete(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Delete a session and all associated messages and responses.

        Permanently deletes a session along with all its messages and responses. This
        operation cannot be undone. Users can only delete their own sessions.

        **Authentication:** Required

        **Path Parameters:**

        - `id`: UUID of the session to delete

        **Returns:** Success message with deleted session ID

        **Response Codes:**

        - 200: Successfully deleted
        - 401: Unauthorized
        - 403: Forbidden (session belongs to another user)
        - 404: Session not found
        - 500: Internal server error during deletion

        **Example:**

        ```
        DELETE /chat/sessions/123e4567-e89b-12d3-a456-426614174000
        ```

        **Example Response:**

        ```json
        {
          "message": "Session deleted successfully",
          "session_id": "123e4567-e89b-12d3-a456-426614174000"
        }
        ```

        **Security:** Users can only delete sessions they own. The system verifies
        session ownership before performing the deletion. All associated messages and
        responses are automatically deleted through cascading database operations.

        **Warning:** This operation is irreversible. All conversation history in the
        session will be permanently deleted.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._delete(
            f"/chat/sessions/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def get_messages(
        self,
        session_id: str,
        *,
        end: int | Omit = omit,
        start: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionGetMessagesResponse:
        """
        Get all messages in a specific session.

        Returns messages ordered chronologically (oldest first). Each message includes
        the sender information and any associated response.

        **Authentication:** Required

        **Path Parameters:**

        - `session_id`: UUID of the session (Claude agent session ID)

        **Query Parameters:**

        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 99)

        **Returns:** List of Message objects ordered by timestamp

        **Response Codes:**

        - 200: Success
        - 401: Unauthorized
        - 403: Forbidden (session belongs to another user)
        - 404: Session not found

        **Example:**

        ```
        GET /chat/sessions/{id}/messages?start=0&end=99
        ```

        **Response Example:**

        ```json
        [
          {
            "id": "msg-uuid",
            "sender": {
              "id": "user-uuid",
              "email": "user@example.com"
            },
            "content": "Hello, this is a message",
            "timestamp": "2024-01-15T10:00:00Z",
            "response": {
              "id": "resp-uuid",
              "success": true,
              "content": "Response content"
            }
          }
        ]
        ```

        **Security:** Users can only access messages from sessions they own.

        Args:
          end: End index for pagination

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return await self._get(
            f"/chat/sessions/{session_id}/messages",
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
                    session_get_messages_params.SessionGetMessagesParams,
                ),
            ),
            cast_to=SessionGetMessagesResponse,
        )


class SessionsResourceWithRawResponse:
    def __init__(self, sessions: SessionsResource) -> None:
        self._sessions = sessions

        self.retrieve = to_raw_response_wrapper(
            sessions.retrieve,
        )
        self.list = to_raw_response_wrapper(
            sessions.list,
        )
        self.delete = to_raw_response_wrapper(
            sessions.delete,
        )
        self.get_messages = to_raw_response_wrapper(
            sessions.get_messages,
        )


class AsyncSessionsResourceWithRawResponse:
    def __init__(self, sessions: AsyncSessionsResource) -> None:
        self._sessions = sessions

        self.retrieve = async_to_raw_response_wrapper(
            sessions.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            sessions.list,
        )
        self.delete = async_to_raw_response_wrapper(
            sessions.delete,
        )
        self.get_messages = async_to_raw_response_wrapper(
            sessions.get_messages,
        )


class SessionsResourceWithStreamingResponse:
    def __init__(self, sessions: SessionsResource) -> None:
        self._sessions = sessions

        self.retrieve = to_streamed_response_wrapper(
            sessions.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            sessions.list,
        )
        self.delete = to_streamed_response_wrapper(
            sessions.delete,
        )
        self.get_messages = to_streamed_response_wrapper(
            sessions.get_messages,
        )


class AsyncSessionsResourceWithStreamingResponse:
    def __init__(self, sessions: AsyncSessionsResource) -> None:
        self._sessions = sessions

        self.retrieve = async_to_streamed_response_wrapper(
            sessions.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            sessions.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            sessions.delete,
        )
        self.get_messages = async_to_streamed_response_wrapper(
            sessions.get_messages,
        )
