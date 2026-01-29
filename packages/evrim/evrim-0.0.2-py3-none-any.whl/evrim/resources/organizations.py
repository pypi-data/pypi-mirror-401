# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ..types import SortOrder, OrganizationSortField, organization_list_params, organization_list_meetings_params
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
from ..types.sort_order import SortOrder
from ..types.organization import Organization
from ..types.organization_sort_field import OrganizationSortField
from ..types.organization_list_response import OrganizationListResponse
from ..types.organization_list_meetings_response import OrganizationListMeetingsResponse

__all__ = ["OrganizationsResource", "AsyncOrganizationsResource"]


class OrganizationsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> OrganizationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return OrganizationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> OrganizationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return OrganizationsResourceWithStreamingResponse(self)

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
    ) -> Organization:
        """
        Get detailed information about a specific organization.

        Returns comprehensive organization data including all names, types, countries,
        and total number of meetings the organization has participated in.

        **Authentication:** Required

        **Path Parameters:**

        - `id`: UUID of the organization

        **Response Fields:**

        - Multiple names (original language and English)
        - Organization types
        - Associated countries
        - Meeting participation count

        **Response Codes:**

        - 200: Success
        - 404: Organization not found
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
            f"/organizations/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Organization,
        )

    def list(
        self,
        *,
        end: int | Omit = omit,
        sort_by: Optional[OrganizationSortField] | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        start: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrganizationListResponse:
        """
        Get paginated list of organizations.

        Returns organizations that have been involved in meetings, including their names
        (Chinese and English), types, countries, and meeting counts.

        **Authentication:** Required

        **Query Parameters:**

        - `start`: Starting index for pagination (default: 0)

          - `end`: Ending index for pagination (default: 9)
          - `sort_by`: Field to sort by (default: None).
          - `sort_order`: Sort order (default: asc). Only available if `sort_by` is
            provided.

          **Organization Fields:**

          - Names in multiple languages
          - Organization types (government, corporate, NGO, etc.)
          - Associated countries
          - Total meeting participation count

          **Example Response:**

          ```json
          [
            {
              "id": "uuid",
              "names": ["组织名称"],
              "name_english": "Organization Name",
              "types": ["Government"],
              "countries": ["China"],
              "meeting_count": 15
            }
          ]
          ```

        Args:
          end: End index for pagination

          sort_by: Fields available for sorting organizations

          sort_order: Sort order

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/organizations",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "end": end,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "start": start,
                    },
                    organization_list_params.OrganizationListParams,
                ),
            ),
            cast_to=OrganizationListResponse,
        )

    def list_meetings(
        self,
        id: str,
        *,
        end: int | Omit = omit,
        start: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrganizationListMeetingsResponse:
        """
        Get all meetings associated with a specific organization.

        Returns a paginated list of all meetings where this organization was involved,
        including complete meeting details with participants, other organizations,
        locations, and source documents.

        **Authentication:** Required

        **Path Parameters:**

        - `id`: UUID of the organization

        **Query Parameters:**

        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)

        **Response:** Returns list of MeetingDetails objects with full meeting
        information including all participants and related entities.

        **Response Codes:**

        - 200: Success (empty list if organization has no meetings)
        - 401: Unauthorized

        Args:
          end: End index for pagination

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/organizations/{id}/meetings",
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
                    organization_list_meetings_params.OrganizationListMeetingsParams,
                ),
            ),
            cast_to=OrganizationListMeetingsResponse,
        )


class AsyncOrganizationsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncOrganizationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return AsyncOrganizationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOrganizationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return AsyncOrganizationsResourceWithStreamingResponse(self)

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
    ) -> Organization:
        """
        Get detailed information about a specific organization.

        Returns comprehensive organization data including all names, types, countries,
        and total number of meetings the organization has participated in.

        **Authentication:** Required

        **Path Parameters:**

        - `id`: UUID of the organization

        **Response Fields:**

        - Multiple names (original language and English)
        - Organization types
        - Associated countries
        - Meeting participation count

        **Response Codes:**

        - 200: Success
        - 404: Organization not found
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
            f"/organizations/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Organization,
        )

    async def list(
        self,
        *,
        end: int | Omit = omit,
        sort_by: Optional[OrganizationSortField] | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        start: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrganizationListResponse:
        """
        Get paginated list of organizations.

        Returns organizations that have been involved in meetings, including their names
        (Chinese and English), types, countries, and meeting counts.

        **Authentication:** Required

        **Query Parameters:**

        - `start`: Starting index for pagination (default: 0)

          - `end`: Ending index for pagination (default: 9)
          - `sort_by`: Field to sort by (default: None).
          - `sort_order`: Sort order (default: asc). Only available if `sort_by` is
            provided.

          **Organization Fields:**

          - Names in multiple languages
          - Organization types (government, corporate, NGO, etc.)
          - Associated countries
          - Total meeting participation count

          **Example Response:**

          ```json
          [
            {
              "id": "uuid",
              "names": ["组织名称"],
              "name_english": "Organization Name",
              "types": ["Government"],
              "countries": ["China"],
              "meeting_count": 15
            }
          ]
          ```

        Args:
          end: End index for pagination

          sort_by: Fields available for sorting organizations

          sort_order: Sort order

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/organizations",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "end": end,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "start": start,
                    },
                    organization_list_params.OrganizationListParams,
                ),
            ),
            cast_to=OrganizationListResponse,
        )

    async def list_meetings(
        self,
        id: str,
        *,
        end: int | Omit = omit,
        start: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> OrganizationListMeetingsResponse:
        """
        Get all meetings associated with a specific organization.

        Returns a paginated list of all meetings where this organization was involved,
        including complete meeting details with participants, other organizations,
        locations, and source documents.

        **Authentication:** Required

        **Path Parameters:**

        - `id`: UUID of the organization

        **Query Parameters:**

        - `start`: Starting index for pagination (default: 0)
        - `end`: Ending index for pagination (default: 9)

        **Response:** Returns list of MeetingDetails objects with full meeting
        information including all participants and related entities.

        **Response Codes:**

        - 200: Success (empty list if organization has no meetings)
        - 401: Unauthorized

        Args:
          end: End index for pagination

          start: Start index for pagination

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/organizations/{id}/meetings",
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
                    organization_list_meetings_params.OrganizationListMeetingsParams,
                ),
            ),
            cast_to=OrganizationListMeetingsResponse,
        )


