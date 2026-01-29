# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from evrim import Evrim, AsyncEvrim
from tests.utils import assert_matches_type
from evrim.types.technology import (
    TechnologyPublication,
    PublicationSearchResponse,
    PublicationGetTopicsResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPublications:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Evrim) -> None:
        publication = client.technology.publications.retrieve(
            "publication_id",
        )
        assert_matches_type(TechnologyPublication, publication, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Evrim) -> None:
        response = client.technology.publications.with_raw_response.retrieve(
            "publication_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        publication = response.parse()
        assert_matches_type(TechnologyPublication, publication, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Evrim) -> None:
        with client.technology.publications.with_streaming_response.retrieve(
            "publication_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            publication = response.parse()
            assert_matches_type(TechnologyPublication, publication, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Evrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `publication_id` but received ''"):
            client.technology.publications.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_topics(self, client: Evrim) -> None:
        publication = client.technology.publications.get_topics(
            publication_id="publication_id",
        )
        assert_matches_type(PublicationGetTopicsResponse, publication, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_topics_with_all_params(self, client: Evrim) -> None:
        publication = client.technology.publications.get_topics(
            publication_id="publication_id",
            limit=1,
            min_similarity=0,
            offset=0,
            sort_by="name",
            sort_order="asc",
        )
        assert_matches_type(PublicationGetTopicsResponse, publication, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_get_topics(self, client: Evrim) -> None:
        response = client.technology.publications.with_raw_response.get_topics(
            publication_id="publication_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        publication = response.parse()
        assert_matches_type(PublicationGetTopicsResponse, publication, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_get_topics(self, client: Evrim) -> None:
        with client.technology.publications.with_streaming_response.get_topics(
            publication_id="publication_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            publication = response.parse()
            assert_matches_type(PublicationGetTopicsResponse, publication, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_get_topics(self, client: Evrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `publication_id` but received ''"):
            client.technology.publications.with_raw_response.get_topics(
                publication_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_search(self, client: Evrim) -> None:
        publication = client.technology.publications.search(
            q="x",
        )
        assert_matches_type(PublicationSearchResponse, publication, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_search_with_all_params(self, client: Evrim) -> None:
        publication = client.technology.publications.search(
            q="x",
            limit=1,
            offset=0,
            sort_by="year",
            sort_order="asc",
            year_max=0,
            year_min=0,
        )
        assert_matches_type(PublicationSearchResponse, publication, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_search(self, client: Evrim) -> None:
        response = client.technology.publications.with_raw_response.search(
            q="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        publication = response.parse()
        assert_matches_type(PublicationSearchResponse, publication, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_search(self, client: Evrim) -> None:
        with client.technology.publications.with_streaming_response.search(
            q="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            publication = response.parse()
            assert_matches_type(PublicationSearchResponse, publication, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncPublications:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncEvrim) -> None:
        publication = await async_client.technology.publications.retrieve(
            "publication_id",
        )
        assert_matches_type(TechnologyPublication, publication, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncEvrim) -> None:
        response = await async_client.technology.publications.with_raw_response.retrieve(
            "publication_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        publication = await response.parse()
        assert_matches_type(TechnologyPublication, publication, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncEvrim) -> None:
        async with async_client.technology.publications.with_streaming_response.retrieve(
            "publication_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            publication = await response.parse()
            assert_matches_type(TechnologyPublication, publication, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncEvrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `publication_id` but received ''"):
            await async_client.technology.publications.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_topics(self, async_client: AsyncEvrim) -> None:
        publication = await async_client.technology.publications.get_topics(
            publication_id="publication_id",
        )
        assert_matches_type(PublicationGetTopicsResponse, publication, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_topics_with_all_params(self, async_client: AsyncEvrim) -> None:
        publication = await async_client.technology.publications.get_topics(
            publication_id="publication_id",
            limit=1,
            min_similarity=0,
            offset=0,
            sort_by="name",
            sort_order="asc",
        )
        assert_matches_type(PublicationGetTopicsResponse, publication, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_get_topics(self, async_client: AsyncEvrim) -> None:
        response = await async_client.technology.publications.with_raw_response.get_topics(
            publication_id="publication_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        publication = await response.parse()
        assert_matches_type(PublicationGetTopicsResponse, publication, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_get_topics(self, async_client: AsyncEvrim) -> None:
        async with async_client.technology.publications.with_streaming_response.get_topics(
            publication_id="publication_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            publication = await response.parse()
            assert_matches_type(PublicationGetTopicsResponse, publication, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_get_topics(self, async_client: AsyncEvrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `publication_id` but received ''"):
            await async_client.technology.publications.with_raw_response.get_topics(
                publication_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_search(self, async_client: AsyncEvrim) -> None:
        publication = await async_client.technology.publications.search(
            q="x",
        )
        assert_matches_type(PublicationSearchResponse, publication, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_search_with_all_params(self, async_client: AsyncEvrim) -> None:
        publication = await async_client.technology.publications.search(
            q="x",
            limit=1,
            offset=0,
            sort_by="year",
            sort_order="asc",
            year_max=0,
            year_min=0,
        )
        assert_matches_type(PublicationSearchResponse, publication, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_search(self, async_client: AsyncEvrim) -> None:
        response = await async_client.technology.publications.with_raw_response.search(
            q="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        publication = await response.parse()
        assert_matches_type(PublicationSearchResponse, publication, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_search(self, async_client: AsyncEvrim) -> None:
        async with async_client.technology.publications.with_streaming_response.search(
            q="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            publication = await response.parse()
            assert_matches_type(PublicationSearchResponse, publication, path=["response"])

        assert cast(Any, response.is_closed) is True
