# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from .._models import BaseModel

__all__ = ["AssetListSupportedMetricsResponse", "MetricMetricItem", "MetricMetricItemCut", "MetricMetricItemTag"]


class MetricMetricItemCut(BaseModel):
    dimension_type: Optional[str] = None

    granularity: Optional[str] = None


class MetricMetricItemTag(BaseModel):
    label: Optional[str] = None

    value: Optional[str] = None


class MetricMetricItem(BaseModel):
    accepts_date: Optional[bool] = None

    aggregation_type: Optional[str] = None

    base_metric: Optional[str] = None

    cuts: Optional[List[MetricMetricItemCut]] = None

    description: Optional[str] = None

    internal_data_source: Optional[str] = None

    label: Optional[str] = None

    methodology: Optional[str] = None

    source: Optional[str] = None

    source_link: Optional[str] = None

    tags: Optional[List[MetricMetricItemTag]] = None

    thumbnail_url: Optional[str] = None

    unit: Optional[str] = None


class AssetListSupportedMetricsResponse(BaseModel):
    metrics: List[Dict[str, MetricMetricItem]]
