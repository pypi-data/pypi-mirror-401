# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from evrim import Evrim, AsyncEvrim
from tests.utils import assert_matches_type
from evrim.types.technology import MeetingGetCommunitiesResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMeetings:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_communities(self, client: Evrim) -> None:
        meeting = client.technology.meetings.get_communities(
            meeting_id="meeting_id",
        )
        assert_matches_type(MeetingGetCommunitiesResponse, meeting, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_get_communities_with_all_params(self, client: Evrim) -> None:
        meeting = client.technology.meetings.get_communities(
            meeting_id="meeting_id",
            limit=1,
            min_similarity=0,
            novelty_filter="novelty_filter",
        )
        assert_matches_type(MeetingGetCommunitiesResponse, meeting, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_get_communities(self, client: Evrim) -> None:
        response = client.technology.meetings.with_raw_response.get_communities(
            meeting_id="meeting_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        meeting = response.parse()
        assert_matches_type(MeetingGetCommunitiesResponse, meeting, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_get_communities(self, client: Evrim) -> None:
        with client.technology.meetings.with_streaming_response.get_communities(
            meeting_id="meeting_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            meeting = response.parse()
            assert_matches_type(MeetingGetCommunitiesResponse, meeting, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_get_communities(self, client: Evrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `meeting_id` but received ''"):
            client.technology.meetings.with_raw_response.get_communities(
                meeting_id="",
            )


class TestAsyncMeetings:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_communities(self, async_client: AsyncEvrim) -> None:
        meeting = await async_client.technology.meetings.get_communities(
            meeting_id="meeting_id",
        )
        assert_matches_type(MeetingGetCommunitiesResponse, meeting, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_get_communities_with_all_params(self, async_client: AsyncEvrim) -> None:
        meeting = await async_client.technology.meetings.get_communities(
            meeting_id="meeting_id",
            limit=1,
            min_similarity=0,
            novelty_filter="novelty_filter",
        )
        assert_matches_type(MeetingGetCommunitiesResponse, meeting, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_get_communities(self, async_client: AsyncEvrim) -> None:
        response = await async_client.technology.meetings.with_raw_response.get_communities(
            meeting_id="meeting_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        meeting = await response.parse()
        assert_matches_type(MeetingGetCommunitiesResponse, meeting, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_get_communities(self, async_client: AsyncEvrim) -> None:
        async with async_client.technology.meetings.with_streaming_response.get_communities(
            meeting_id="meeting_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            meeting = await response.parse()
            assert_matches_type(MeetingGetCommunitiesResponse, meeting, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_get_communities(self, async_client: AsyncEvrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `meeting_id` but received ''"):
            await async_client.technology.meetings.with_raw_response.get_communities(
                meeting_id="",
            )
