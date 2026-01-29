# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from evrim import Evrim, AsyncEvrim
from tests.utils import assert_matches_type
from evrim.types.documents import HTMLDocument, HTMLListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestHTML:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: Evrim) -> None:
        html = client.documents.html.list()
        assert_matches_type(HTMLListResponse, html, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Evrim) -> None:
        html = client.documents.html.list(
            end=0,
            start=0,
        )
        assert_matches_type(HTMLListResponse, html, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Evrim) -> None:
        response = client.documents.html.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        html = response.parse()
        assert_matches_type(HTMLListResponse, html, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Evrim) -> None:
        with client.documents.html.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            html = response.parse()
            assert_matches_type(HTMLListResponse, html, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve_by_url(self, client: Evrim) -> None:
        html = client.documents.html.retrieve_by_url(
            "url",
        )
        assert_matches_type(HTMLDocument, html, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve_by_url(self, client: Evrim) -> None:
        response = client.documents.html.with_raw_response.retrieve_by_url(
            "url",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        html = response.parse()
        assert_matches_type(HTMLDocument, html, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve_by_url(self, client: Evrim) -> None:
        with client.documents.html.with_streaming_response.retrieve_by_url(
            "url",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            html = response.parse()
            assert_matches_type(HTMLDocument, html, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve_by_url(self, client: Evrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `url` but received ''"):
            client.documents.html.with_raw_response.retrieve_by_url(
                "",
            )


class TestAsyncHTML:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncEvrim) -> None:
        html = await async_client.documents.html.list()
        assert_matches_type(HTMLListResponse, html, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncEvrim) -> None:
        html = await async_client.documents.html.list(
            end=0,
            start=0,
        )
        assert_matches_type(HTMLListResponse, html, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEvrim) -> None:
        response = await async_client.documents.html.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        html = await response.parse()
        assert_matches_type(HTMLListResponse, html, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEvrim) -> None:
        async with async_client.documents.html.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            html = await response.parse()
            assert_matches_type(HTMLListResponse, html, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve_by_url(self, async_client: AsyncEvrim) -> None:
        html = await async_client.documents.html.retrieve_by_url(
            "url",
        )
        assert_matches_type(HTMLDocument, html, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve_by_url(self, async_client: AsyncEvrim) -> None:
        response = await async_client.documents.html.with_raw_response.retrieve_by_url(
            "url",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        html = await response.parse()
        assert_matches_type(HTMLDocument, html, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve_by_url(self, async_client: AsyncEvrim) -> None:
        async with async_client.documents.html.with_streaming_response.retrieve_by_url(
            "url",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            html = await response.parse()
            assert_matches_type(HTMLDocument, html, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve_by_url(self, async_client: AsyncEvrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `url` but received ''"):
            await async_client.documents.html.with_raw_response.retrieve_by_url(
                "",
            )
