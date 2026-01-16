"""DCE API Python SDK.

大连商品交易所 (DCE) API v1.0 Python SDK

基本使用:
    >>> from dceapi import Client
    >>> client = Client.from_env()
    >>> trade_date = client.common.get_curr_trade_date()
    >>> print(f"当前交易日期: {trade_date.date}")
"""

__version__ = "0.1.0"

from .client import Client
from .config import Config
from .errors import (
    APIError,
    AuthError,
    DCEAPIException,
    ErrorCode,
    NetworkError,
    TokenError,
    ValidationError,
)
from .models import (
    ArbitrageContract,
    Article,
    ArticleDetail,
    ContractInfo,
    ContractInfoRequest,
    ContractStat,
    ContractStatRequest,
    DailyRankingRequest,
    DailyRankingResponse,
    DayTradeParamRequest,
    DeliveryCost,
    DeliveryData,
    DeliveryDataRequest,
    DeliveryMatch,
    GetArticleByPageRequest,
    GetArticleByPageResponse,
    MonthQuotesRequest,
    PhaseRanking,
    PhaseRankingRequest,
    Quote,
    QuotesRequest,
    Ranking,
    SettleParam,
    SettleParamRequest,
    TradeDate,
    TradeParam,
    Variety,
    WarehousePremium,
    WarehouseReceipt,
    WarehouseReceiptRequest,
    WeekQuotesRequest,
)

__all__ = [
    # 版本
    "__version__",
    # 客户端
    "Client",
    "Config",
    # 错误
    "DCEAPIException",
    "APIError",
    "AuthError",
    "NetworkError",
    "ValidationError",
    "TokenError",
    "ErrorCode",
    # 通用模型
    "TradeDate",
    "Variety",
    # 资讯模型
    "Article",
    "ArticleDetail",
    "GetArticleByPageRequest",
    "GetArticleByPageResponse",
    # 行情模型
    "Quote",
    "QuotesRequest",
    "WeekQuotesRequest",
    "MonthQuotesRequest",
    "ContractStatRequest",
    "ContractStat",
    # 交易模型
    "TradeParam",
    "DayTradeParamRequest",
    "ContractInfo",
    "ContractInfoRequest",
    "ArbitrageContract",
    # 结算模型
    "SettleParam",
    "SettleParamRequest",
    # 会员模型
    "Ranking",
    "DailyRankingRequest",
    "DailyRankingResponse",
    "PhaseRanking",
    "PhaseRankingRequest",
    # 交割模型
    "DeliveryData",
    "DeliveryDataRequest",
    "DeliveryMatch",
    "WarehouseReceipt",
    "WarehouseReceiptRequest",
    "DeliveryCost",
    "WarehousePremium",
]
