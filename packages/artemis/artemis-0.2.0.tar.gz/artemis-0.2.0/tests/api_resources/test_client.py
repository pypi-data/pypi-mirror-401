# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from artemis import Artemis, AsyncArtemis
from tests.utils import assert_matches_type
from artemis.types import FetchMetricsResponse
from artemis._utils import parse_date

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestClient:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_fetch_metrics(self, client: Artemis) -> None:
        client_ = client.fetch_metrics(
            metric_names="metricNames",
            api_key="APIKey",
            end_date=parse_date("2019-12-27"),
            start_date=parse_date("2019-12-27"),
            symbols="symbols",
        )
        assert_matches_type(FetchMetricsResponse, client_, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_fetch_metrics_with_all_params(self, client: Artemis) -> None:
        client_ = client.fetch_metrics(
            metric_names="metricNames",
            api_key="APIKey",
            end_date=parse_date("2019-12-27"),
            start_date=parse_date("2019-12-27"),
            symbols="symbols",
            summarize=True,
        )
        assert_matches_type(FetchMetricsResponse, client_, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_fetch_metrics(self, client: Artemis) -> None:
        response = client.with_raw_response.fetch_metrics(
            metric_names="metricNames",
            api_key="APIKey",
            end_date=parse_date("2019-12-27"),
            start_date=parse_date("2019-12-27"),
            symbols="symbols",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(FetchMetricsResponse, client_, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_fetch_metrics(self, client: Artemis) -> None:
        with client.with_streaming_response.fetch_metrics(
            metric_names="metricNames",
            api_key="APIKey",
            end_date=parse_date("2019-12-27"),
            start_date=parse_date("2019-12-27"),
            symbols="symbols",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(FetchMetricsResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_fetch_metrics(self, client: Artemis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `metric_names` but received ''"):
            client.with_raw_response.fetch_metrics(
                metric_names="",
                api_key="APIKey",
                end_date=parse_date("2019-12-27"),
                start_date=parse_date("2019-12-27"),
                symbols="symbols",
            )


class TestAsyncClient:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_fetch_metrics(self, async_client: AsyncArtemis) -> None:
        client = await async_client.fetch_metrics(
            metric_names="metricNames",
            api_key="APIKey",
            end_date=parse_date("2019-12-27"),
            start_date=parse_date("2019-12-27"),
            symbols="symbols",
        )
        assert_matches_type(FetchMetricsResponse, client, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_fetch_metrics_with_all_params(self, async_client: AsyncArtemis) -> None:
        client = await async_client.fetch_metrics(
            metric_names="metricNames",
            api_key="APIKey",
            end_date=parse_date("2019-12-27"),
            start_date=parse_date("2019-12-27"),
            symbols="symbols",
            summarize=True,
        )
        assert_matches_type(FetchMetricsResponse, client, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_fetch_metrics(self, async_client: AsyncArtemis) -> None:
        response = await async_client.with_raw_response.fetch_metrics(
            metric_names="metricNames",
            api_key="APIKey",
            end_date=parse_date("2019-12-27"),
            start_date=parse_date("2019-12-27"),
            symbols="symbols",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(FetchMetricsResponse, client, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_fetch_metrics(self, async_client: AsyncArtemis) -> None:
        async with async_client.with_streaming_response.fetch_metrics(
            metric_names="metricNames",
            api_key="APIKey",
            end_date=parse_date("2019-12-27"),
            start_date=parse_date("2019-12-27"),
            symbols="symbols",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(FetchMetricsResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_fetch_metrics(self, async_client: AsyncArtemis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `metric_names` but received ''"):
            await async_client.with_raw_response.fetch_metrics(
                metric_names="",
                api_key="APIKey",
                end_date=parse_date("2019-12-27"),
                start_date=parse_date("2019-12-27"),
                symbols="symbols",
            )
