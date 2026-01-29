# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .graph import (
    GraphResource,
    AsyncGraphResource,
    GraphResourceWithRawResponse,
    AsyncGraphResourceWithRawResponse,
    GraphResourceWithStreamingResponse,
    AsyncGraphResourceWithStreamingResponse,
)
from .topics import (
    TopicsResource,
    AsyncTopicsResource,
    TopicsResourceWithRawResponse,
    AsyncTopicsResourceWithRawResponse,
    TopicsResourceWithStreamingResponse,
    AsyncTopicsResourceWithStreamingResponse,
)
from .meetings import (
    MeetingsResource,
    AsyncMeetingsResource,
    MeetingsResourceWithRawResponse,
    AsyncMeetingsResourceWithRawResponse,
    MeetingsResourceWithStreamingResponse,
    AsyncMeetingsResourceWithStreamingResponse,
)
from ..._compat import cached_property
from .analytics import (
    AnalyticsResource,
    AsyncAnalyticsResource,
    AnalyticsResourceWithRawResponse,
    AsyncAnalyticsResourceWithRawResponse,
    AnalyticsResourceWithStreamingResponse,
    AsyncAnalyticsResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from .communities import (
    CommunitiesResource,
    AsyncCommunitiesResource,
    CommunitiesResourceWithRawResponse,
    AsyncCommunitiesResourceWithRawResponse,
    CommunitiesResourceWithStreamingResponse,
    AsyncCommunitiesResourceWithStreamingResponse,
)
from .publications import (
    PublicationsResource,
    AsyncPublicationsResource,
    PublicationsResourceWithRawResponse,
    AsyncPublicationsResourceWithRawResponse,
    PublicationsResourceWithStreamingResponse,
    AsyncPublicationsResourceWithStreamingResponse,
)

__all__ = ["TechnologyResource", "AsyncTechnologyResource"]


class TechnologyResource(SyncAPIResource):
    @cached_property
    def communities(self) -> CommunitiesResource:
        return CommunitiesResource(self._client)

    @cached_property
    def topics(self) -> TopicsResource:
        return TopicsResource(self._client)

    @cached_property
    def publications(self) -> PublicationsResource:
        return PublicationsResource(self._client)

    @cached_property
    def graph(self) -> GraphResource:
        return GraphResource(self._client)

    @cached_property
    def analytics(self) -> AnalyticsResource:
        return AnalyticsResource(self._client)

    @cached_property
    def meetings(self) -> MeetingsResource:
        return MeetingsResource(self._client)

    @cached_property
    def with_raw_response(self) -> TechnologyResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return TechnologyResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TechnologyResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return TechnologyResourceWithStreamingResponse(self)


class AsyncTechnologyResource(AsyncAPIResource):
    @cached_property
    def communities(self) -> AsyncCommunitiesResource:
        return AsyncCommunitiesResource(self._client)

    @cached_property
    def topics(self) -> AsyncTopicsResource:
        return AsyncTopicsResource(self._client)

    @cached_property
    def publications(self) -> AsyncPublicationsResource:
        return AsyncPublicationsResource(self._client)

    @cached_property
    def graph(self) -> AsyncGraphResource:
        return AsyncGraphResource(self._client)

    @cached_property
    def analytics(self) -> AsyncAnalyticsResource:
        return AsyncAnalyticsResource(self._client)

    @cached_property
    def meetings(self) -> AsyncMeetingsResource:
        return AsyncMeetingsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncTechnologyResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTechnologyResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTechnologyResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return AsyncTechnologyResourceWithStreamingResponse(self)


class TechnologyResourceWithRawResponse:
    def __init__(self, technology: TechnologyResource) -> None:
        self._technology = technology

    @cached_property
    def communities(self) -> CommunitiesResourceWithRawResponse:
        return CommunitiesResourceWithRawResponse(self._technology.communities)

    @cached_property
    def topics(self) -> TopicsResourceWithRawResponse:
        return TopicsResourceWithRawResponse(self._technology.topics)

    @cached_property
    def publications(self) -> PublicationsResourceWithRawResponse:
        return PublicationsResourceWithRawResponse(self._technology.publications)

    @cached_property
    def graph(self) -> GraphResourceWithRawResponse:
        return GraphResourceWithRawResponse(self._technology.graph)

    @cached_property
    def analytics(self) -> AnalyticsResourceWithRawResponse:
        return AnalyticsResourceWithRawResponse(self._technology.analytics)

    @cached_property
    def meetings(self) -> MeetingsResourceWithRawResponse:
        return MeetingsResourceWithRawResponse(self._technology.meetings)


class AsyncTechnologyResourceWithRawResponse:
    def __init__(self, technology: AsyncTechnologyResource) -> None:
        self._technology = technology

    @cached_property
    def communities(self) -> AsyncCommunitiesResourceWithRawResponse:
        return AsyncCommunitiesResourceWithRawResponse(self._technology.communities)

    @cached_property
    def topics(self) -> AsyncTopicsResourceWithRawResponse:
        return AsyncTopicsResourceWithRawResponse(self._technology.topics)

    @cached_property
    def publications(self) -> AsyncPublicationsResourceWithRawResponse:
        return AsyncPublicationsResourceWithRawResponse(self._technology.publications)

    @cached_property
    def graph(self) -> AsyncGraphResourceWithRawResponse:
        return AsyncGraphResourceWithRawResponse(self._technology.graph)

    @cached_property
    def analytics(self) -> AsyncAnalyticsResourceWithRawResponse:
        return AsyncAnalyticsResourceWithRawResponse(self._technology.analytics)

    @cached_property
    def meetings(self) -> AsyncMeetingsResourceWithRawResponse:
        return AsyncMeetingsResourceWithRawResponse(self._technology.meetings)


class TechnologyResourceWithStreamingResponse:
    def __init__(self, technology: TechnologyResource) -> None:
        self._technology = technology

    @cached_property
    def communities(self) -> CommunitiesResourceWithStreamingResponse:
        return CommunitiesResourceWithStreamingResponse(self._technology.communities)

    @cached_property
    def topics(self) -> TopicsResourceWithStreamingResponse:
        return TopicsResourceWithStreamingResponse(self._technology.topics)

    @cached_property
    def publications(self) -> PublicationsResourceWithStreamingResponse:
        return PublicationsResourceWithStreamingResponse(self._technology.publications)

    @cached_property
    def graph(self) -> GraphResourceWithStreamingResponse:
        return GraphResourceWithStreamingResponse(self._technology.graph)

    @cached_property
    def analytics(self) -> AnalyticsResourceWithStreamingResponse:
        return AnalyticsResourceWithStreamingResponse(self._technology.analytics)

    @cached_property
    def meetings(self) -> MeetingsResourceWithStreamingResponse:
        return MeetingsResourceWithStreamingResponse(self._technology.meetings)


class AsyncTechnologyResourceWithStreamingResponse:
    def __init__(self, technology: AsyncTechnologyResource) -> None:
        self._technology = technology

    @cached_property
    def communities(self) -> AsyncCommunitiesResourceWithStreamingResponse:
        return AsyncCommunitiesResourceWithStreamingResponse(self._technology.communities)

    @cached_property
    def topics(self) -> AsyncTopicsResourceWithStreamingResponse:
        return AsyncTopicsResourceWithStreamingResponse(self._technology.topics)

    @cached_property
    def publications(self) -> AsyncPublicationsResourceWithStreamingResponse:
        return AsyncPublicationsResourceWithStreamingResponse(self._technology.publications)

    @cached_property
    def graph(self) -> AsyncGraphResourceWithStreamingResponse:
        return AsyncGraphResourceWithStreamingResponse(self._technology.graph)

    @cached_property
    def analytics(self) -> AsyncAnalyticsResourceWithStreamingResponse:
        return AsyncAnalyticsResourceWithStreamingResponse(self._technology.analytics)

    @cached_property
    def meetings(self) -> AsyncMeetingsResourceWithStreamingResponse:
        return AsyncMeetingsResourceWithStreamingResponse(self._technology.meetings)
