# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import relationship_list_params
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
from ..types.relationship import Relationship
from ..types.relationship_list_response import RelationshipListResponse

__all__ = ["RelationshipsResource", "AsyncRelationshipsResource"]


class RelationshipsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> RelationshipsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return RelationshipsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RelationshipsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return RelationshipsResourceWithStreamingResponse(self)

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
    ) -> Relationship:
        """
        Get detailed information about a specific relationship.

        Returns complete relationship data including the participants involved, meeting
        context, relationship type, and purpose.

        **Authentication:** Required

        **Path Parameters:**

        - `id`: UUID of the relationship

        **Response Fields:**

        - Meeting ID where the relationship occurred
        - From/To participant IDs
        - Relationship type
        - Purpose or goal of the interaction
        - Creation timestamp

        **Use Cases:**

        - Analyze specific participant interactions
        - Build relationship graphs
        - Understand meeting dynamics
        - Track collaboration patterns

        **Response Codes:**

        - 200: Success
        - 404: Relationship not found
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
            f"/relationships/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Relationship,
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
    ) -> RelationshipListResponse:
        """
        Get paginated list of relationships between participants.

        Returns relationships that capture interactions and connections between
        participants in meetings, including relationship types and purposes.

        **Authentication:** Required

        **Query Parameters:**

        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)

        **Relationship Fields:**

        - Meeting ID: Which meeting this relationship occurred in
        - From/To Participant IDs: The participants involved
        - Relationship Type: Nature of the relationship
        - Purpose: Goal or reason for the interaction
        - Timestamps

        **Use Cases:**

        - Social network analysis
        - Mapping participant connections
        - Understanding meeting dynamics
        - Identifying key relationships and interactions

        **Example Response:**

        ```json
        [
          {
            "id": "uuid",
            "meeting_id": "meeting-uuid",
            "from_participant_id": "participant1-uuid",
            "to_participant_id": "participant2-uuid",
            "relationship_type": "collaboration",
            "purpose": "Joint project discussion"
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
            "/relationships",
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
                    relationship_list_params.RelationshipListParams,
                ),
            ),
            cast_to=RelationshipListResponse,
        )


class AsyncRelationshipsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncRelationshipsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return AsyncRelationshipsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRelationshipsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return AsyncRelationshipsResourceWithStreamingResponse(self)

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
    ) -> Relationship:
        """
        Get detailed information about a specific relationship.

        Returns complete relationship data including the participants involved, meeting
        context, relationship type, and purpose.

        **Authentication:** Required

        **Path Parameters:**

        - `id`: UUID of the relationship

        **Response Fields:**

        - Meeting ID where the relationship occurred
        - From/To participant IDs
        - Relationship type
        - Purpose or goal of the interaction
        - Creation timestamp

        **Use Cases:**

        - Analyze specific participant interactions
        - Build relationship graphs
        - Understand meeting dynamics
        - Track collaboration patterns

        **Response Codes:**

        - 200: Success
        - 404: Relationship not found
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
            f"/relationships/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Relationship,
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
    ) -> RelationshipListResponse:
        """
        Get paginated list of relationships between participants.

        Returns relationships that capture interactions and connections between
        participants in meetings, including relationship types and purposes.

        **Authentication:** Required

        **Query Parameters:**

        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)

        **Relationship Fields:**

        - Meeting ID: Which meeting this relationship occurred in
        - From/To Participant IDs: The participants involved
        - Relationship Type: Nature of the relationship
        - Purpose: Goal or reason for the interaction
        - Timestamps

        **Use Cases:**

        - Social network analysis
        - Mapping participant connections
        - Understanding meeting dynamics
        - Identifying key relationships and interactions

        **Example Response:**

        ```json
        [
          {
            "id": "uuid",
            "meeting_id": "meeting-uuid",
            "from_participant_id": "participant1-uuid",
            "to_participant_id": "participant2-uuid",
            "relationship_type": "collaboration",
            "purpose": "Joint project discussion"
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
            "/relationships",
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
                    relationship_list_params.RelationshipListParams,
                ),
            ),
            cast_to=RelationshipListResponse,
        )


class RelationshipsResourceWithRawResponse:
    def __init__(self, relationships: RelationshipsResource) -> None:
        self._relationships = relationships

        self.retrieve = to_raw_response_wrapper(
            relationships.retrieve,
        )
        self.list = to_raw_response_wrapper(
            relationships.list,
        )


class AsyncRelationshipsResourceWithRawResponse:
    def __init__(self, relationships: AsyncRelationshipsResource) -> None:
        self._relationships = relationships

        self.retrieve = async_to_raw_response_wrapper(
            relationships.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            relationships.list,
        )


class RelationshipsResourceWithStreamingResponse:
    def __init__(self, relationships: RelationshipsResource) -> None:
        self._relationships = relationships

        self.retrieve = to_streamed_response_wrapper(
            relationships.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            relationships.list,
        )


class AsyncRelationshipsResourceWithStreamingResponse:
    def __init__(self, relationships: AsyncRelationshipsResource) -> None:
        self._relationships = relationships

        self.retrieve = async_to_streamed_response_wrapper(
            relationships.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            relationships.list,
        )
