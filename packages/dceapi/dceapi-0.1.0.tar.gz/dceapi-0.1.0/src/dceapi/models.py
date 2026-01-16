"""DCE API Python SDK - 数据模型."""

from dataclasses import dataclass
from typing import List, Optional


# ============================================================================
# 通用响应模型
# ============================================================================


@dataclass
class APIResponse:
    """API 通用响应."""

    code: int
    message: str
    data: Optional[dict] = None


@dataclass
class TokenResponse:
    """认证响应."""

    token_type: str  # Bearer
    access_token: str  # 访问令牌
    expires_in: int  # 过期时间（秒）


# ============================================================================
# 资讯数据模型
# ============================================================================


@dataclass
class Article:
    """文章."""

    id: str
    title: str
    sub_title: str
    summary: str
    show_date: str
    create_date: str
    content: str
    keywords: str
    page_name: str


@dataclass
class ArticleDetail(Article):
    """文章详情."""

    pass


@dataclass
class GetArticleByPageRequest:
    """分页获取文章请求."""

    column_id: str
    page_no: int
    page_size: int
    site_id: int = 5


@dataclass
class GetArticleByPageResponse:
    """分页获取文章响应."""

    column_id: str
    total_count: int
    result_list: List[Article]


# ============================================================================
# 通用数据模型
# ============================================================================


@dataclass
class TradeDate:
    """交易日期."""

    trade_date: str  # 对应 API 的 tradeDate 字段


@dataclass
class Variety:
    """品种."""

    variety_id: str  # 对应 API 的 varietyId
    variety_name: str  # 对应 API 的 varietyName
    variety_english_name: str  # 对应 API 的 varietyEnglishName
    pic: str
    variety_type: str  # 对应 API 的 varietyType


# ============================================================================
# 行情数据模型
# ============================================================================


@dataclass
class Quote:
    """行情数据."""

    variety: str
    contract_id: str
    deliv_month: Optional[str] = None  # 夜盘行情使用此字段
    open: Optional[str] = None
    high: Optional[str] = None
    low: Optional[str] = None
    close: Optional[str] = None
    last_clear: Optional[str] = None
    last_price: Optional[str] = None  # 夜盘行情
    clear_price: Optional[str] = None
    diff: Optional[str] = None
    diff1: Optional[str] = None
    volume: Optional[int] = None
    open_interest: Optional[int] = None
    diff_i: Optional[int] = None
    turnover: Optional[str] = None


@dataclass
class QuotesRequest:
    """行情请求."""

    trade_date: str
    trade_type: str
    variety_id: Optional[str] = None
    variety: Optional[str] = None  # 用于夜盘行情
    lang: Optional[str] = None
    statistics_type: Optional[int] = None  # 期权统计类型：0-合约，1-系列，2-品种


@dataclass
class WeekQuotesRequest:
    """周行情请求."""

    variety_code: str
    year: int
    week: int


@dataclass
class MonthQuotesRequest:
    """月行情请求."""

    variety_code: str
    year: int
    month: int


@dataclass
class ContractStatRequest:
    """合约统计请求."""

    contract_code: str
    start_date: str
    end_date: str


@dataclass
class ContractStat:
    """合约统计."""

    contract_code: str
    total_volume: int
    avg_price: float


# ============================================================================
# 交割数据模型
# ============================================================================


@dataclass
class DeliveryData:
    """交割数据."""

    variety_code: str
    delivery_month: str
    delivery_volume: int
    delivery_amount: float


@dataclass
class DeliveryDataRequest:
    """交割数据请求."""

    variety_code: str
    trade_date: str


@dataclass
class DeliveryMatch:
    """交割配对."""

    variety_code: str
    buy_member: str
    sell_member: str
    volume: int


@dataclass
class DeliveryMatchRequest:
    """交割配对请求."""

    variety_code: str
    trade_date: str


@dataclass
class WarehouseReceipt:
    """仓单."""

    variety_code: str
    warehouse_name: str
    quantity: int
    trade_date: str


@dataclass
class WarehouseReceiptRequest:
    """仓单请求."""

    variety_code: str
    trade_date: str


