# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import datetime
from typing import Dict, List

from .._models import BaseModel

__all__ = ["FetchMetricsResponse", "Data", "DataSymbolsDataSymbolsItem"]


class DataSymbolsDataSymbolsItem(BaseModel):
    date: datetime.date

    val: float


class Data(BaseModel):
    symbols: Dict[str, Dict[str, List[DataSymbolsDataSymbolsItem]]]
    """
    Object where keys are symbol names (e.g., 'btc', 'eth') and values are their
    metric data
    """


class FetchMetricsResponse(BaseModel):
    data: Data
