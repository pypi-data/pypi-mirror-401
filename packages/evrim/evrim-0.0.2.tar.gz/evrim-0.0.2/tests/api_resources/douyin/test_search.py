# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from evrim import Evrim, AsyncEvrim
from tests.utils import assert_matches_type
from evrim.types.douyin import SearchBySourceDomainResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSearch:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_by_source_domain(self, client: Evrim) -> None:
        search = client.douyin.search.by_source_domain(
            domain="x",
        )
        assert_matches_type(SearchBySourceDomainResponse, search, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_by_source_domain_with_all_params(self, client: Evrim) -> None:
        search = client.douyin.search.by_source_domain(
            domain="x",
            end=0,
            start=0,
        )
        assert_matches_type(SearchBySourceDomainResponse, search, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_by_source_domain(self, client: Evrim) -> None:
        response = client.douyin.search.with_raw_response.by_source_domain(
            domain="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = response.parse()
        assert_matches_type(SearchBySourceDomainResponse, search, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_by_source_domain(self, client: Evrim) -> None:
        with client.douyin.search.with_streaming_response.by_source_domain(
            domain="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = response.parse()
            assert_matches_type(SearchBySourceDomainResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSearch:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_by_source_domain(self, async_client: AsyncEvrim) -> None:
        search = await async_client.douyin.search.by_source_domain(
            domain="x",
        )
        assert_matches_type(SearchBySourceDomainResponse, search, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_by_source_domain_with_all_params(self, async_client: AsyncEvrim) -> None:
        search = await async_client.douyin.search.by_source_domain(
            domain="x",
            end=0,
            start=0,
        )
        assert_matches_type(SearchBySourceDomainResponse, search, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_by_source_domain(self, async_client: AsyncEvrim) -> None:
        response = await async_client.douyin.search.with_raw_response.by_source_domain(
            domain="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = await response.parse()
        assert_matches_type(SearchBySourceDomainResponse, search, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_by_source_domain(self, async_client: AsyncEvrim) -> None:
        async with async_client.douyin.search.with_streaming_response.by_source_domain(
            domain="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = await response.parse()
            assert_matches_type(SearchBySourceDomainResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True
