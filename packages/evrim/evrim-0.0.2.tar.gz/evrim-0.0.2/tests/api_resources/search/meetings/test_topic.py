# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from evrim import Evrim, AsyncEvrim
from tests.utils import assert_matches_type
from evrim.types.search.meetings import (
    TopicSearchResponse,
    TopicSearchSemanticResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTopic:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_search(self, client: Evrim) -> None:
        topic = client.search.meetings.topic.search(
            q="q",
        )
        assert_matches_type(TopicSearchResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_search_with_all_params(self, client: Evrim) -> None:
        topic = client.search.meetings.topic.search(
            q="q",
            limit=1,
            offset=0,
            sort_by="name",
            sort_order="asc",
        )
        assert_matches_type(TopicSearchResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_search(self, client: Evrim) -> None:
        response = client.search.meetings.topic.with_raw_response.search(
            q="q",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        topic = response.parse()
        assert_matches_type(TopicSearchResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_search(self, client: Evrim) -> None:
        with client.search.meetings.topic.with_streaming_response.search(
            q="q",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            topic = response.parse()
            assert_matches_type(TopicSearchResponse, topic, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_search_semantic(self, client: Evrim) -> None:
        topic = client.search.meetings.topic.search_semantic(
            q="q",
        )
        assert_matches_type(TopicSearchSemanticResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_search_semantic_with_all_params(self, client: Evrim) -> None:
        topic = client.search.meetings.topic.search_semantic(
            q="q",
            limit=1,
            threshold=0,
        )
        assert_matches_type(TopicSearchSemanticResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_search_semantic(self, client: Evrim) -> None:
        response = client.search.meetings.topic.with_raw_response.search_semantic(
            q="q",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        topic = response.parse()
        assert_matches_type(TopicSearchSemanticResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_search_semantic(self, client: Evrim) -> None:
        with client.search.meetings.topic.with_streaming_response.search_semantic(
            q="q",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            topic = response.parse()
            assert_matches_type(TopicSearchSemanticResponse, topic, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncTopic:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_search(self, async_client: AsyncEvrim) -> None:
        topic = await async_client.search.meetings.topic.search(
            q="q",
        )
        assert_matches_type(TopicSearchResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_search_with_all_params(self, async_client: AsyncEvrim) -> None:
        topic = await async_client.search.meetings.topic.search(
            q="q",
            limit=1,
            offset=0,
            sort_by="name",
            sort_order="asc",
        )
        assert_matches_type(TopicSearchResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_search(self, async_client: AsyncEvrim) -> None:
        response = await async_client.search.meetings.topic.with_raw_response.search(
            q="q",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        topic = await response.parse()
        assert_matches_type(TopicSearchResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_search(self, async_client: AsyncEvrim) -> None:
        async with async_client.search.meetings.topic.with_streaming_response.search(
            q="q",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            topic = await response.parse()
            assert_matches_type(TopicSearchResponse, topic, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_search_semantic(self, async_client: AsyncEvrim) -> None:
        topic = await async_client.search.meetings.topic.search_semantic(
            q="q",
        )
        assert_matches_type(TopicSearchSemanticResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_search_semantic_with_all_params(self, async_client: AsyncEvrim) -> None:
        topic = await async_client.search.meetings.topic.search_semantic(
            q="q",
            limit=1,
            threshold=0,
        )
        assert_matches_type(TopicSearchSemanticResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_search_semantic(self, async_client: AsyncEvrim) -> None:
        response = await async_client.search.meetings.topic.with_raw_response.search_semantic(
            q="q",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        topic = await response.parse()
        assert_matches_type(TopicSearchSemanticResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_search_semantic(self, async_client: AsyncEvrim) -> None:
        async with async_client.search.meetings.topic.with_streaming_response.search_semantic(
            q="q",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            topic = await response.parse()
            assert_matches_type(TopicSearchSemanticResponse, topic, path=["response"])

        assert cast(Any, response.is_closed) is True
