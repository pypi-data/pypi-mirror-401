# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from evrim import Evrim, AsyncEvrim
from tests.utils import assert_matches_type
from evrim.types.technology import (
    GraphFindPathResponse,
    GraphGetOverlapResponse,
    GraphGetSubgraphResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestGraph:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_find_path(self, client: Evrim) -> None:
        graph = client.technology.graph.find_path(
            source="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            target="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(GraphFindPathResponse, graph, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_find_path_with_all_params(self, client: Evrim) -> None:
        graph = client.technology.graph.find_path(
            source="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            target="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            max_depth=1,
        )
        assert_matches_type(GraphFindPathResponse, graph, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_find_path(self, client: Evrim) -> None:
        response = client.technology.graph.with_raw_response.find_path(
            source="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            target="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        graph = response.parse()
        assert_matches_type(GraphFindPathResponse, graph, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_find_path(self, client: Evrim) -> None:
        with client.technology.graph.with_streaming_response.find_path(
            source="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            target="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            graph = response.parse()
            assert_matches_type(GraphFindPathResponse, graph, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_overlap(self, client: Evrim) -> None:
        graph = client.technology.graph.get_overlap(
            community_id1="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            community_id2="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(GraphGetOverlapResponse, graph, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_get_overlap(self, client: Evrim) -> None:
        response = client.technology.graph.with_raw_response.get_overlap(
            community_id1="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            community_id2="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        graph = response.parse()
        assert_matches_type(GraphGetOverlapResponse, graph, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_get_overlap(self, client: Evrim) -> None:
        with client.technology.graph.with_streaming_response.get_overlap(
            community_id1="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            community_id2="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            graph = response.parse()
            assert_matches_type(GraphGetOverlapResponse, graph, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_subgraph(self, client: Evrim) -> None:
        graph = client.technology.graph.get_subgraph(
            community_ids=["string"],
        )
        assert_matches_type(GraphGetSubgraphResponse, graph, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_subgraph_with_all_params(self, client: Evrim) -> None:
        graph = client.technology.graph.get_subgraph(
            community_ids=["string"],
            depth=1,
            min_edge_strength=0,
        )
        assert_matches_type(GraphGetSubgraphResponse, graph, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_get_subgraph(self, client: Evrim) -> None:
        response = client.technology.graph.with_raw_response.get_subgraph(
            community_ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        graph = response.parse()
        assert_matches_type(GraphGetSubgraphResponse, graph, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_get_subgraph(self, client: Evrim) -> None:
        with client.technology.graph.with_streaming_response.get_subgraph(
            community_ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            graph = response.parse()
            assert_matches_type(GraphGetSubgraphResponse, graph, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncGraph:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_find_path(self, async_client: AsyncEvrim) -> None:
        graph = await async_client.technology.graph.find_path(
            source="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            target="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(GraphFindPathResponse, graph, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_find_path_with_all_params(self, async_client: AsyncEvrim) -> None:
        graph = await async_client.technology.graph.find_path(
            source="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            target="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            max_depth=1,
        )
        assert_matches_type(GraphFindPathResponse, graph, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_find_path(self, async_client: AsyncEvrim) -> None:
        response = await async_client.technology.graph.with_raw_response.find_path(
            source="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            target="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        graph = await response.parse()
        assert_matches_type(GraphFindPathResponse, graph, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_find_path(self, async_client: AsyncEvrim) -> None:
        async with async_client.technology.graph.with_streaming_response.find_path(
            source="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            target="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            graph = await response.parse()
            assert_matches_type(GraphFindPathResponse, graph, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_overlap(self, async_client: AsyncEvrim) -> None:
        graph = await async_client.technology.graph.get_overlap(
            community_id1="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            community_id2="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(GraphGetOverlapResponse, graph, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_get_overlap(self, async_client: AsyncEvrim) -> None:
        response = await async_client.technology.graph.with_raw_response.get_overlap(
            community_id1="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            community_id2="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        graph = await response.parse()
        assert_matches_type(GraphGetOverlapResponse, graph, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_get_overlap(self, async_client: AsyncEvrim) -> None:
        async with async_client.technology.graph.with_streaming_response.get_overlap(
            community_id1="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            community_id2="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            graph = await response.parse()
            assert_matches_type(GraphGetOverlapResponse, graph, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_subgraph(self, async_client: AsyncEvrim) -> None:
        graph = await async_client.technology.graph.get_subgraph(
            community_ids=["string"],
        )
        assert_matches_type(GraphGetSubgraphResponse, graph, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_subgraph_with_all_params(self, async_client: AsyncEvrim) -> None:
        graph = await async_client.technology.graph.get_subgraph(
            community_ids=["string"],
            depth=1,
            min_edge_strength=0,
        )
        assert_matches_type(GraphGetSubgraphResponse, graph, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_get_subgraph(self, async_client: AsyncEvrim) -> None:
        response = await async_client.technology.graph.with_raw_response.get_subgraph(
            community_ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        graph = await response.parse()
        assert_matches_type(GraphGetSubgraphResponse, graph, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_get_subgraph(self, async_client: AsyncEvrim) -> None:
        async with async_client.technology.graph.with_streaming_response.get_subgraph(
            community_ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            graph = await response.parse()
            assert_matches_type(GraphGetSubgraphResponse, graph, path=["response"])

        assert cast(Any, response.is_closed) is True
