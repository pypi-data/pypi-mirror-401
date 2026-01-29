# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import date
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ClientFetchMetricsParams"]


class ClientFetchMetricsParams(TypedDict, total=False):
    api_key: Required[Annotated[str, PropertyInfo(alias="APIKey")]]
    """Your Artemis API key"""

    end_date: Required[Annotated[Union[str, date], PropertyInfo(alias="endDate", format="iso8601")]]
    """End date in YYYY-MM-DD format"""

    start_date: Required[Annotated[Union[str, date], PropertyInfo(alias="startDate", format="iso8601")]]
    """Start date in YYYY-MM-DD format"""

    symbols: Required[str]
    """Comma-separated list of symbols (e.g., "BTC,ETH")"""

    summarize: bool
    """When true, calculates percent change from startDate to endDate"""