class OrganizationsResourceWithRawResponse:
    def __init__(self, organizations: OrganizationsResource) -> None:
        self._organizations = organizations

        self.retrieve = to_raw_response_wrapper(
            organizations.retrieve,
        )
        self.list = to_raw_response_wrapper(
            organizations.list,
        )
        self.list_meetings = to_raw_response_wrapper(
            organizations.list_meetings,
        )


class AsyncOrganizationsResourceWithRawResponse:
    def __init__(self, organizations: AsyncOrganizationsResource) -> None:
        self._organizations = organizations

        self.retrieve = async_to_raw_response_wrapper(
            organizations.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            organizations.list,
        )
        self.list_meetings = async_to_raw_response_wrapper(
            organizations.list_meetings,
        )


class OrganizationsResourceWithStreamingResponse:
    def __init__(self, organizations: OrganizationsResource) -> None:
        self._organizations = organizations

        self.retrieve = to_streamed_response_wrapper(
            organizations.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            organizations.list,
        )
        self.list_meetings = to_streamed_response_wrapper(
            organizations.list_meetings,
        )


class AsyncOrganizationsResourceWithStreamingResponse:
    def __init__(self, organizations: AsyncOrganizationsResource) -> None:
        self._organizations = organizations

        self.retrieve = async_to_streamed_response_wrapper(
            organizations.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            organizations.list,
        )
        self.list_meetings = async_to_streamed_response_wrapper(
            organizations.list_meetings,
        )
