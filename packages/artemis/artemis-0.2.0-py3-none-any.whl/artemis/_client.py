# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Union, Mapping
from datetime import date
from typing_extensions import Self, override

import httpx

from . import _exceptions
from ._qs import Querystring
from .types import client_fetch_metrics_params
from ._types import (
    Body,
    Omit,
    Query,
    Headers,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
    omit,
    not_given,
)
from ._utils import (
    is_given,
    maybe_transform,
    get_async_library,
    async_maybe_transform,
)
from ._compat import cached_property
from ._version import __version__
from ._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
    make_request_options,
)
from .types.fetch_metrics_response import FetchMetricsResponse

if TYPE_CHECKING:
    from .resources import asset
    from .resources.asset import AssetResource, AsyncAssetResource

__all__ = ["Timeout", "Transport", "ProxiesTypes", "RequestOptions", "Artemis", "AsyncArtemis", "Client", "AsyncClient"]


class Artemis(SyncAPIClient):
    # client options
    api_key: str | None

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous Artemis client instance.

        This automatically infers the `api_key` argument from the `ARTEMIS_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("ARTEMIS_API_KEY")
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("ARTEMIS_BASE_URL")
        if base_url is None:
            base_url = f"https://data-svc.artemisxyz.com"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

    @cached_property
    def asset(self) -> AssetResource:
        from .resources.asset import AssetResource

        return AssetResource(self)

    @cached_property
    def with_raw_response(self) -> ArtemisWithRawResponse:
        return ArtemisWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ArtemisWithStreamedResponse:
        return ArtemisWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    @property
    @override
    def default_query(self) -> dict[str, object]:
        return {
            **super().default_query,
            "APIKey": self.api_key if self.api_key is not None else Omit(),
            **self._custom_query,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    def fetch_metrics(
        self,
        metric_names: str,
        *,
        api_key: str,
        end_date: Union[str, date],
        start_date: Union[str, date],
        symbols: str,
        summarize: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> FetchMetricsResponse:
        """
        Fetch Metrics for Assets by Symbol

        Args:
          api_key: Your Artemis API key

          end_date: End date in YYYY-MM-DD format

          start_date: Start date in YYYY-MM-DD format

          symbols: Comma-separated list of symbols (e.g., "BTC,ETH")

          summarize: When true, calculates percent change from startDate to endDate

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not metric_names:
            raise ValueError(f"Expected a non-empty value for `metric_names` but received {metric_names!r}")
        return self.get(
            f"/data/api/{metric_names}/",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "api_key": api_key,
                        "end_date": end_date,
                        "start_date": start_date,
                        "symbols": symbols,
                        "summarize": summarize,
                    },
                    client_fetch_metrics_params.ClientFetchMetricsParams,
                ),
            ),
            cast_to=FetchMetricsResponse,
        )

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncArtemis(AsyncAPIClient):
    # client options
    api_key: str | None

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async AsyncArtemis client instance.

        This automatically infers the `api_key` argument from the `ARTEMIS_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("ARTEMIS_API_KEY")
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("ARTEMIS_BASE_URL")
        if base_url is None:
            base_url = f"https://data-svc.artemisxyz.com"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

    @cached_property
    def asset(self) -> AsyncAssetResource:
        from .resources.asset import AsyncAssetResource

        return AsyncAssetResource(self)

    @cached_property
    def with_raw_response(self) -> AsyncArtemisWithRawResponse:
        return AsyncArtemisWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncArtemisWithStreamedResponse:
        return AsyncArtemisWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    @property
    @override
    def default_query(self) -> dict[str, object]:
        return {
            **super().default_query,
            "APIKey": self.api_key if self.api_key is not None else Omit(),
            **self._custom_query,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    async def fetch_metrics(
        self,
        metric_names: str,
        *,
        api_key: str,
        end_date: Union[str, date],
        start_date: Union[str, date],
        symbols: str,
        summarize: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> FetchMetricsResponse:
        """
        Fetch Metrics for Assets by Symbol

        Args:
          api_key: Your Artemis API key

          end_date: End date in YYYY-MM-DD format

          start_date: Start date in YYYY-MM-DD format

          symbols: Comma-separated list of symbols (e.g., "BTC,ETH")

          summarize: When true, calculates percent change from startDate to endDate

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not metric_names:
            raise ValueError(f"Expected a non-empty value for `metric_names` but received {metric_names!r}")
        return await self.get(
            f"/data/api/{metric_names}/",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "api_key": api_key,
                        "end_date": end_date,
                        "start_date": start_date,
                        "symbols": symbols,
                        "summarize": summarize,
                    },
                    client_fetch_metrics_params.ClientFetchMetricsParams,
                ),
            ),
            cast_to=FetchMetricsResponse,
        )

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class ArtemisWithRawResponse:
    _client: Artemis

    def __init__(self, client: Artemis) -> None:
        self._client = client

        self.fetch_metrics = to_raw_response_wrapper(
            client.fetch_metrics,
        )

    @cached_property
    def asset(self) -> asset.AssetResourceWithRawResponse:
        from .resources.asset import AssetResourceWithRawResponse

        return AssetResourceWithRawResponse(self._client.asset)


class AsyncArtemisWithRawResponse:
    _client: AsyncArtemis

    def __init__(self, client: AsyncArtemis) -> None:
        self._client = client

        self.fetch_metrics = async_to_raw_response_wrapper(
            client.fetch_metrics,
        )

    @cached_property
    def asset(self) -> asset.AsyncAssetResourceWithRawResponse:
        from .resources.asset import AsyncAssetResourceWithRawResponse

        return AsyncAssetResourceWithRawResponse(self._client.asset)


class ArtemisWithStreamedResponse:
    _client: Artemis

    def __init__(self, client: Artemis) -> None:
        self._client = client

        self.fetch_metrics = to_streamed_response_wrapper(
            client.fetch_metrics,
        )

    @cached_property
    def asset(self) -> asset.AssetResourceWithStreamingResponse:
        from .resources.asset import AssetResourceWithStreamingResponse

        return AssetResourceWithStreamingResponse(self._client.asset)


class AsyncArtemisWithStreamedResponse:
    _client: AsyncArtemis

    def __init__(self, client: AsyncArtemis) -> None:
        self._client = client

        self.fetch_metrics = async_to_streamed_response_wrapper(
            client.fetch_metrics,
        )

    @cached_property
    def asset(self) -> asset.AsyncAssetResourceWithStreamingResponse:
        from .resources.asset import AsyncAssetResourceWithStreamingResponse

        return AsyncAssetResourceWithStreamingResponse(self._client.asset)


Client = Artemis

AsyncClient = AsyncArtemis
