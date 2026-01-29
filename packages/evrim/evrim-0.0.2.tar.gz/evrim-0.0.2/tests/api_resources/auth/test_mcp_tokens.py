# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from evrim import Evrim, AsyncEvrim
from tests.utils import assert_matches_type
from evrim.types.auth import (
    McpTokenListResponse,
    McpTokenCreateResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMcpTokens:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create(self, client: Evrim) -> None:
        mcp_token = client.auth.mcp_tokens.create(
            name="x",
        )
        assert_matches_type(McpTokenCreateResponse, mcp_token, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Evrim) -> None:
        mcp_token = client.auth.mcp_tokens.create(
            name="x",
            expiry_days=1,
        )
        assert_matches_type(McpTokenCreateResponse, mcp_token, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Evrim) -> None:
        response = client.auth.mcp_tokens.with_raw_response.create(
            name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        mcp_token = response.parse()
        assert_matches_type(McpTokenCreateResponse, mcp_token, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Evrim) -> None:
        with client.auth.mcp_tokens.with_streaming_response.create(
            name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            mcp_token = response.parse()
            assert_matches_type(McpTokenCreateResponse, mcp_token, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: Evrim) -> None:
        mcp_token = client.auth.mcp_tokens.list()
        assert_matches_type(McpTokenListResponse, mcp_token, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Evrim) -> None:
        mcp_token = client.auth.mcp_tokens.list(
            include_revoked=True,
        )
        assert_matches_type(McpTokenListResponse, mcp_token, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Evrim) -> None:
        response = client.auth.mcp_tokens.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        mcp_token = response.parse()
        assert_matches_type(McpTokenListResponse, mcp_token, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Evrim) -> None:
        with client.auth.mcp_tokens.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            mcp_token = response.parse()
            assert_matches_type(McpTokenListResponse, mcp_token, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_revoke(self, client: Evrim) -> None:
        mcp_token = client.auth.mcp_tokens.revoke(
            "token_id",
        )
        assert_matches_type(object, mcp_token, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_revoke(self, client: Evrim) -> None:
        response = client.auth.mcp_tokens.with_raw_response.revoke(
            "token_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        mcp_token = response.parse()
        assert_matches_type(object, mcp_token, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_revoke(self, client: Evrim) -> None:
        with client.auth.mcp_tokens.with_streaming_response.revoke(
            "token_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            mcp_token = response.parse()
            assert_matches_type(object, mcp_token, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_revoke(self, client: Evrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `token_id` but received ''"):
            client.auth.mcp_tokens.with_raw_response.revoke(
                "",
            )


class TestAsyncMcpTokens:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncEvrim) -> None:
        mcp_token = await async_client.auth.mcp_tokens.create(
            name="x",
        )
        assert_matches_type(McpTokenCreateResponse, mcp_token, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncEvrim) -> None:
        mcp_token = await async_client.auth.mcp_tokens.create(
            name="x",
            expiry_days=1,
        )
        assert_matches_type(McpTokenCreateResponse, mcp_token, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEvrim) -> None:
        response = await async_client.auth.mcp_tokens.with_raw_response.create(
            name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        mcp_token = await response.parse()
        assert_matches_type(McpTokenCreateResponse, mcp_token, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEvrim) -> None:
        async with async_client.auth.mcp_tokens.with_streaming_response.create(
            name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            mcp_token = await response.parse()
            assert_matches_type(McpTokenCreateResponse, mcp_token, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncEvrim) -> None:
        mcp_token = await async_client.auth.mcp_tokens.list()
        assert_matches_type(McpTokenListResponse, mcp_token, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncEvrim) -> None:
        mcp_token = await async_client.auth.mcp_tokens.list(
            include_revoked=True,
        )
        assert_matches_type(McpTokenListResponse, mcp_token, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEvrim) -> None:
        response = await async_client.auth.mcp_tokens.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        mcp_token = await response.parse()
        assert_matches_type(McpTokenListResponse, mcp_token, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEvrim) -> None:
        async with async_client.auth.mcp_tokens.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            mcp_token = await response.parse()
            assert_matches_type(McpTokenListResponse, mcp_token, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_revoke(self, async_client: AsyncEvrim) -> None:
        mcp_token = await async_client.auth.mcp_tokens.revoke(
            "token_id",
        )
        assert_matches_type(object, mcp_token, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_revoke(self, async_client: AsyncEvrim) -> None:
        response = await async_client.auth.mcp_tokens.with_raw_response.revoke(
            "token_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        mcp_token = await response.parse()
        assert_matches_type(object, mcp_token, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_revoke(self, async_client: AsyncEvrim) -> None:
        async with async_client.auth.mcp_tokens.with_streaming_response.revoke(
            "token_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            mcp_token = await response.parse()
            assert_matches_type(object, mcp_token, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_revoke(self, async_client: AsyncEvrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `token_id` but received ''"):
            await async_client.auth.mcp_tokens.with_raw_response.revoke(
                "",
            )
