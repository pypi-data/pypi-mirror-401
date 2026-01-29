# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Mapping
from typing_extensions import Self, override

import httpx

from . import _exceptions
from ._qs import Querystring
from ._types import (
    Body,
    Omit,
    Query,
    Headers,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
    not_given,
)
from ._utils import is_given, get_async_library
from ._compat import cached_property
from ._version import __version__
from ._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import EvrimError, APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
    make_request_options,
)

if TYPE_CHECKING:
    from .resources import (
        qq,
        auth,
        chat,
        weibo,
        zhihu,
        douyin,
        emails,
        health,
        phones,
        search,
        wechat,
        sources,
        bilibili,
        meetings,
        documents,
        locations,
        technology,
        participants,
        organizations,
        relationships,
    )
    from .resources.qq.qq import QqResource, AsyncQqResource
    from .resources.health import HealthResource, AsyncHealthResource
    from .resources.sources import SourcesResource, AsyncSourcesResource
    from .resources.meetings import MeetingsResource, AsyncMeetingsResource
    from .resources.auth.auth import AuthResource, AsyncAuthResource
    from .resources.chat.chat import ChatResource, AsyncChatResource
    from .resources.weibo.weibo import WeiboResource, AsyncWeiboResource
    from .resources.zhihu.zhihu import ZhihuResource, AsyncZhihuResource
    from .resources.participants import ParticipantsResource, AsyncParticipantsResource
    from .resources.douyin.douyin import DouyinResource, AsyncDouyinResource
    from .resources.emails.emails import EmailsResource, AsyncEmailsResource
    from .resources.organizations import OrganizationsResource, AsyncOrganizationsResource
    from .resources.phones.phones import PhonesResource, AsyncPhonesResource
    from .resources.relationships import RelationshipsResource, AsyncRelationshipsResource
    from .resources.search.search import SearchResource, AsyncSearchResource
    from .resources.wechat.wechat import WechatResource, AsyncWechatResource
    from .resources.bilibili.bilibili import BilibiliResource, AsyncBilibiliResource
    from .resources.documents.documents import DocumentsResource, AsyncDocumentsResource
    from .resources.locations.locations import LocationsResource, AsyncLocationsResource
    from .resources.technology.technology import TechnologyResource, AsyncTechnologyResource

__all__ = ["Timeout", "Transport", "ProxiesTypes", "RequestOptions", "Evrim", "AsyncEvrim", "Client", "AsyncClient"]


