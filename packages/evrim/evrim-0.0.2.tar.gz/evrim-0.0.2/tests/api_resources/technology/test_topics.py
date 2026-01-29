# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from evrim import Evrim, AsyncEvrim
from tests.utils import assert_matches_type
from evrim.types.technology import (
    TopicSearchResponse,
    TopicRetrieveResponse,
    TopicGetPublicationsResponse,
    TopicGetSimilarTopicsResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTopics:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Evrim) -> None:
        topic = client.technology.topics.retrieve(
            "topic_id",
        )
        assert_matches_type(TopicRetrieveResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Evrim) -> None:
        response = client.technology.topics.with_raw_response.retrieve(
            "topic_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        topic = response.parse()
        assert_matches_type(TopicRetrieveResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Evrim) -> None:
        with client.technology.topics.with_streaming_response.retrieve(
            "topic_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            topic = response.parse()
            assert_matches_type(TopicRetrieveResponse, topic, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Evrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `topic_id` but received ''"):
            client.technology.topics.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_publications(self, client: Evrim) -> None:
        topic = client.technology.topics.get_publications(
            topic_id="topic_id",
        )
        assert_matches_type(TopicGetPublicationsResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_publications_with_all_params(self, client: Evrim) -> None:
        topic = client.technology.topics.get_publications(
            topic_id="topic_id",
            limit=1,
            min_similarity=0,
            offset=0,
            sort_by="title",
            sort_order="asc",
            year_max=1900,
            year_min=1900,
        )
        assert_matches_type(TopicGetPublicationsResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_get_publications(self, client: Evrim) -> None:
        response = client.technology.topics.with_raw_response.get_publications(
            topic_id="topic_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        topic = response.parse()
        assert_matches_type(TopicGetPublicationsResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_get_publications(self, client: Evrim) -> None:
        with client.technology.topics.with_streaming_response.get_publications(
            topic_id="topic_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            topic = response.parse()
            assert_matches_type(TopicGetPublicationsResponse, topic, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_get_publications(self, client: Evrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `topic_id` but received ''"):
            client.technology.topics.with_raw_response.get_publications(
                topic_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_similar_topics(self, client: Evrim) -> None:
        topic = client.technology.topics.get_similar_topics(
            topic_id="topic_id",
        )
        assert_matches_type(TopicGetSimilarTopicsResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_similar_topics_with_all_params(self, client: Evrim) -> None:
        topic = client.technology.topics.get_similar_topics(
            topic_id="topic_id",
            limit=1,
            min_similarity=0,
        )
        assert_matches_type(TopicGetSimilarTopicsResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_get_similar_topics(self, client: Evrim) -> None:
        response = client.technology.topics.with_raw_response.get_similar_topics(
            topic_id="topic_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        topic = response.parse()
        assert_matches_type(TopicGetSimilarTopicsResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_get_similar_topics(self, client: Evrim) -> None:
        with client.technology.topics.with_streaming_response.get_similar_topics(
            topic_id="topic_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            topic = response.parse()
            assert_matches_type(TopicGetSimilarTopicsResponse, topic, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_get_similar_topics(self, client: Evrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `topic_id` but received ''"):
            client.technology.topics.with_raw_response.get_similar_topics(
                topic_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_search(self, client: Evrim) -> None:
        topic = client.technology.topics.search(
            q="x",
        )
        assert_matches_type(TopicSearchResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_search_with_all_params(self, client: Evrim) -> None:
        topic = client.technology.topics.search(
            q="x",
            limit=1,
            offset=0,
            sort_by="name",
            sort_order="asc",
        )
        assert_matches_type(TopicSearchResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_search(self, client: Evrim) -> None:
        response = client.technology.topics.with_raw_response.search(
            q="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        topic = response.parse()
        assert_matches_type(TopicSearchResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_search(self, client: Evrim) -> None:
        with client.technology.topics.with_streaming_response.search(
            q="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            topic = response.parse()
            assert_matches_type(TopicSearchResponse, topic, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncTopics:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncEvrim) -> None:
        topic = await async_client.technology.topics.retrieve(
            "topic_id",
        )
        assert_matches_type(TopicRetrieveResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncEvrim) -> None:
        response = await async_client.technology.topics.with_raw_response.retrieve(
            "topic_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        topic = await response.parse()
        assert_matches_type(TopicRetrieveResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncEvrim) -> None:
        async with async_client.technology.topics.with_streaming_response.retrieve(
            "topic_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            topic = await response.parse()
            assert_matches_type(TopicRetrieveResponse, topic, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncEvrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `topic_id` but received ''"):
            await async_client.technology.topics.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_publications(self, async_client: AsyncEvrim) -> None:
        topic = await async_client.technology.topics.get_publications(
            topic_id="topic_id",
        )
        assert_matches_type(TopicGetPublicationsResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_publications_with_all_params(self, async_client: AsyncEvrim) -> None:
        topic = await async_client.technology.topics.get_publications(
            topic_id="topic_id",
            limit=1,
            min_similarity=0,
            offset=0,
            sort_by="title",
            sort_order="asc",
            year_max=1900,
            year_min=1900,
        )
        assert_matches_type(TopicGetPublicationsResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_get_publications(self, async_client: AsyncEvrim) -> None:
        response = await async_client.technology.topics.with_raw_response.get_publications(
            topic_id="topic_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        topic = await response.parse()
        assert_matches_type(TopicGetPublicationsResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_get_publications(self, async_client: AsyncEvrim) -> None:
        async with async_client.technology.topics.with_streaming_response.get_publications(
            topic_id="topic_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            topic = await response.parse()
            assert_matches_type(TopicGetPublicationsResponse, topic, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_get_publications(self, async_client: AsyncEvrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `topic_id` but received ''"):
            await async_client.technology.topics.with_raw_response.get_publications(
                topic_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_similar_topics(self, async_client: AsyncEvrim) -> None:
        topic = await async_client.technology.topics.get_similar_topics(
            topic_id="topic_id",
        )
        assert_matches_type(TopicGetSimilarTopicsResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_similar_topics_with_all_params(self, async_client: AsyncEvrim) -> None:
        topic = await async_client.technology.topics.get_similar_topics(
            topic_id="topic_id",
            limit=1,
            min_similarity=0,
        )
        assert_matches_type(TopicGetSimilarTopicsResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_get_similar_topics(self, async_client: AsyncEvrim) -> None:
        response = await async_client.technology.topics.with_raw_response.get_similar_topics(
            topic_id="topic_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        topic = await response.parse()
        assert_matches_type(TopicGetSimilarTopicsResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_get_similar_topics(self, async_client: AsyncEvrim) -> None:
        async with async_client.technology.topics.with_streaming_response.get_similar_topics(
            topic_id="topic_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            topic = await response.parse()
            assert_matches_type(TopicGetSimilarTopicsResponse, topic, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_get_similar_topics(self, async_client: AsyncEvrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `topic_id` but received ''"):
            await async_client.technology.topics.with_raw_response.get_similar_topics(
                topic_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_search(self, async_client: AsyncEvrim) -> None:
        topic = await async_client.technology.topics.search(
            q="x",
        )
        assert_matches_type(TopicSearchResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_search_with_all_params(self, async_client: AsyncEvrim) -> None:
        topic = await async_client.technology.topics.search(
            q="x",
            limit=1,
            offset=0,
            sort_by="name",
            sort_order="asc",
        )
        assert_matches_type(TopicSearchResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_search(self, async_client: AsyncEvrim) -> None:
        response = await async_client.technology.topics.with_raw_response.search(
            q="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        topic = await response.parse()
        assert_matches_type(TopicSearchResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_search(self, async_client: AsyncEvrim) -> None:
        async with async_client.technology.topics.with_streaming_response.search(
            q="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            topic = await response.parse()
            assert_matches_type(TopicSearchResponse, topic, path=["response"])

        assert cast(Any, response.is_closed) is True
