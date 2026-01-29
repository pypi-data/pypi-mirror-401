# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import TypeAlias

from .._models import BaseModel

__all__ = ["AssetListAssetSymbolsResponse", "AssetListAssetSymbolsResponseItem"]


class AssetListAssetSymbolsResponseItem(BaseModel):
    artemis_id: str

    symbol: str

    title: str

    coingecko_id: Optional[str] = None

    color: Optional[str] = None


AssetListAssetSymbolsResponse: TypeAlias = List[AssetListAssetSymbolsResponseItem]
