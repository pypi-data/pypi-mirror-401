# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from evrim import Evrim, AsyncEvrim
from tests.utils import assert_matches_type
from evrim.types.technology import (
    CommunityListResponse,
    CommunitySearchResponse,
    CommunityRetrieveResponse,
    CommunityGetTopicsResponse,
    CommunityGetMeetingsResponse,
    CommunityGetNeighborsResponse,
    CommunityGetPublicationsResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCommunities:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Evrim) -> None:
        community = client.technology.communities.retrieve(
            "community_id",
        )
        assert_matches_type(CommunityRetrieveResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Evrim) -> None:
        response = client.technology.communities.with_raw_response.retrieve(
            "community_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        community = response.parse()
        assert_matches_type(CommunityRetrieveResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Evrim) -> None:
        with client.technology.communities.with_streaming_response.retrieve(
            "community_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            community = response.parse()
            assert_matches_type(CommunityRetrieveResponse, community, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Evrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `community_id` but received ''"):
            client.technology.communities.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: Evrim) -> None:
        community = client.technology.communities.list()
        assert_matches_type(CommunityListResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Evrim) -> None:
        community = client.technology.communities.list(
            end=0,
            min_topics=0,
            novelty_score="novelty_score",
            sort_by="novelty",
            sort_order="asc",
            start=0,
        )
        assert_matches_type(CommunityListResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Evrim) -> None:
        response = client.technology.communities.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        community = response.parse()
        assert_matches_type(CommunityListResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Evrim) -> None:
        with client.technology.communities.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            community = response.parse()
            assert_matches_type(CommunityListResponse, community, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_meetings(self, client: Evrim) -> None:
        community = client.technology.communities.get_meetings(
            community_id="community_id",
        )
        assert_matches_type(CommunityGetMeetingsResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_meetings_with_all_params(self, client: Evrim) -> None:
        community = client.technology.communities.get_meetings(
            community_id="community_id",
            full=True,
            limit=1,
            min_similarity=0,
            offset=0,
        )
        assert_matches_type(CommunityGetMeetingsResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_get_meetings(self, client: Evrim) -> None:
        response = client.technology.communities.with_raw_response.get_meetings(
            community_id="community_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        community = response.parse()
        assert_matches_type(CommunityGetMeetingsResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_get_meetings(self, client: Evrim) -> None:
        with client.technology.communities.with_streaming_response.get_meetings(
            community_id="community_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            community = response.parse()
            assert_matches_type(CommunityGetMeetingsResponse, community, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_get_meetings(self, client: Evrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `community_id` but received ''"):
            client.technology.communities.with_raw_response.get_meetings(
                community_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_neighbors(self, client: Evrim) -> None:
        community = client.technology.communities.get_neighbors(
            community_id="community_id",
        )
        assert_matches_type(CommunityGetNeighborsResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_neighbors_with_all_params(self, client: Evrim) -> None:
        community = client.technology.communities.get_neighbors(
            community_id="community_id",
            direction="direction",
            limit=1,
            min_strength=0,
            sort_order="asc",
        )
        assert_matches_type(CommunityGetNeighborsResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_get_neighbors(self, client: Evrim) -> None:
        response = client.technology.communities.with_raw_response.get_neighbors(
            community_id="community_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        community = response.parse()
        assert_matches_type(CommunityGetNeighborsResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_get_neighbors(self, client: Evrim) -> None:
        with client.technology.communities.with_streaming_response.get_neighbors(
            community_id="community_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            community = response.parse()
            assert_matches_type(CommunityGetNeighborsResponse, community, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_get_neighbors(self, client: Evrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `community_id` but received ''"):
            client.technology.communities.with_raw_response.get_neighbors(
                community_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_publications(self, client: Evrim) -> None:
        community = client.technology.communities.get_publications(
            community_id="community_id",
        )
        assert_matches_type(CommunityGetPublicationsResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_publications_with_all_params(self, client: Evrim) -> None:
        community = client.technology.communities.get_publications(
            community_id="community_id",
            limit=1,
            offset=0,
            sort_by="year",
            sort_order="asc",
            year_max=0,
            year_min=0,
        )
        assert_matches_type(CommunityGetPublicationsResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_get_publications(self, client: Evrim) -> None:
        response = client.technology.communities.with_raw_response.get_publications(
            community_id="community_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        community = response.parse()
        assert_matches_type(CommunityGetPublicationsResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_get_publications(self, client: Evrim) -> None:
        with client.technology.communities.with_streaming_response.get_publications(
            community_id="community_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            community = response.parse()
            assert_matches_type(CommunityGetPublicationsResponse, community, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_get_publications(self, client: Evrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `community_id` but received ''"):
            client.technology.communities.with_raw_response.get_publications(
                community_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_topics(self, client: Evrim) -> None:
        community = client.technology.communities.get_topics(
            community_id="community_id",
        )
        assert_matches_type(CommunityGetTopicsResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_topics_with_all_params(self, client: Evrim) -> None:
        community = client.technology.communities.get_topics(
            community_id="community_id",
            limit=1,
            offset=0,
            sort_by="name",
            sort_order="asc",
        )
        assert_matches_type(CommunityGetTopicsResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_get_topics(self, client: Evrim) -> None:
        response = client.technology.communities.with_raw_response.get_topics(
            community_id="community_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        community = response.parse()
        assert_matches_type(CommunityGetTopicsResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_get_topics(self, client: Evrim) -> None:
        with client.technology.communities.with_streaming_response.get_topics(
            community_id="community_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            community = response.parse()
            assert_matches_type(CommunityGetTopicsResponse, community, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_get_topics(self, client: Evrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `community_id` but received ''"):
            client.technology.communities.with_raw_response.get_topics(
                community_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_search(self, client: Evrim) -> None:
        community = client.technology.communities.search(
            q="x",
        )
        assert_matches_type(CommunitySearchResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_search_with_all_params(self, client: Evrim) -> None:
        community = client.technology.communities.search(
            q="x",
            limit=1,
            offset=0,
            sort_by="novelty",
            sort_order="asc",
        )
        assert_matches_type(CommunitySearchResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_search(self, client: Evrim) -> None:
        response = client.technology.communities.with_raw_response.search(
            q="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        community = response.parse()
        assert_matches_type(CommunitySearchResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_search(self, client: Evrim) -> None:
        with client.technology.communities.with_streaming_response.search(
            q="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            community = response.parse()
            assert_matches_type(CommunitySearchResponse, community, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncCommunities:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncEvrim) -> None:
        community = await async_client.technology.communities.retrieve(
            "community_id",
        )
        assert_matches_type(CommunityRetrieveResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncEvrim) -> None:
        response = await async_client.technology.communities.with_raw_response.retrieve(
            "community_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        community = await response.parse()
        assert_matches_type(CommunityRetrieveResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncEvrim) -> None:
        async with async_client.technology.communities.with_streaming_response.retrieve(
            "community_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            community = await response.parse()
            assert_matches_type(CommunityRetrieveResponse, community, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncEvrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `community_id` but received ''"):
            await async_client.technology.communities.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncEvrim) -> None:
        community = await async_client.technology.communities.list()
        assert_matches_type(CommunityListResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncEvrim) -> None:
        community = await async_client.technology.communities.list(
            end=0,
            min_topics=0,
            novelty_score="novelty_score",
            sort_by="novelty",
            sort_order="asc",
            start=0,
        )
        assert_matches_type(CommunityListResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEvrim) -> None:
        response = await async_client.technology.communities.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        community = await response.parse()
        assert_matches_type(CommunityListResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEvrim) -> None:
        async with async_client.technology.communities.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            community = await response.parse()
            assert_matches_type(CommunityListResponse, community, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_meetings(self, async_client: AsyncEvrim) -> None:
        community = await async_client.technology.communities.get_meetings(
            community_id="community_id",
        )
        assert_matches_type(CommunityGetMeetingsResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_meetings_with_all_params(self, async_client: AsyncEvrim) -> None:
        community = await async_client.technology.communities.get_meetings(
            community_id="community_id",
            full=True,
            limit=1,
            min_similarity=0,
            offset=0,
        )
        assert_matches_type(CommunityGetMeetingsResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_get_meetings(self, async_client: AsyncEvrim) -> None:
        response = await async_client.technology.communities.with_raw_response.get_meetings(
            community_id="community_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        community = await response.parse()
        assert_matches_type(CommunityGetMeetingsResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_get_meetings(self, async_client: AsyncEvrim) -> None:
        async with async_client.technology.communities.with_streaming_response.get_meetings(
            community_id="community_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            community = await response.parse()
            assert_matches_type(CommunityGetMeetingsResponse, community, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_get_meetings(self, async_client: AsyncEvrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `community_id` but received ''"):
            await async_client.technology.communities.with_raw_response.get_meetings(
                community_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_neighbors(self, async_client: AsyncEvrim) -> None:
        community = await async_client.technology.communities.get_neighbors(
            community_id="community_id",
        )
        assert_matches_type(CommunityGetNeighborsResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_neighbors_with_all_params(self, async_client: AsyncEvrim) -> None:
        community = await async_client.technology.communities.get_neighbors(
            community_id="community_id",
            direction="direction",
            limit=1,
            min_strength=0,
            sort_order="asc",
        )
        assert_matches_type(CommunityGetNeighborsResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_get_neighbors(self, async_client: AsyncEvrim) -> None:
        response = await async_client.technology.communities.with_raw_response.get_neighbors(
            community_id="community_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        community = await response.parse()
        assert_matches_type(CommunityGetNeighborsResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_get_neighbors(self, async_client: AsyncEvrim) -> None:
        async with async_client.technology.communities.with_streaming_response.get_neighbors(
            community_id="community_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            community = await response.parse()
            assert_matches_type(CommunityGetNeighborsResponse, community, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_get_neighbors(self, async_client: AsyncEvrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `community_id` but received ''"):
            await async_client.technology.communities.with_raw_response.get_neighbors(
                community_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_publications(self, async_client: AsyncEvrim) -> None:
        community = await async_client.technology.communities.get_publications(
            community_id="community_id",
        )
        assert_matches_type(CommunityGetPublicationsResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_publications_with_all_params(self, async_client: AsyncEvrim) -> None:
        community = await async_client.technology.communities.get_publications(
            community_id="community_id",
            limit=1,
            offset=0,
            sort_by="year",
            sort_order="asc",
            year_max=0,
            year_min=0,
        )
        assert_matches_type(CommunityGetPublicationsResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_get_publications(self, async_client: AsyncEvrim) -> None:
        response = await async_client.technology.communities.with_raw_response.get_publications(
            community_id="community_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        community = await response.parse()
        assert_matches_type(CommunityGetPublicationsResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_get_publications(self, async_client: AsyncEvrim) -> None:
        async with async_client.technology.communities.with_streaming_response.get_publications(
            community_id="community_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            community = await response.parse()
            assert_matches_type(CommunityGetPublicationsResponse, community, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_get_publications(self, async_client: AsyncEvrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `community_id` but received ''"):
            await async_client.technology.communities.with_raw_response.get_publications(
                community_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_topics(self, async_client: AsyncEvrim) -> None:
        community = await async_client.technology.communities.get_topics(
            community_id="community_id",
        )
        assert_matches_type(CommunityGetTopicsResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_topics_with_all_params(self, async_client: AsyncEvrim) -> None:
        community = await async_client.technology.communities.get_topics(
            community_id="community_id",
            limit=1,
            offset=0,
            sort_by="name",
            sort_order="asc",
        )
        assert_matches_type(CommunityGetTopicsResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_get_topics(self, async_client: AsyncEvrim) -> None:
        response = await async_client.technology.communities.with_raw_response.get_topics(
            community_id="community_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        community = await response.parse()
        assert_matches_type(CommunityGetTopicsResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_get_topics(self, async_client: AsyncEvrim) -> None:
        async with async_client.technology.communities.with_streaming_response.get_topics(
            community_id="community_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            community = await response.parse()
            assert_matches_type(CommunityGetTopicsResponse, community, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_get_topics(self, async_client: AsyncEvrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `community_id` but received ''"):
            await async_client.technology.communities.with_raw_response.get_topics(
                community_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_search(self, async_client: AsyncEvrim) -> None:
        community = await async_client.technology.communities.search(
            q="x",
        )
        assert_matches_type(CommunitySearchResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_search_with_all_params(self, async_client: AsyncEvrim) -> None:
        community = await async_client.technology.communities.search(
            q="x",
            limit=1,
            offset=0,
            sort_by="novelty",
            sort_order="asc",
        )
        assert_matches_type(CommunitySearchResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_search(self, async_client: AsyncEvrim) -> None:
        response = await async_client.technology.communities.with_raw_response.search(
            q="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        community = await response.parse()
        assert_matches_type(CommunitySearchResponse, community, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_search(self, async_client: AsyncEvrim) -> None:
        async with async_client.technology.communities.with_streaming_response.search(
            q="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            community = await response.parse()
            assert_matches_type(CommunitySearchResponse, community, path=["response"])

        assert cast(Any, response.is_closed) is True
