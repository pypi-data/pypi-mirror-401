# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from evrim import Evrim, AsyncEvrim
from tests.utils import assert_matches_type
from evrim.types.technology import AnalyticsGetCommunityStatsResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAnalytics:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_community_stats(self, client: Evrim) -> None:
        analytics = client.technology.analytics.get_community_stats(
            "community_id",
        )
        assert_matches_type(AnalyticsGetCommunityStatsResponse, analytics, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_get_community_stats(self, client: Evrim) -> None:
        response = client.technology.analytics.with_raw_response.get_community_stats(
            "community_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        analytics = response.parse()
        assert_matches_type(AnalyticsGetCommunityStatsResponse, analytics, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_get_community_stats(self, client: Evrim) -> None:
        with client.technology.analytics.with_streaming_response.get_community_stats(
            "community_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            analytics = response.parse()
            assert_matches_type(AnalyticsGetCommunityStatsResponse, analytics, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_get_community_stats(self, client: Evrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `community_id` but received ''"):
            client.technology.analytics.with_raw_response.get_community_stats(
                "",
            )


class TestAsyncAnalytics:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_community_stats(self, async_client: AsyncEvrim) -> None:
        analytics = await async_client.technology.analytics.get_community_stats(
            "community_id",
        )
        assert_matches_type(AnalyticsGetCommunityStatsResponse, analytics, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_get_community_stats(self, async_client: AsyncEvrim) -> None:
        response = await async_client.technology.analytics.with_raw_response.get_community_stats(
            "community_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        analytics = await response.parse()
        assert_matches_type(AnalyticsGetCommunityStatsResponse, analytics, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_get_community_stats(self, async_client: AsyncEvrim) -> None:
        async with async_client.technology.analytics.with_streaming_response.get_community_stats(
            "community_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            analytics = await response.parse()
            assert_matches_type(AnalyticsGetCommunityStatsResponse, analytics, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_get_community_stats(self, async_client: AsyncEvrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `community_id` but received ''"):
            await async_client.technology.analytics.with_raw_response.get_community_stats(
                "",
            )
