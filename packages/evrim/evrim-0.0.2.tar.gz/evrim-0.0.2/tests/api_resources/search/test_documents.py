# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from evrim import Evrim, AsyncEvrim
from tests.utils import assert_matches_type
from evrim.types.search import (
    DocumentSearchMarkdownResponse,
    DocumentSearchSemanticResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDocuments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_search_markdown(self, client: Evrim) -> None:
        document = client.search.documents.search_markdown(
            q="q",
        )
        assert_matches_type(DocumentSearchMarkdownResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_search_markdown_with_all_params(self, client: Evrim) -> None:
        document = client.search.documents.search_markdown(
            q="q",
            limit=1,
            offset=0,
        )
        assert_matches_type(DocumentSearchMarkdownResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_search_markdown(self, client: Evrim) -> None:
        response = client.search.documents.with_raw_response.search_markdown(
            q="q",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = response.parse()
        assert_matches_type(DocumentSearchMarkdownResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_search_markdown(self, client: Evrim) -> None:
        with client.search.documents.with_streaming_response.search_markdown(
            q="q",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = response.parse()
            assert_matches_type(DocumentSearchMarkdownResponse, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_search_semantic(self, client: Evrim) -> None:
        document = client.search.documents.search_semantic(
            q="q",
        )
        assert_matches_type(DocumentSearchSemanticResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_search_semantic_with_all_params(self, client: Evrim) -> None:
        document = client.search.documents.search_semantic(
            q="q",
            limit=1,
            threshold=0,
        )
        assert_matches_type(DocumentSearchSemanticResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_search_semantic(self, client: Evrim) -> None:
        response = client.search.documents.with_raw_response.search_semantic(
            q="q",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = response.parse()
        assert_matches_type(DocumentSearchSemanticResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_search_semantic(self, client: Evrim) -> None:
        with client.search.documents.with_streaming_response.search_semantic(
            q="q",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = response.parse()
            assert_matches_type(DocumentSearchSemanticResponse, document, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncDocuments:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_search_markdown(self, async_client: AsyncEvrim) -> None:
        document = await async_client.search.documents.search_markdown(
            q="q",
        )
        assert_matches_type(DocumentSearchMarkdownResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_search_markdown_with_all_params(self, async_client: AsyncEvrim) -> None:
        document = await async_client.search.documents.search_markdown(
            q="q",
            limit=1,
            offset=0,
        )
        assert_matches_type(DocumentSearchMarkdownResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_search_markdown(self, async_client: AsyncEvrim) -> None:
        response = await async_client.search.documents.with_raw_response.search_markdown(
            q="q",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = await response.parse()
        assert_matches_type(DocumentSearchMarkdownResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_search_markdown(self, async_client: AsyncEvrim) -> None:
        async with async_client.search.documents.with_streaming_response.search_markdown(
            q="q",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = await response.parse()
            assert_matches_type(DocumentSearchMarkdownResponse, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_search_semantic(self, async_client: AsyncEvrim) -> None:
        document = await async_client.search.documents.search_semantic(
            q="q",
        )
        assert_matches_type(DocumentSearchSemanticResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_search_semantic_with_all_params(self, async_client: AsyncEvrim) -> None:
        document = await async_client.search.documents.search_semantic(
            q="q",
            limit=1,
            threshold=0,
        )
        assert_matches_type(DocumentSearchSemanticResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_search_semantic(self, async_client: AsyncEvrim) -> None:
        response = await async_client.search.documents.with_raw_response.search_semantic(
            q="q",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = await response.parse()
        assert_matches_type(DocumentSearchSemanticResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_search_semantic(self, async_client: AsyncEvrim) -> None:
        async with async_client.search.documents.with_streaming_response.search_semantic(
            q="q",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = await response.parse()
            assert_matches_type(DocumentSearchSemanticResponse, document, path=["response"])

        assert cast(Any, response.is_closed) is True