class Evrim(SyncAPIClient):
    # client options
    api_key: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous Evrim client instance.

        This automatically infers the `api_key` argument from the `EVRIM_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("EVRIM_API_KEY")
        if api_key is None:
            raise EvrimError(
                "The api_key client option must be set either by passing api_key to the client or by setting the EVRIM_API_KEY environment variable"
            )
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("EVRIM_BASE_URL")
        if base_url is None:
            base_url = f"https://api.example.com"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

    @cached_property
    def chat(self) -> ChatResource:
        from .resources.chat import ChatResource

        return ChatResource(self)

    @cached_property
    def sources(self) -> SourcesResource:
        from .resources.sources import SourcesResource

        return SourcesResource(self)

    @cached_property
    def meetings(self) -> MeetingsResource:
        from .resources.meetings import MeetingsResource

        return MeetingsResource(self)

    @cached_property
    def participants(self) -> ParticipantsResource:
        from .resources.participants import ParticipantsResource

        return ParticipantsResource(self)

    @cached_property
    def organizations(self) -> OrganizationsResource:
        from .resources.organizations import OrganizationsResource

        return OrganizationsResource(self)

    @cached_property
    def locations(self) -> LocationsResource:
        from .resources.locations import LocationsResource

        return LocationsResource(self)

    @cached_property
    def documents(self) -> DocumentsResource:
        from .resources.documents import DocumentsResource

        return DocumentsResource(self)

    @cached_property
    def relationships(self) -> RelationshipsResource:
        from .resources.relationships import RelationshipsResource

        return RelationshipsResource(self)

    @cached_property
    def search(self) -> SearchResource:
        from .resources.search import SearchResource

        return SearchResource(self)

    @cached_property
    def emails(self) -> EmailsResource:
        from .resources.emails import EmailsResource

        return EmailsResource(self)

    @cached_property
    def phones(self) -> PhonesResource:
        from .resources.phones import PhonesResource

        return PhonesResource(self)

    @cached_property
    def wechat(self) -> WechatResource:
        from .resources.wechat import WechatResource

        return WechatResource(self)

    @cached_property
    def weibo(self) -> WeiboResource:
        from .resources.weibo import WeiboResource

        return WeiboResource(self)

    @cached_property
    def douyin(self) -> DouyinResource:
        from .resources.douyin import DouyinResource

        return DouyinResource(self)

    @cached_property
    def bilibili(self) -> BilibiliResource:
        from .resources.bilibili import BilibiliResource

        return BilibiliResource(self)

    @cached_property
    def zhihu(self) -> ZhihuResource:
        from .resources.zhihu import ZhihuResource

        return ZhihuResource(self)

    @cached_property
    def qq(self) -> QqResource:
        from .resources.qq import QqResource

        return QqResource(self)

    @cached_property
    def health(self) -> HealthResource:
        from .resources.health import HealthResource

        return HealthResource(self)

    @cached_property
    def auth(self) -> AuthResource:
        from .resources.auth import AuthResource

        return AuthResource(self)

    @cached_property
    def technology(self) -> TechnologyResource:
        from .resources.technology import TechnologyResource

        return TechnologyResource(self)

    @cached_property
    def with_raw_response(self) -> EvrimWithRawResponse:
        return EvrimWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EvrimWithStreamedResponse:
        return EvrimWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"Authorization": f"Bearer {api_key}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    def welcome(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        API Welcome Message

        Returns a welcome message and API information.

        **Authentication:** Not Required

        **Use this endpoint to:**

        - Verify the API is running
        - Check API availability
        - Get basic API information

        **Response:**

        ```json
        {
          "message": "Welcome to Evrim API"
        }
        ```

        **For full API documentation:**

        - Interactive docs: `/docs`
        - Alternative docs: `/redoc`
        - OpenAPI schema: `/openapi.json`
        """
        return self.get(
            "/",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncEvrim(AsyncAPIClient):
    # client options
    api_key: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async AsyncEvrim client instance.

        This automatically infers the `api_key` argument from the `EVRIM_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("EVRIM_API_KEY")
        if api_key is None:
            raise EvrimError(
                "The api_key client option must be set either by passing api_key to the client or by setting the EVRIM_API_KEY environment variable"
            )
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("EVRIM_BASE_URL")
        if base_url is None:
            base_url = f"https://api.example.com"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

    @cached_property
    def chat(self) -> AsyncChatResource:
        from .resources.chat import AsyncChatResource

        return AsyncChatResource(self)

    @cached_property
    def sources(self) -> AsyncSourcesResource:
        from .resources.sources import AsyncSourcesResource

        return AsyncSourcesResource(self)

    @cached_property
    def meetings(self) -> AsyncMeetingsResource:
        from .resources.meetings import AsyncMeetingsResource

        return AsyncMeetingsResource(self)

    @cached_property
    def participants(self) -> AsyncParticipantsResource:
        from .resources.participants import AsyncParticipantsResource

        return AsyncParticipantsResource(self)

    @cached_property
    def organizations(self) -> AsyncOrganizationsResource:
        from .resources.organizations import AsyncOrganizationsResource

        return AsyncOrganizationsResource(self)

    @cached_property
    def locations(self) -> AsyncLocationsResource:
        from .resources.locations import AsyncLocationsResource

        return AsyncLocationsResource(self)

    @cached_property
    def documents(self) -> AsyncDocumentsResource:
        from .resources.documents import AsyncDocumentsResource

        return AsyncDocumentsResource(self)

    @cached_property
    def relationships(self) -> AsyncRelationshipsResource:
        from .resources.relationships import AsyncRelationshipsResource

        return AsyncRelationshipsResource(self)

    @cached_property
    def search(self) -> AsyncSearchResource:
        from .resources.search import AsyncSearchResource

        return AsyncSearchResource(self)

    @cached_property
    def emails(self) -> AsyncEmailsResource:
        from .resources.emails import AsyncEmailsResource

        return AsyncEmailsResource(self)

    @cached_property
    def phones(self) -> AsyncPhonesResource:
        from .resources.phones import AsyncPhonesResource

        return AsyncPhonesResource(self)

    @cached_property
    def wechat(self) -> AsyncWechatResource:
        from .resources.wechat import AsyncWechatResource

        return AsyncWechatResource(self)

    @cached_property
    def weibo(self) -> AsyncWeiboResource:
        from .resources.weibo import AsyncWeiboResource

        return AsyncWeiboResource(self)

    @cached_property
    def douyin(self) -> AsyncDouyinResource:
        from .resources.douyin import AsyncDouyinResource

        return AsyncDouyinResource(self)

    @cached_property
    def bilibili(self) -> AsyncBilibiliResource:
        from .resources.bilibili import AsyncBilibiliResource

        return AsyncBilibiliResource(self)

    @cached_property
    def zhihu(self) -> AsyncZhihuResource:
        from .resources.zhihu import AsyncZhihuResource

        return AsyncZhihuResource(self)

    @cached_property
    def qq(self) -> AsyncQqResource:
        from .resources.qq import AsyncQqResource

        return AsyncQqResource(self)

    @cached_property
    def health(self) -> AsyncHealthResource:
        from .resources.health import AsyncHealthResource

        return AsyncHealthResource(self)

    @cached_property
    def auth(self) -> AsyncAuthResource:
        from .resources.auth import AsyncAuthResource

        return AsyncAuthResource(self)

    @cached_property
    def technology(self) -> AsyncTechnologyResource:
        from .resources.technology import AsyncTechnologyResource

        return AsyncTechnologyResource(self)

    @cached_property
    def with_raw_response(self) -> AsyncEvrimWithRawResponse:
        return AsyncEvrimWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEvrimWithStreamedResponse:
        return AsyncEvrimWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"Authorization": f"Bearer {api_key}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    async def welcome(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        API Welcome Message

        Returns a welcome message and API information.

        **Authentication:** Not Required

        **Use this endpoint to:**

        - Verify the API is running
        - Check API availability
        - Get basic API information

        **Response:**

        ```json
        {
          "message": "Welcome to Evrim API"
        }
        ```

        **For full API documentation:**

        - Interactive docs: `/docs`
        - Alternative docs: `/redoc`
        - OpenAPI schema: `/openapi.json`
        """
        return await self.get(
            "/",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class EvrimWithRawResponse:
    _client: Evrim

    def __init__(self, client: Evrim) -> None:
        self._client = client

        self.welcome = to_raw_response_wrapper(
            client.welcome,
        )

    @cached_property
    def chat(self) -> chat.ChatResourceWithRawResponse:
        from .resources.chat import ChatResourceWithRawResponse

        return ChatResourceWithRawResponse(self._client.chat)

    @cached_property
    def sources(self) -> sources.SourcesResourceWithRawResponse:
        from .resources.sources import SourcesResourceWithRawResponse

        return SourcesResourceWithRawResponse(self._client.sources)

    @cached_property
    def meetings(self) -> meetings.MeetingsResourceWithRawResponse:
        from .resources.meetings import MeetingsResourceWithRawResponse

        return MeetingsResourceWithRawResponse(self._client.meetings)

    @cached_property
    def participants(self) -> participants.ParticipantsResourceWithRawResponse:
        from .resources.participants import ParticipantsResourceWithRawResponse

        return ParticipantsResourceWithRawResponse(self._client.participants)

    @cached_property
    def organizations(self) -> organizations.OrganizationsResourceWithRawResponse:
        from .resources.organizations import OrganizationsResourceWithRawResponse

        return OrganizationsResourceWithRawResponse(self._client.organizations)

    @cached_property
    def locations(self) -> locations.LocationsResourceWithRawResponse:
        from .resources.locations import LocationsResourceWithRawResponse

        return LocationsResourceWithRawResponse(self._client.locations)

    @cached_property
    def documents(self) -> documents.DocumentsResourceWithRawResponse:
        from .resources.documents import DocumentsResourceWithRawResponse

        return DocumentsResourceWithRawResponse(self._client.documents)

    @cached_property
    def relationships(self) -> relationships.RelationshipsResourceWithRawResponse:
        from .resources.relationships import RelationshipsResourceWithRawResponse

        return RelationshipsResourceWithRawResponse(self._client.relationships)

    @cached_property
    def search(self) -> search.SearchResourceWithRawResponse:
        from .resources.search import SearchResourceWithRawResponse

        return SearchResourceWithRawResponse(self._client.search)

    @cached_property
    def emails(self) -> emails.EmailsResourceWithRawResponse:
        from .resources.emails import EmailsResourceWithRawResponse

        return EmailsResourceWithRawResponse(self._client.emails)

    @cached_property
    def phones(self) -> phones.PhonesResourceWithRawResponse:
        from .resources.phones import PhonesResourceWithRawResponse

        return PhonesResourceWithRawResponse(self._client.phones)

    @cached_property
    def wechat(self) -> wechat.WechatResourceWithRawResponse:
        from .resources.wechat import WechatResourceWithRawResponse

        return WechatResourceWithRawResponse(self._client.wechat)

    @cached_property
    def weibo(self) -> weibo.WeiboResourceWithRawResponse:
        from .resources.weibo import WeiboResourceWithRawResponse

        return WeiboResourceWithRawResponse(self._client.weibo)

    @cached_property
    def douyin(self) -> douyin.DouyinResourceWithRawResponse:
        from .resources.douyin import DouyinResourceWithRawResponse

        return DouyinResourceWithRawResponse(self._client.douyin)

    @cached_property
    def bilibili(self) -> bilibili.BilibiliResourceWithRawResponse:
        from .resources.bilibili import BilibiliResourceWithRawResponse

        return BilibiliResourceWithRawResponse(self._client.bilibili)

    @cached_property
    def zhihu(self) -> zhihu.ZhihuResourceWithRawResponse:
        from .resources.zhihu import ZhihuResourceWithRawResponse

        return ZhihuResourceWithRawResponse(self._client.zhihu)

    @cached_property
    def qq(self) -> qq.QqResourceWithRawResponse:
        from .resources.qq import QqResourceWithRawResponse

        return QqResourceWithRawResponse(self._client.qq)

    @cached_property
    def health(self) -> health.HealthResourceWithRawResponse:
        from .resources.health import HealthResourceWithRawResponse

        return HealthResourceWithRawResponse(self._client.health)

    @cached_property
    def auth(self) -> auth.AuthResourceWithRawResponse:
        from .resources.auth import AuthResourceWithRawResponse

        return AuthResourceWithRawResponse(self._client.auth)

    @cached_property
    def technology(self) -> technology.TechnologyResourceWithRawResponse:
        from .resources.technology import TechnologyResourceWithRawResponse

        return TechnologyResourceWithRawResponse(self._client.technology)


class AsyncEvrimWithRawResponse:
    _client: AsyncEvrim

    def __init__(self, client: AsyncEvrim) -> None:
        self._client = client

        self.welcome = async_to_raw_response_wrapper(
            client.welcome,
        )

    @cached_property
    def chat(self) -> chat.AsyncChatResourceWithRawResponse:
        from .resources.chat import AsyncChatResourceWithRawResponse

        return AsyncChatResourceWithRawResponse(self._client.chat)

    @cached_property
    def sources(self) -> sources.AsyncSourcesResourceWithRawResponse:
        from .resources.sources import AsyncSourcesResourceWithRawResponse

        return AsyncSourcesResourceWithRawResponse(self._client.sources)

    @cached_property
    def meetings(self) -> meetings.AsyncMeetingsResourceWithRawResponse:
        from .resources.meetings import AsyncMeetingsResourceWithRawResponse

        return AsyncMeetingsResourceWithRawResponse(self._client.meetings)

    @cached_property
    def participants(self) -> participants.AsyncParticipantsResourceWithRawResponse:
        from .resources.participants import AsyncParticipantsResourceWithRawResponse

        return AsyncParticipantsResourceWithRawResponse(self._client.participants)

    @cached_property
    def organizations(self) -> organizations.AsyncOrganizationsResourceWithRawResponse:
        from .resources.organizations import AsyncOrganizationsResourceWithRawResponse

        return AsyncOrganizationsResourceWithRawResponse(self._client.organizations)

    @cached_property
    def locations(self) -> locations.AsyncLocationsResourceWithRawResponse:
        from .resources.locations import AsyncLocationsResourceWithRawResponse

        return AsyncLocationsResourceWithRawResponse(self._client.locations)

    @cached_property
    def documents(self) -> documents.AsyncDocumentsResourceWithRawResponse:
        from .resources.documents import AsyncDocumentsResourceWithRawResponse

        return AsyncDocumentsResourceWithRawResponse(self._client.documents)

    @cached_property
    def relationships(self) -> relationships.AsyncRelationshipsResourceWithRawResponse:
        from .resources.relationships import AsyncRelationshipsResourceWithRawResponse

        return AsyncRelationshipsResourceWithRawResponse(self._client.relationships)

    @cached_property
    def search(self) -> search.AsyncSearchResourceWithRawResponse:
        from .resources.search import AsyncSearchResourceWithRawResponse

        return AsyncSearchResourceWithRawResponse(self._client.search)

    @cached_property
    def emails(self) -> emails.AsyncEmailsResourceWithRawResponse:
        from .resources.emails import AsyncEmailsResourceWithRawResponse

        return AsyncEmailsResourceWithRawResponse(self._client.emails)

    @cached_property
    def phones(self) -> phones.AsyncPhonesResourceWithRawResponse:
        from .resources.phones import AsyncPhonesResourceWithRawResponse

        return AsyncPhonesResourceWithRawResponse(self._client.phones)

    @cached_property
    def wechat(self) -> wechat.AsyncWechatResourceWithRawResponse:
        from .resources.wechat import AsyncWechatResourceWithRawResponse

        return AsyncWechatResourceWithRawResponse(self._client.wechat)

    @cached_property
    def weibo(self) -> weibo.AsyncWeiboResourceWithRawResponse:
        from .resources.weibo import AsyncWeiboResourceWithRawResponse

        return AsyncWeiboResourceWithRawResponse(self._client.weibo)

    @cached_property
    def douyin(self) -> douyin.AsyncDouyinResourceWithRawResponse:
        from .resources.douyin import AsyncDouyinResourceWithRawResponse

        return AsyncDouyinResourceWithRawResponse(self._client.douyin)

    @cached_property
    def bilibili(self) -> bilibili.AsyncBilibiliResourceWithRawResponse:
        from .resources.bilibili import AsyncBilibiliResourceWithRawResponse

        return AsyncBilibiliResourceWithRawResponse(self._client.bilibili)

    @cached_property
    def zhihu(self) -> zhihu.AsyncZhihuResourceWithRawResponse:
        from .resources.zhihu import AsyncZhihuResourceWithRawResponse

        return AsyncZhihuResourceWithRawResponse(self._client.zhihu)

    @cached_property
    def qq(self) -> qq.AsyncQqResourceWithRawResponse:
        from .resources.qq import AsyncQqResourceWithRawResponse

        return AsyncQqResourceWithRawResponse(self._client.qq)

    @cached_property
    def health(self) -> health.AsyncHealthResourceWithRawResponse:
        from .resources.health import AsyncHealthResourceWithRawResponse

        return AsyncHealthResourceWithRawResponse(self._client.health)

    @cached_property
    def auth(self) -> auth.AsyncAuthResourceWithRawResponse:
        from .resources.auth import AsyncAuthResourceWithRawResponse

        return AsyncAuthResourceWithRawResponse(self._client.auth)

    @cached_property
    def technology(self) -> technology.AsyncTechnologyResourceWithRawResponse:
        from .resources.technology import AsyncTechnologyResourceWithRawResponse

        return AsyncTechnologyResourceWithRawResponse(self._client.technology)


class EvrimWithStreamedResponse:
    _client: Evrim

    def __init__(self, client: Evrim) -> None:
        self._client = client

        self.welcome = to_streamed_response_wrapper(
            client.welcome,
        )

    @cached_property
    def chat(self) -> chat.ChatResourceWithStreamingResponse:
        from .resources.chat import ChatResourceWithStreamingResponse

        return ChatResourceWithStreamingResponse(self._client.chat)

    @cached_property
    def sources(self) -> sources.SourcesResourceWithStreamingResponse:
        from .resources.sources import SourcesResourceWithStreamingResponse

        return SourcesResourceWithStreamingResponse(self._client.sources)

    @cached_property
    def meetings(self) -> meetings.MeetingsResourceWithStreamingResponse:
        from .resources.meetings import MeetingsResourceWithStreamingResponse

        return MeetingsResourceWithStreamingResponse(self._client.meetings)

    @cached_property
    def participants(self) -> participants.ParticipantsResourceWithStreamingResponse:
        from .resources.participants import ParticipantsResourceWithStreamingResponse

        return ParticipantsResourceWithStreamingResponse(self._client.participants)

    @cached_property
    def organizations(self) -> organizations.OrganizationsResourceWithStreamingResponse:
        from .resources.organizations import OrganizationsResourceWithStreamingResponse

        return OrganizationsResourceWithStreamingResponse(self._client.organizations)

    @cached_property
    def locations(self) -> locations.LocationsResourceWithStreamingResponse:
        from .resources.locations import LocationsResourceWithStreamingResponse

        return LocationsResourceWithStreamingResponse(self._client.locations)

    @cached_property
    def documents(self) -> documents.DocumentsResourceWithStreamingResponse:
        from .resources.documents import DocumentsResourceWithStreamingResponse

        return DocumentsResourceWithStreamingResponse(self._client.documents)

    @cached_property
    def relationships(self) -> relationships.RelationshipsResourceWithStreamingResponse:
        from .resources.relationships import RelationshipsResourceWithStreamingResponse

        return RelationshipsResourceWithStreamingResponse(self._client.relationships)

    @cached_property
    def search(self) -> search.SearchResourceWithStreamingResponse:
        from .resources.search import SearchResourceWithStreamingResponse

        return SearchResourceWithStreamingResponse(self._client.search)

    @cached_property
    def emails(self) -> emails.EmailsResourceWithStreamingResponse:
        from .resources.emails import EmailsResourceWithStreamingResponse

        return EmailsResourceWithStreamingResponse(self._client.emails)

    @cached_property
    def phones(self) -> phones.PhonesResourceWithStreamingResponse:
        from .resources.phones import PhonesResourceWithStreamingResponse

        return PhonesResourceWithStreamingResponse(self._client.phones)

    @cached_property
    def wechat(self) -> wechat.WechatResourceWithStreamingResponse:
        from .resources.wechat import WechatResourceWithStreamingResponse

        return WechatResourceWithStreamingResponse(self._client.wechat)

    @cached_property
    def weibo(self) -> weibo.WeiboResourceWithStreamingResponse:
        from .resources.weibo import WeiboResourceWithStreamingResponse

        return WeiboResourceWithStreamingResponse(self._client.weibo)

    @cached_property
    def douyin(self) -> douyin.DouyinResourceWithStreamingResponse:
        from .resources.douyin import DouyinResourceWithStreamingResponse

        return DouyinResourceWithStreamingResponse(self._client.douyin)

    @cached_property
    def bilibili(self) -> bilibili.BilibiliResourceWithStreamingResponse:
        from .resources.bilibili import BilibiliResourceWithStreamingResponse

        return BilibiliResourceWithStreamingResponse(self._client.bilibili)

    @cached_property
    def zhihu(self) -> zhihu.ZhihuResourceWithStreamingResponse:
        from .resources.zhihu import ZhihuResourceWithStreamingResponse

        return ZhihuResourceWithStreamingResponse(self._client.zhihu)

    @cached_property
    def qq(self) -> qq.QqResourceWithStreamingResponse:
        from .resources.qq import QqResourceWithStreamingResponse

        return QqResourceWithStreamingResponse(self._client.qq)

    @cached_property
    def health(self) -> health.HealthResourceWithStreamingResponse:
        from .resources.health import HealthResourceWithStreamingResponse

        return HealthResourceWithStreamingResponse(self._client.health)

    @cached_property
    def auth(self) -> auth.AuthResourceWithStreamingResponse:
        from .resources.auth import AuthResourceWithStreamingResponse

        return AuthResourceWithStreamingResponse(self._client.auth)

    @cached_property
    def technology(self) -> technology.TechnologyResourceWithStreamingResponse:
        from .resources.technology import TechnologyResourceWithStreamingResponse

        return TechnologyResourceWithStreamingResponse(self._client.technology)


class AsyncEvrimWithStreamedResponse:
    _client: AsyncEvrim

    def __init__(self, client: AsyncEvrim) -> None:
        self._client = client

        self.welcome = async_to_streamed_response_wrapper(
            client.welcome,
        )

    @cached_property
    def chat(self) -> chat.AsyncChatResourceWithStreamingResponse:
        from .resources.chat import AsyncChatResourceWithStreamingResponse

        return AsyncChatResourceWithStreamingResponse(self._client.chat)

    @cached_property
    def sources(self) -> sources.AsyncSourcesResourceWithStreamingResponse:
        from .resources.sources import AsyncSourcesResourceWithStreamingResponse

        return AsyncSourcesResourceWithStreamingResponse(self._client.sources)

    @cached_property
    def meetings(self) -> meetings.AsyncMeetingsResourceWithStreamingResponse:
        from .resources.meetings import AsyncMeetingsResourceWithStreamingResponse

        return AsyncMeetingsResourceWithStreamingResponse(self._client.meetings)

    @cached_property
    def participants(self) -> participants.AsyncParticipantsResourceWithStreamingResponse:
        from .resources.participants import AsyncParticipantsResourceWithStreamingResponse

        return AsyncParticipantsResourceWithStreamingResponse(self._client.participants)

    @cached_property
    def organizations(self) -> organizations.AsyncOrganizationsResourceWithStreamingResponse:
        from .resources.organizations import AsyncOrganizationsResourceWithStreamingResponse

        return AsyncOrganizationsResourceWithStreamingResponse(self._client.organizations)

    @cached_property
    def locations(self) -> locations.AsyncLocationsResourceWithStreamingResponse:
        from .resources.locations import AsyncLocationsResourceWithStreamingResponse

        return AsyncLocationsResourceWithStreamingResponse(self._client.locations)

    @cached_property
    def documents(self) -> documents.AsyncDocumentsResourceWithStreamingResponse:
        from .resources.documents import AsyncDocumentsResourceWithStreamingResponse

        return AsyncDocumentsResourceWithStreamingResponse(self._client.documents)

    @cached_property
    def relationships(self) -> relationships.AsyncRelationshipsResourceWithStreamingResponse:
        from .resources.relationships import AsyncRelationshipsResourceWithStreamingResponse

        return AsyncRelationshipsResourceWithStreamingResponse(self._client.relationships)

    @cached_property
    def search(self) -> search.AsyncSearchResourceWithStreamingResponse:
        from .resources.search import AsyncSearchResourceWithStreamingResponse

        return AsyncSearchResourceWithStreamingResponse(self._client.search)

    @cached_property
    def emails(self) -> emails.AsyncEmailsResourceWithStreamingResponse:
        from .resources.emails import AsyncEmailsResourceWithStreamingResponse

        return AsyncEmailsResourceWithStreamingResponse(self._client.emails)

    @cached_property
    def phones(self) -> phones.AsyncPhonesResourceWithStreamingResponse:
        from .resources.phones import AsyncPhonesResourceWithStreamingResponse

        return AsyncPhonesResourceWithStreamingResponse(self._client.phones)

    @cached_property
    def wechat(self) -> wechat.AsyncWechatResourceWithStreamingResponse:
        from .resources.wechat import AsyncWechatResourceWithStreamingResponse

        return AsyncWechatResourceWithStreamingResponse(self._client.wechat)

    @cached_property
    def weibo(self) -> weibo.AsyncWeiboResourceWithStreamingResponse:
        from .resources.weibo import AsyncWeiboResourceWithStreamingResponse

        return AsyncWeiboResourceWithStreamingResponse(self._client.weibo)

    @cached_property
    def douyin(self) -> douyin.AsyncDouyinResourceWithStreamingResponse:
        from .resources.douyin import AsyncDouyinResourceWithStreamingResponse

        return AsyncDouyinResourceWithStreamingResponse(self._client.douyin)

    @cached_property
    def bilibili(self) -> bilibili.AsyncBilibiliResourceWithStreamingResponse:
        from .resources.bilibili import AsyncBilibiliResourceWithStreamingResponse

        return AsyncBilibiliResourceWithStreamingResponse(self._client.bilibili)

    @cached_property
    def zhihu(self) -> zhihu.AsyncZhihuResourceWithStreamingResponse:
        from .resources.zhihu import AsyncZhihuResourceWithStreamingResponse

        return AsyncZhihuResourceWithStreamingResponse(self._client.zhihu)

    @cached_property
    def qq(self) -> qq.AsyncQqResourceWithStreamingResponse:
        from .resources.qq import AsyncQqResourceWithStreamingResponse

        return AsyncQqResourceWithStreamingResponse(self._client.qq)

    @cached_property
    def health(self) -> health.AsyncHealthResourceWithStreamingResponse:
        from .resources.health import AsyncHealthResourceWithStreamingResponse

        return AsyncHealthResourceWithStreamingResponse(self._client.health)

    @cached_property
    def auth(self) -> auth.AsyncAuthResourceWithStreamingResponse:
        from .resources.auth import AsyncAuthResourceWithStreamingResponse

        return AsyncAuthResourceWithStreamingResponse(self._client.auth)

    @cached_property
    def technology(self) -> technology.AsyncTechnologyResourceWithStreamingResponse:
        from .resources.technology import AsyncTechnologyResourceWithStreamingResponse

        return AsyncTechnologyResourceWithStreamingResponse(self._client.technology)


Client = Evrim

AsyncClient = AsyncEvrim