@dataclass
class DeliveryCost:
    """交割费用."""

    variety_code: str
    delivery_fee: float
    inspection_fee: float
    storage_fee: float


@dataclass
class WarehousePremium:
    """仓库升贴水."""

    variety_code: str
    warehouse_name: str
    premium: float


# ============================================================================
# 会员数据模型
# ============================================================================


@dataclass
class Ranking:
    """排名数据."""

    rank: str
    qty_abbr: str  # 成交量会员简称
    today_qty: int  # 今日成交量
    qty_sub: int  # 成交量增减
    buy_abbr: str  # 持买会员简称
    today_buy_qty: int  # 今日持买量
    buy_sub: int  # 持买增减
    sell_abbr: str  # 持卖会员简称
    today_sell_qty: int  # 今日持卖量
    sell_sub: int  # 持卖增减


@dataclass
class DailyRankingRequest:
    """日排名请求."""

    variety_id: str
    contract_id: str
    trade_date: str
    trade_type: str  # 1=期货, 2=期权


@dataclass
class DailyRankingResponse:
    """日排名响应."""

    contract_id: str
    today_qty: int
    qty_sub: int
    today_buy_qty: int
    buy_sub: int
    today_sell_qty: int
    sell_sub: int
    qty_future_list: List[Ranking]  # 成交量排名
    buy_future_list: List[Ranking]  # 持买排名
    sell_future_list: List[Ranking]  # 持卖排名


@dataclass
class PhaseRankingRequest:
    """阶段排名请求."""

    variety: str
    start_month: str
    end_month: str
    trade_type: str


@dataclass
class PhaseRanking:
    """阶段排名数据."""

    seq: str
    member_id: str
    member_name: str
    month_qty: float
    qty_ratio: float
    month_amt: float
    amt_ratio: float


# ============================================================================
# 交易参数数据模型
# ============================================================================


@dataclass
class TradeParam:
    """交易参数."""

    contract_id: str
    spec_buy_rate: float  # 投机买保证金率
    spec_buy: float  # 投机买保证金
    hedge_buy_rate: float  # 套保买保证金率
    hedge_buy: float  # 套保买保证金
    rise_limit_rate: float  # 涨停板比例
    rise_limit: float  # 涨停价
    fall_limit: float  # 跌停价
    trade_date: str


@dataclass
class DayTradeParamRequest:
    """日交易参数请求."""

    variety_id: str
    trade_type: str
    lang: str


@dataclass
class ContractInfo:
    """合约信息."""

    contract_id: str
    variety: str
    variety_order: str
    unit: int
    tick: str
    start_trade_date: str
    end_trade_date: str
    end_delivery_date: str
    trade_type: str


@dataclass
class ContractInfoRequest:
    """合约信息请求."""

    variety_id: str
    trade_type: str
    lang: str


@dataclass
class ArbitrageContract:
    """套利合约."""

    arbi_name: str  # 套利策略名称
    variety_name: str  # 品种名称
    arbi_contract_id: str  # 套利合约代码
    max_hand: int  # 最大下单手数
    tick: float  # 最小变动价位


@dataclass
class ArbitrageContractRequest:
    """套利合约请求."""

    lang: str


# ============================================================================
# 结算参数数据模型
# ============================================================================


@dataclass
class SettleParam:
    """结算参数."""

    variety: str
    variety_order: str
    contract_id: str
    clear_price: str  # 结算价
    open_fee: str  # 开仓手续费
    offset_fee: str  # 平仓手续费
    short_open_fee: str  # 日内开仓手续费
    short_offset_fee: str  # 日内平仓手续费
    style: str  # 限仓模式
    spec_buy_rate: str  # 投机买保证金率
    spec_sell_rate: str  # 投机卖保证金率
    hedge_buy_rate: str  # 套保买保证金率
    hedge_sell_rate: str  # 套保卖保证金率


@dataclass
class SettleParamRequest:
    """结算参数请求."""

    variety_id: str
    trade_date: str
    trade_type: str
    lang: str
