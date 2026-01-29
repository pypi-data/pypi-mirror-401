# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

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
from ...types.chat import message_send_params
from ..._base_client import make_request_options
from ...types.chat.message import Message

__all__ = ["MessagesResource", "AsyncMessagesResource"]


class MessagesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> MessagesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return MessagesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MessagesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return MessagesResourceWithStreamingResponse(self)

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
    ) -> Message:
        """
        Get a specific message by ID.

        Returns complete message details including sender information and any associated
        response. Users can only access messages from their own sessions.

        **Authentication:** Required

        **Path Parameters:**

        - `id`: UUID of the message

        **Returns:** Message object with sender and response details

        **Response Codes:**

        - 200: Success
        - 401: Unauthorized
        - 403: Forbidden (message belongs to another user's session)
        - 404: Message not found

        **Example:**

        ```
        GET /chat/messages/123e4567-e89b-12d3-a456-426614174000
        ```

        **Security:** The system verifies that the message's session belongs to the
        authenticated user before returning the message.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/chat/messages/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Message,
        )

    def send(
        self,
        *,
        message: str,
        session_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Message:
        """
        Send a message and start async agent processing.

        This endpoint returns immediately with the message in 'pending' status. Use GET
        /chat/messages/{id} to poll for completion.

        This endpoint supports two flows:

        1. **New session** (no session_id): Creates message with null session_id,
           background task creates session after agent responds
        2. **Continue session** (with session_id): Creates message linked to session,
           background task processes and updates status

        **Polling Behavior:** Messages are created with status='pending'. The workflow
        runs asynchronously and:

        - Updates status to 'running' when processing starts
        - Updates status to 'completed' or 'failed' when done
        - For new sessions: session_id will be null initially, then populated after
          completion
        - For existing sessions: session_id is set immediately

        Client should poll GET /chat/messages/{id} until status is 'completed' or
        'failed'. Expected completion time: 2-30 seconds depending on Bedrock AgentCore
        response time.

        **Authentication:** Required **Rate Limit:** 60 requests/minute

        **Request Body:**

        - message: User's message content (required)
        - session_id: Claude session ID (optional, for continuing conversation)

        **Returns:** Message object with status='pending' (poll GET /chat/messages/{id}
        for updates)

        **Response Codes:**

        - 202: Message accepted for processing
        - 400: Invalid request
        - 401: Unauthorized
        - 403: Forbidden (session belongs to another user)
        - 404: Session not found
        - 429: Rate limit exceeded

        **Example Request (New Session):**

        ```json
        {
          "message": "What meetings happened in Beijing last month?"
        }
        ```

        **Example Request (Continue Session):**

        ```json
        {
          "session_id": "123e4567-e89b-12d3-a456-426614174000",
          "message": "Tell me more about the first one"
        }
        ```

        **Example Response (Immediate):**

        ```json
        {
          "id": "msg-uuid",
          "session_id": null,
          "sender": {
            "id": "user-uuid",
            "email": "user@example.com"
          },
          "content": "What meetings happened in Beijing last month?",
          "timestamp": "2024-01-15T10:00:00Z",
          "status": "pending",
          "error_message": null,
          "response": null
        }
        ```

        **Polling Response (After Completion):**

        ```json
        {
          "id": "msg-uuid",
          "session_id": "session-uuid",
          "sender": {...},
          "content": "What meetings happened in Beijing last month?",
          "timestamp": "2024-01-15T10:00:00Z",
          "status": "completed",
          "error_message": null,
          "response": {
            "id": "resp-uuid",
            "success": true,
            "content": "{\"session_id\": \"session-123\", ...}",
            "created_at": "2024-01-15T10:00:01Z"
          }
        }
        ```

        Args:
          message: User's message content

          session_id: Claude session ID for continuing conversation

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/chat/messages",
            body=maybe_transform(
                {
                    "message": message,
                    "session_id": session_id,
                },
                message_send_params.MessageSendParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Message,
        )


class AsyncMessagesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMessagesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return AsyncMessagesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMessagesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return AsyncMessagesResourceWithStreamingResponse(self)

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
    ) -> Message:
        """
        Get a specific message by ID.

        Returns complete message details including sender information and any associated
        response. Users can only access messages from their own sessions.

        **Authentication:** Required

        **Path Parameters:**

        - `id`: UUID of the message

        **Returns:** Message object with sender and response details

        **Response Codes:**

        - 200: Success
        - 401: Unauthorized
        - 403: Forbidden (message belongs to another user's session)
        - 404: Message not found

        **Example:**

        ```
        GET /chat/messages/123e4567-e89b-12d3-a456-426614174000
        ```

        **Security:** The system verifies that the message's session belongs to the
        authenticated user before returning the message.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/chat/messages/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Message,
        )

    async def send(
        self,
        *,
        message: str,
        session_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Message:
        """
        Send a message and start async agent processing.

        This endpoint returns immediately with the message in 'pending' status. Use GET
        /chat/messages/{id} to poll for completion.

        This endpoint supports two flows:

        1. **New session** (no session_id): Creates message with null session_id,
           background task creates session after agent responds
        2. **Continue session** (with session_id): Creates message linked to session,
           background task processes and updates status

        **Polling Behavior:** Messages are created with status='pending'. The workflow
        runs asynchronously and:

        - Updates status to 'running' when processing starts
        - Updates status to 'completed' or 'failed' when done
        - For new sessions: session_id will be null initially, then populated after
          completion
        - For existing sessions: session_id is set immediately

        Client should poll GET /chat/messages/{id} until status is 'completed' or
        'failed'. Expected completion time: 2-30 seconds depending on Bedrock AgentCore
        response time.

        **Authentication:** Required **Rate Limit:** 60 requests/minute

        **Request Body:**

        - message: User's message content (required)
        - session_id: Claude session ID (optional, for continuing conversation)

        **Returns:** Message object with status='pending' (poll GET /chat/messages/{id}
        for updates)

        **Response Codes:**

        - 202: Message accepted for processing
        - 400: Invalid request
        - 401: Unauthorized
        - 403: Forbidden (session belongs to another user)
        - 404: Session not found
        - 429: Rate limit exceeded

        **Example Request (New Session):**

        ```json
        {
          "message": "What meetings happened in Beijing last month?"
        }
        ```

        **Example Request (Continue Session):**

        ```json
        {
          "session_id": "123e4567-e89b-12d3-a456-426614174000",
          "message": "Tell me more about the first one"
        }
        ```

        **Example Response (Immediate):**

        ```json
        {
          "id": "msg-uuid",
          "session_id": null,
          "sender": {
            "id": "user-uuid",
            "email": "user@example.com"
          },
          "content": "What meetings happened in Beijing last month?",
          "timestamp": "2024-01-15T10:00:00Z",
          "status": "pending",
          "error_message": null,
          "response": null
        }
        ```

        **Polling Response (After Completion):**

        ```json
        {
          "id": "msg-uuid",
          "session_id": "session-uuid",
          "sender": {...},
          "content": "What meetings happened in Beijing last month?",
          "timestamp": "2024-01-15T10:00:00Z",
          "status": "completed",
          "error_message": null,
          "response": {
            "id": "resp-uuid",
            "success": true,
            "content": "{\"session_id\": \"session-123\", ...}",
            "created_at": "2024-01-15T10:00:01Z"
          }
        }
        ```

        Args:
          message: User's message content

          session_id: Claude session ID for continuing conversation

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/chat/messages",
            body=await async_maybe_transform(
                {
                    "message": message,
                    "session_id": session_id,
                },
                message_send_params.MessageSendParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Message,
        )


class MessagesResourceWithRawResponse:
    def __init__(self, messages: MessagesResource) -> None:
        self._messages = messages

        self.retrieve = to_raw_response_wrapper(
            messages.retrieve,
        )
        self.send = to_raw_response_wrapper(
            messages.send,
        )


class AsyncMessagesResourceWithRawResponse:
    def __init__(self, messages: AsyncMessagesResource) -> None:
        self._messages = messages

        self.retrieve = async_to_raw_response_wrapper(
            messages.retrieve,
        )
        self.send = async_to_raw_response_wrapper(
            messages.send,
        )


class MessagesResourceWithStreamingResponse:
    def __init__(self, messages: MessagesResource) -> None:
        self._messages = messages

        self.retrieve = to_streamed_response_wrapper(
            messages.retrieve,
        )
        self.send = to_streamed_response_wrapper(
            messages.send,
        )


class AsyncMessagesResourceWithStreamingResponse:
    def __init__(self, messages: AsyncMessagesResource) -> None:
        self._messages = messages

        self.retrieve = async_to_streamed_response_wrapper(
            messages.retrieve,
        )
        self.send = async_to_streamed_response_wrapper(
            messages.send,
        )
