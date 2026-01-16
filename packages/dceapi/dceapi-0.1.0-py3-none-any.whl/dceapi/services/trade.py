"""DCE API Python SDK - 交易服务."""

from typing import TYPE_CHECKING, List, Optional

from ..errors import ValidationError
from ..models import (
    ArbitrageContract,
    ArbitrageContractRequest,
    ContractInfo,
    ContractInfoRequest,
    DayTradeParamRequest,
    TradeParam,
)

if TYPE_CHECKING:
    from ..http import BaseClient

# API 端点
PATH_GET_DAY_TRADE_PARAM = "/dceapi/forward/publicweb/tradepara/dayTradPara"
PATH_GET_MONTH_TRADE_PARAM = "/dceapi/forward/publicweb/tradepara/monthTradPara"
PATH_GET_CONTRACT_INFO = "/dceapi/forward/publicweb/tradepara/contractInfo"
PATH_GET_ARBITRAGE_CONTRACT = "/dceapi/forward/publicweb/tradepara/arbitrageContract"


class TradeService:
    """交易服务."""

    def __init__(self, client: "BaseClient") -> None:
        """初始化交易服务.

        Args:
            client: HTTP 客户端
        """
        self.client = client

    def get_day_trade_param(
        self,
        request: DayTradeParamRequest,
        trade_type: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> List[TradeParam]:
        """获取日交易参数.

        Args:
            request: 请求参数
            trade_type: 交易类型（覆盖配置）
            lang: 语言（覆盖配置）

        Returns:
            List[TradeParam]: 交易参数列表

        Raises:
            ValidationError: 参数验证错误
            APIError: API 错误
            NetworkError: 网络错误
        """
        if request is None:
            raise ValidationError("request", "request is required")

        result = self.client.do_request(
            method="POST",
            path=PATH_GET_DAY_TRADE_PARAM,
            body=request,
            result_type=list,
            trade_type=trade_type,
            lang=lang,
        )

        return self._parse_trade_params(result)

    def _parse_trade_params(self, data: List) -> List[TradeParam]:
        """解析交易参数数据.

        Args:
            data: 原始数据列表

        Returns:
            List[TradeParam]: TradeParam 对象列表
        """
        if not isinstance(data, list):
            return []

        params = []
        for item in data:
            if isinstance(item, dict):
                param = TradeParam(
                    contract_id=item.get("contractId", ""),
                    spec_buy_rate=float(item.get("specBuyRate", 0)),
                    spec_buy=float(item.get("specBuy", 0)),
                    hedge_buy_rate=float(item.get("hedgeBuyRate", 0)),
                    hedge_buy=float(item.get("hedgeBuy", 0)),
                    rise_limit_rate=float(item.get("riseLimitRate", 0)),
                    rise_limit=float(item.get("riseLimit", 0)),
                    fall_limit=float(item.get("fallLimit", 0)),
                    trade_date=item.get("tradeDate", ""),
                )
                params.append(param)
        return params

    def get_contract_info(
        self,
        request: ContractInfoRequest,
        trade_type: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> List[ContractInfo]:
        """获取合约信息.

        Args:
            request: 请求参数
            trade_type: 交易类型（覆盖配置）
            lang: 语言（覆盖配置）

        Returns:
            List[ContractInfo]: 合约信息列表

        Raises:
            ValidationError: 参数验证错误
            APIError: API 错误
            NetworkError: 网络错误
        """
        if request is None:
            raise ValidationError("request", "request is required")

        result = self.client.do_request(
            method="POST",
            path=PATH_GET_CONTRACT_INFO,
            body=request,
            result_type=list,
            trade_type=trade_type,
            lang=lang,
        )

        return self._parse_contract_info(result)

    def _parse_contract_info(self, data: List) -> List[ContractInfo]:
        """解析合约信息数据.

        Args:
            data: 原始数据列表

        Returns:
            List[ContractInfo]: ContractInfo 对象列表
        """
        if not isinstance(data, list):
            return []

        contracts = []
        for item in data:
            if isinstance(item, dict):
                contract = ContractInfo(
                    contract_id=item.get("contractId", ""),
                    variety=item.get("variety", ""),
                    variety_order=item.get("varietyOrder", ""),
                    unit=int(item.get("unit", 0)),
                    tick=item.get("tick", ""),
                    start_trade_date=item.get("startTradeDate", ""),
                    end_trade_date=item.get("endTradeDate", ""),
                    end_delivery_date=item.get("endDeliveryDate", ""),
                    trade_type=item.get("tradeType", ""),
                )
                contracts.append(contract)
        return contracts

    def get_arbitrage_contract(
        self,
        lang: str = "zh",
        trade_type: Optional[int] = None,
    ) -> List[ArbitrageContract]:
        """获取套利合约.

        Args:
            lang: 语言（"zh" 或 "en"）
            trade_type: 交易类型（覆盖配置）

        Returns:
            List[ArbitrageContract]: 套利合约列表

        Raises:
            APIError: API 错误
            NetworkError: 网络错误
        """
        req = ArbitrageContractRequest(lang=lang if lang else "zh")

        result = self.client.do_request(
            method="POST",
            path=PATH_GET_ARBITRAGE_CONTRACT,
            body=req,
            result_type=list,
            trade_type=trade_type,
            lang=lang,
        )

        return self._parse_arbitrage_contracts(result)

    def _parse_arbitrage_contracts(self, data: List) -> List[ArbitrageContract]:
        """解析套利合约数据.

        Args:
            data: 原始数据列表

        Returns:
            List[ArbitrageContract]: ArbitrageContract 对象列表
        """
        if not isinstance(data, list):
            return []

        contracts = []
        for item in data:
            if isinstance(item, dict):
                contract = ArbitrageContract(
                    arbi_name=item.get("arbiName", ""),
                    variety_name=item.get("varietyName", ""),
                    arbi_contract_id=item.get("arbiContractId", ""),
                    max_hand=int(item.get("maxHand", 0)),
                    tick=float(item.get("tick", 0)),
                )
                contracts.append(contract)
        return contracts
