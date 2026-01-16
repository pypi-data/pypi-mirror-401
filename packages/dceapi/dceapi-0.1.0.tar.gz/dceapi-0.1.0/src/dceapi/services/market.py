"""DCE API Python SDK - 行情服务."""

from typing import TYPE_CHECKING, List, Optional

from ..errors import ValidationError
from ..models import (
    ContractStat,
    ContractStatRequest,
    MonthQuotesRequest,
    Quote,
    QuotesRequest,
    WeekQuotesRequest,
)

if TYPE_CHECKING:
    from ..http import BaseClient

# API 端点
PATH_GET_NIGHT_QUOTES = "/dceapi/forward/publicweb/dailystat/tiNightQuotes"
PATH_GET_DAY_QUOTES = "/dceapi/forward/publicweb/dailystat/dayQuotes"
PATH_GET_WEEK_QUOTES = "/dceapi/forward/publicweb/dailystat/weekQuotes"
PATH_GET_MONTH_QUOTES = "/dceapi/forward/publicweb/dailystat/monthQuotes"
PATH_GET_CONTRACT_STAT = "/dceapi/forward/publicweb/dailystat/contractStat"


class MarketService:
    """行情服务."""

    def __init__(self, client: "BaseClient") -> None:
        """初始化行情服务.

        Args:
            client: HTTP 客户端
        """
        self.client = client

    def get_night_quotes(
        self,
        request: QuotesRequest,
        trade_type: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> List[Quote]:
        """获取夜盘行情.

        Args:
            request: 行情请求参数
            trade_type: 交易类型（覆盖配置）
            lang: 语言（覆盖配置）

        Returns:
            List[Quote]: 行情数据列表

        Raises:
            ValidationError: 参数验证错误
            APIError: API 错误
            NetworkError: 网络错误
        """
        if request is None:
            raise ValidationError("request", "request is required")

        result = self.client.do_request(
            method="POST",
            path=PATH_GET_NIGHT_QUOTES,
            body=request,
            result_type=list,
            trade_type=trade_type,
            lang=lang,
        )

        # 转换为 Quote 对象列表
        return self._parse_quotes(result)

    def get_day_quotes(
        self,
        request: QuotesRequest,
        trade_type: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> List[Quote]:
        """获取日行情.

        Args:
            request: 行情请求参数
            trade_type: 交易类型（覆盖配置）
            lang: 语言（覆盖配置）

        Returns:
            List[Quote]: 行情数据列表

        Raises:
            ValidationError: 参数验证错误
            APIError: API 错误
            NetworkError: 网络错误
        """
        if request is None:
            raise ValidationError("request", "request is required")

        result = self.client.do_request(
            method="POST",
            path=PATH_GET_DAY_QUOTES,
            body=request,
            result_type=list,
            trade_type=trade_type,
            lang=lang,
        )

        return self._parse_quotes(result)

    def get_week_quotes(
        self,
        request: WeekQuotesRequest,
        trade_type: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> List[Quote]:
        """获取周行情.

        Args:
            request: 周行情请求参数
            trade_type: 交易类型（覆盖配置）
            lang: 语言（覆盖配置）

        Returns:
            List[Quote]: 行情数据列表

        Raises:
            ValidationError: 参数验证错误
            APIError: API 错误
            NetworkError: 网络错误
        """
        if request is None:
            raise ValidationError("request", "request is required")

        result = self.client.do_request(
            method="POST",
            path=PATH_GET_WEEK_QUOTES,
            body=request,
            result_type=list,
            trade_type=trade_type,
            lang=lang,
        )

        return self._parse_quotes(result)

    def get_month_quotes(
        self,
        request: MonthQuotesRequest,
        trade_type: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> List[Quote]:
        """获取月行情.

        Args:
            request: 月行情请求参数
            trade_type: 交易类型（覆盖配置）
            lang: 语言（覆盖配置）

        Returns:
            List[Quote]: 行情数据列表

        Raises:
            ValidationError: 参数验证错误
            APIError: API 错误
            NetworkError: 网络错误
        """
        if request is None:
            raise ValidationError("request", "request is required")

        result = self.client.do_request(
            method="POST",
            path=PATH_GET_MONTH_QUOTES,
            body=request,
            result_type=list,
            trade_type=trade_type,
            lang=lang,
        )

        return self._parse_quotes(result)

    def get_contract_stat(
        self,
        request: ContractStatRequest,
        trade_type: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> List[ContractStat]:
        """获取合约统计.

        Args:
            request: 合约统计请求参数
            trade_type: 交易类型（覆盖配置）
            lang: 语言（覆盖配置）

        Returns:
            List[ContractStat]: 合约统计列表

        Raises:
            ValidationError: 参数验证错误
            APIError: API 错误
            NetworkError: 网络错误
        """
        if request is None:
            raise ValidationError("request", "request is required")

        result = self.client.do_request(
            method="POST",
            path=PATH_GET_CONTRACT_STAT,
            body=request,
            result_type=list,
            trade_type=trade_type,
            lang=lang,
        )

        return result if isinstance(result, list) else []

    def _parse_quotes(self, data: List) -> List[Quote]:
        """解析行情数据.

        Args:
            data: 原始数据列表

        Returns:
            List[Quote]: Quote 对象列表
        """
        if not isinstance(data, list):
            return []

        quotes = []
        for item in data:
            if isinstance(item, dict):
                quote = Quote(
                    variety=item.get("variety", ""),
                    contract_id=item.get("contractId", ""),
                    deliv_month=item.get("delivMonth"),
                    open=item.get("open"),
                    high=item.get("high"),
                    low=item.get("low"),
                    close=item.get("close"),
                    last_clear=item.get("lastClear"),
                    last_price=item.get("lastPrice"),
                    clear_price=item.get("clearPrice"),
                    diff=item.get("diff"),
                    diff1=item.get("diff1"),
                    volume=item.get("volumn"),  # 注意 API 拼写
                    open_interest=item.get("openInterest"),
                    diff_i=item.get("diffI"),
                    turnover=item.get("turnover"),
                )
                quotes.append(quote)
        return quotes
