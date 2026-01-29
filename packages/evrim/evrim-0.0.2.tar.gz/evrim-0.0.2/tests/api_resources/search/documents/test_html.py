# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from evrim import Evrim, AsyncEvrim
from tests.utils import assert_matches_type
from evrim.types.search.documents import (
    HTMLSearchResponse,
    HTMLSearchByURLResponse,
    HTMLSearchByDomainResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestHTML:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_search(self, client: Evrim) -> None:
        html = client.search.documents.html.search(
            q="q",
        )
        assert_matches_type(HTMLSearchResponse, html, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_search_with_all_params(self, client: Evrim) -> None:
        html = client.search.documents.html.search(
            q="q",
            limit=1,
            offset=0,
        )
        assert_matches_type(HTMLSearchResponse, html, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_search(self, client: Evrim) -> None:
        response = client.search.documents.html.with_raw_response.search(
            q="q",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        html = response.parse()
        assert_matches_type(HTMLSearchResponse, html, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_search(self, client: Evrim) -> None:
        with client.search.documents.html.with_streaming_response.search(
            q="q",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            html = response.parse()
            assert_matches_type(HTMLSearchResponse, html, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_search_by_domain(self, client: Evrim) -> None:
        html = client.search.documents.html.search_by_domain(
            domain="domain",
        )
        assert_matches_type(HTMLSearchByDomainResponse, html, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_search_by_domain_with_all_params(self, client: Evrim) -> None:
        html = client.search.documents.html.search_by_domain(
            domain="domain",
            end=0,
            start=0,
        )
        assert_matches_type(HTMLSearchByDomainResponse, html, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_search_by_domain(self, client: Evrim) -> None:
        response = client.search.documents.html.with_raw_response.search_by_domain(
            domain="domain",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        html = response.parse()
        assert_matches_type(HTMLSearchByDomainResponse, html, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_search_by_domain(self, client: Evrim) -> None:
        with client.search.documents.html.with_streaming_response.search_by_domain(
            domain="domain",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            html = response.parse()
            assert_matches_type(HTMLSearchByDomainResponse, html, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_search_by_url(self, client: Evrim) -> None:
        html = client.search.documents.html.search_by_url(
            url="url",
        )
        assert_matches_type(HTMLSearchByURLResponse, html, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_search_by_url_with_all_params(self, client: Evrim) -> None:
        html = client.search.documents.html.search_by_url(
            url="url",
            limit=1,
            offset=0,
        )
        assert_matches_type(HTMLSearchByURLResponse, html, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_search_by_url(self, client: Evrim) -> None:
        response = client.search.documents.html.with_raw_response.search_by_url(
            url="url",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        html = response.parse()
        assert_matches_type(HTMLSearchByURLResponse, html, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_search_by_url(self, client: Evrim) -> None:
        with client.search.documents.html.with_streaming_response.search_by_url(
            url="url",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            html = response.parse()
            assert_matches_type(HTMLSearchByURLResponse, html, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncHTML:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_search(self, async_client: AsyncEvrim) -> None:
        html = await async_client.search.documents.html.search(
            q="q",
        )
        assert_matches_type(HTMLSearchResponse, html, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_search_with_all_params(self, async_client: AsyncEvrim) -> None:
        html = await async_client.search.documents.html.search(
            q="q",
            limit=1,
            offset=0,
        )
        assert_matches_type(HTMLSearchResponse, html, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_search(self, async_client: AsyncEvrim) -> None:
        response = await async_client.search.documents.html.with_raw_response.search(
            q="q",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        html = await response.parse()
        assert_matches_type(HTMLSearchResponse, html, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_search(self, async_client: AsyncEvrim) -> None:
        async with async_client.search.documents.html.with_streaming_response.search(
            q="q",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            html = await response.parse()
            assert_matches_type(HTMLSearchResponse, html, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_search_by_domain(self, async_client: AsyncEvrim) -> None:
        html = await async_client.search.documents.html.search_by_domain(
            domain="domain",
        )
        assert_matches_type(HTMLSearchByDomainResponse, html, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_search_by_domain_with_all_params(self, async_client: AsyncEvrim) -> None:
        html = await async_client.search.documents.html.search_by_domain(
            domain="domain",
            end=0,
            start=0,
        )
        assert_matches_type(HTMLSearchByDomainResponse, html, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_search_by_domain(self, async_client: AsyncEvrim) -> None:
        response = await async_client.search.documents.html.with_raw_response.search_by_domain(
            domain="domain",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        html = await response.parse()
        assert_matches_type(HTMLSearchByDomainResponse, html, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_search_by_domain(self, async_client: AsyncEvrim) -> None:
        async with async_client.search.documents.html.with_streaming_response.search_by_domain(
            domain="domain",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            html = await response.parse()
            assert_matches_type(HTMLSearchByDomainResponse, html, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_search_by_url(self, async_client: AsyncEvrim) -> None:
        html = await async_client.search.documents.html.search_by_url(
            url="url",
        )
        assert_matches_type(HTMLSearchByURLResponse, html, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_search_by_url_with_all_params(self, async_client: AsyncEvrim) -> None:
        html = await async_client.search.documents.html.search_by_url(
            url="url",
            limit=1,
            offset=0,
        )
        assert_matches_type(HTMLSearchByURLResponse, html, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_search_by_url(self, async_client: AsyncEvrim) -> None:
        response = await async_client.search.documents.html.with_raw_response.search_by_url(
            url="url",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        html = await response.parse()
        assert_matches_type(HTMLSearchByURLResponse, html, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_search_by_url(self, async_client: AsyncEvrim) -> None:
        async with async_client.search.documents.html.with_streaming_response.search_by_url(
            url="url",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            html = await response.parse()
            assert_matches_type(HTMLSearchByURLResponse, html, path=["response"])

        assert cast(Any, response.is_closed) is True
