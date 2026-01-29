# Artemis

Types:

```python
from artemis.types import FetchMetricsResponse
```

Methods:

- <code title="get /data/api/{metricNames}/">client.<a href="./src/artemis/_client.py">fetch_metrics</a>(metric_names, \*\*<a href="src/artemis/types/client_fetch_metrics_params.py">params</a>) -> <a href="./src/artemis/types/fetch_metrics_response.py">FetchMetricsResponse</a></code>

# Asset

Types:

```python
from artemis.types import AssetListAssetSymbolsResponse, AssetListSupportedMetricsResponse
```

Methods:

- <code title="get /asset/symbols/">client.asset.<a href="./src/artemis/resources/asset.py">list_asset_symbols</a>() -> <a href="./src/artemis/types/asset_list_asset_symbols_response.py">AssetListAssetSymbolsResponse</a></code>
- <code title="get /supported-metrics/">client.asset.<a href="./src/artemis/resources/asset.py">list_supported_metrics</a>(\*\*<a href="src/artemis/types/asset_list_supported_metrics_params.py">params</a>) -> <a href="./src/artemis/types/asset_list_supported_metrics_response.py">AssetListSupportedMetricsResponse</a></code>
