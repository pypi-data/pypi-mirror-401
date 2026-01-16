"""DCE API Python SDK - 交割服务."""

from typing import TYPE_CHECKING, List, Optional

from ..errors import ValidationError
from ..models import (
    DeliveryCost,
    DeliveryData,
    DeliveryDataRequest,
    DeliveryMatch,
    DeliveryMatchRequest,
    WarehousePremium,
    WarehouseReceipt,
    WarehouseReceiptRequest,
)

if TYPE_CHECKING:
    from ..http import BaseClient

# API 端点
PATH_GET_DELIVERY_DATA = "/dceapi/forward/publicweb/deliverystat/delivery"
PATH_GET_DELIVERY_MATCH = "/dceapi/forward/publicweb/deliverystat/deliveryMatch"
PATH_GET_WAREHOUSE_RECEIPT = "/dceapi/forward/publicweb/deliverystat/warehouseReceipt"
PATH_GET_DELIVERY_COST = "/dceapi/forward/publicweb/deliverypara/deliveryCosts"
PATH_GET_WAREHOUSE_PREMIUM = "/dceapi/forward/publicweb/deliverypara/floatingAgio"


class DeliveryService:
    """交割服务."""

    def __init__(self, client: "BaseClient") -> None:
        """初始化交割服务.

        Args:
            client: HTTP 客户端
        """
        self.client = client

    def get_delivery_data(
        self,
        request: DeliveryDataRequest,
        trade_type: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> List[DeliveryData]:
        """获取交割数据.

        Args:
            request: 请求参数
            trade_type: 交易类型（覆盖配置）
            lang: 语言（覆盖配置）

        Returns:
            List[DeliveryData]: 交割数据列表

        Raises:
            ValidationError: 参数验证错误
            APIError: API 错误
            NetworkError: 网络错误
        """
        if request is None:
            raise ValidationError("request", "request is required")

        result = self.client.do_request(
            method="POST",
            path=PATH_GET_DELIVERY_DATA,
            body=request,
            result_type=list,
            trade_type=trade_type,
            lang=lang,
        )

        return result if isinstance(result, list) else []

    def get_delivery_match(
        self,
        request: DeliveryMatchRequest,
        trade_type: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> List[DeliveryMatch]:
        """获取交割配对数据.

        Args:
            request: 请求参数
            trade_type: 交易类型（覆盖配置）
            lang: 语言（覆盖配置）

        Returns:
            List[DeliveryMatch]: 交割配对列表

        Raises:
            ValidationError: 参数验证错误
            APIError: API 错误
            NetworkError: 网络错误
        """
        if request is None:
            raise ValidationError("request", "request is required")

        result = self.client.do_request(
            method="POST",
            path=PATH_GET_DELIVERY_MATCH,
            body=request,
            result_type=list,
            trade_type=trade_type,
            lang=lang,
        )

        return result if isinstance(result, list) else []

    def get_warehouse_receipt(
        self,
        request: WarehouseReceiptRequest,
        trade_type: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> List[WarehouseReceipt]:
        """获取仓单数据.

        Args:
            request: 请求参数
            trade_type: 交易类型（覆盖配置）
            lang: 语言（覆盖配置）

        Returns:
            List[WarehouseReceipt]: 仓单列表

        Raises:
            ValidationError: 参数验证错误
            APIError: API 错误
            NetworkError: 网络错误
        """
        if request is None:
            raise ValidationError("request", "request is required")

        result = self.client.do_request(
            method="POST",
            path=PATH_GET_WAREHOUSE_RECEIPT,
            body=request,
            result_type=list,
            trade_type=trade_type,
            lang=lang,
        )

        return result if isinstance(result, list) else []

    def get_delivery_cost(
        self,
        variety: str,
        trade_type: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> DeliveryCost:
        """获取交割费用.

        Args:
            variety: 品种代码
            trade_type: 交易类型（覆盖配置）
            lang: 语言（覆盖配置）

        Returns:
            DeliveryCost: 交割费用

        Raises:
            ValidationError: 参数验证错误
            APIError: API 错误
            NetworkError: 网络错误
        """
        if not variety:
            raise ValidationError("variety", "variety is required")

        req_body = {"varietyCode": variety}

        result = self.client.do_request(
            method="POST",
            path=PATH_GET_DELIVERY_COST,
            body=req_body,
            result_type=DeliveryCost,
            trade_type=trade_type,
            lang=lang,
        )

        return result

    def get_warehouse_premium(
        self,
        variety: str,
        trade_type: Optional[int] = None,
        lang: Optional[str] = None,
    ) -> List[WarehousePremium]:
        """获取仓库升贴水.

        Args:
            variety: 品种代码
            trade_type: 交易类型（覆盖配置）
            lang: 语言（覆盖配置）

        Returns:
            List[WarehousePremium]: 仓库升贴水列表

        Raises:
            ValidationError: 参数验证错误
            APIError: API 错误
            NetworkError: 网络错误
        """
        if not variety:
            raise ValidationError("variety", "variety is required")

        req_body = {"varietyCode": variety}

        result = self.client.do_request(
            method="POST",
            path=PATH_GET_WAREHOUSE_PREMIUM,
            body=req_body,
            result_type=list,
            trade_type=trade_type,
            lang=lang,
        )

        return result if isinstance(result, list) else []
