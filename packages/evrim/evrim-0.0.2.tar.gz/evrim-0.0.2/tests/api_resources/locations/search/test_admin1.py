# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from evrim import Evrim, AsyncEvrim
from tests.utils import assert_matches_type
from evrim.types.locations.search import Admin1ListMeetingsResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAdmin1:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_meetings(self, client: Evrim) -> None:
        admin1 = client.locations.search.admin1.list_meetings(
            admin1="x",
        )
        assert_matches_type(Admin1ListMeetingsResponse, admin1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_meetings_with_all_params(self, client: Evrim) -> None:
        admin1 = client.locations.search.admin1.list_meetings(
            admin1="x",
            end=0,
            start=0,
        )
        assert_matches_type(Admin1ListMeetingsResponse, admin1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list_meetings(self, client: Evrim) -> None:
        response = client.locations.search.admin1.with_raw_response.list_meetings(
            admin1="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        admin1 = response.parse()
        assert_matches_type(Admin1ListMeetingsResponse, admin1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list_meetings(self, client: Evrim) -> None:
        with client.locations.search.admin1.with_streaming_response.list_meetings(
            admin1="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            admin1 = response.parse()
            assert_matches_type(Admin1ListMeetingsResponse, admin1, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAdmin1:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_meetings(self, async_client: AsyncEvrim) -> None:
        admin1 = await async_client.locations.search.admin1.list_meetings(
            admin1="x",
        )
        assert_matches_type(Admin1ListMeetingsResponse, admin1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_meetings_with_all_params(self, async_client: AsyncEvrim) -> None:
        admin1 = await async_client.locations.search.admin1.list_meetings(
            admin1="x",
            end=0,
            start=0,
        )
        assert_matches_type(Admin1ListMeetingsResponse, admin1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list_meetings(self, async_client: AsyncEvrim) -> None:
        response = await async_client.locations.search.admin1.with_raw_response.list_meetings(
            admin1="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        admin1 = await response.parse()
        assert_matches_type(Admin1ListMeetingsResponse, admin1, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list_meetings(self, async_client: AsyncEvrim) -> None:
        async with async_client.locations.search.admin1.with_streaming_response.list_meetings(
            admin1="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            admin1 = await response.parse()
            assert_matches_type(Admin1ListMeetingsResponse, admin1, path=["response"])

        assert cast(Any, response.is_closed) is True
