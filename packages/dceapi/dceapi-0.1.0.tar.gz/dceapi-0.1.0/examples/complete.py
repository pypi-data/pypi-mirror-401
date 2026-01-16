"""DCE API Python SDK - 完整示例.

演示 SDK 的所有主要功能，包括:
- 客户端配置
- 通用服务（交易日期、品种列表）
- 资讯服务（文章列表、文章详情）
- 行情服务（日行情、周行情、月行情）
- 交易服务（交易参数、合约信息、套利合约）
- 结算服务（结算参数）
- 会员服务（日排名、阶段排名）
- 交割服务（交割数据、仓单、费用）
- 错误处理

运行前请设置环境变量:
    export DCE_API_KEY="your-api-key"
    export DCE_SECRET="your-secret"

然后运行:
    python examples/complete.py
"""

import sys
from pathlib import Path

# 添加 src 目录到 Python 路径（用于开发环境）
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from dceapi import (
    APIError,
    AuthError,
    Client,
    Config,
    ContractInfoRequest,
    DailyRankingRequest,
    DailyRankingResponse,
    DayTradeParamRequest,
    DeliveryDataRequest,
    GetArticleByPageRequest,
    NetworkError,
    PhaseRankingRequest,
    QuotesRequest,
    SettleParamRequest,
    ValidationError,
    WarehouseReceiptRequest,
    WeekQuotesRequest,
)


class DCEAPIDemo:
    """DCE API 演示类."""

    def __init__(self):
        """初始化演示."""
        self.client = self._create_client()

    def _create_client(self) -> Client:
        """创建客户端."""
        try:
            client = Client.from_env()
            print("✓ 客户端创建成功")
            return client
        except ValidationError as e:
            print(f"✗ 配置错误: {e}")
            print("\n请设置以下环境变量:")
            print("  export DCE_API_KEY='your-api-key'")
            print("  export DCE_SECRET='your-secret'")
            sys.exit(1)

    def run_common_examples(self):
        """运行通用服务示例."""
        print("\n" + "=" * 60)
        print("CommonService 通用服务示例")
        print("=" * 60)

        # 获取当前交易日期
        try:
            print("\n--- GetCurrTradeDate 获取当前交易日期 ---")
            trade_date = self.client.common.get_curr_trade_date()
            print(f"当前交易日期: {trade_date.trade_date}")
        except Exception as e:
            print(f"错误: {e}")

        # 获取期货品种
        try:
            print("\n--- GetVarietyList 获取品种列表 ---")
            varieties = self.client.common.get_variety_list(trade_type=1)
            print(f"品种数量: {len(varieties)}")
            for i, v in enumerate(varieties):
                if i >= 5:
                    print(f"  ... 还有 {len(varieties) - 5} 个品种")
                    break
                print(f"  - {v.variety_name} ({v.variety_id}) - {v.variety_type}")
        except Exception as e:
            print(f"错误: {e}")

    def run_news_examples(self):
        """运行资讯服务示例."""
        print("\n" + "=" * 60)
        print("NewsService 资讯服务示例")
        print("=" * 60)

        # 获取交易所公告
        try:
            print("\n--- GetArticleByPage 获取交易所公告 (columnId=244) ---")
            req = GetArticleByPageRequest(
                column_id="244",  # 交易所公告
                page_no=1,
                page_size=5,
                site_id=5
            )
            result = self.client.news.get_article_by_page(req)
            print(f"总文章数: {result.total_count}, 当前页: {len(result.result_list)} 篇")
            for article in result.result_list:
                print(f"  - [{article.show_date}] {article.title}")
        except Exception as e:
            print(f"错误: {e}")

        # 获取交易所通知
        try:
            print("\n--- GetArticleByPage 获取交易所通知 (columnId=245) ---")
            req = GetArticleByPageRequest(
                column_id="245",  # 交易所通知
                page_no=1,
                page_size=3,
                site_id=5
            )
            result = self.client.news.get_article_by_page(req)
            print(f"总通知数: {result.total_count}")
            for article in result.result_list:
                print(f"  - [{article.show_date}] {article.title}")
        except Exception as e:
            print(f"错误: {e}")

    def run_market_examples(self):
        """运行行情服务示例."""
        print("\n" + "=" * 60)
        print("MarketService 行情服务示例")
        print("=" * 60)

        # 获取当前交易日期
        try:
            trade_date = self.client.common.get_curr_trade_date()
            current_date = trade_date.trade_date
            print(f"当前交易日期: {current_date}")
        except Exception as e:
            print(f"无法获取交易日期: {e}")
            current_date = "20251230"

        # 获取日行情
        try:
            print(f"\n--- GetDayQuotes 获取日行情 (豆粕 m) ---")
            req = QuotesRequest(
                variety_id="m",
                trade_date="20251230",
                trade_type="1",
                lang="zh"
            )
            quotes = self.client.market.get_day_quotes(req)
            print(f"豆粕日行情, 合约数: {len(quotes)}")
            count = 0
            for q in quotes:
                if not q.contract_id or q.variety == "总计":
                    continue
                if count >= 3:
                    print("  ... 还有更多合约")
                    break
                print(f"  合约: {q.contract_id} | 开: {q.open} 高: {q.high} "
                      f"低: {q.low} 收: {q.close} | 成交量: {q.volume}")
                count += 1
        except Exception as e:
            print(f"错误: {e}")

        # 获取夜盘行情
        try:
            print(f"\n--- GetNightQuotes 获取夜盘行情 (铁矿石 i) ---")
            req = QuotesRequest(
                variety="i",
                trade_date="20251230",
                trade_type="1"
            )
            quotes = self.client.market.get_night_quotes(req)
            print(f"铁矿石夜盘行情, 合约数: {len(quotes)}")
            count = 0
            for q in quotes:
                contract = q.deliv_month
                if not contract or q.variety == "总计":
                    continue
                if count >= 3:
                    break
                print(f"  合约: {contract} | 最新价: {q.last_price} | 持仓量: {q.open_interest}")
                count += 1
        except Exception as e:
            print(f"错误: {e}")

    def run_trade_examples(self):
        """运行交易服务示例."""
        print("\n" + "=" * 60)
        print("TradeService 交易服务示例")
        print("=" * 60)

        # 获取日交易参数
        try:
            print("\n--- GetDayTradeParam 获取日交易参数 (豆粕 m) ---")
            req = DayTradeParamRequest(
                variety_id="m",
                trade_type="1",
                lang="zh"
            )
            params = self.client.trade.get_day_trade_param(req)
            print(f"日交易参数数量: {len(params)}")
            for i, p in enumerate(params):
                if i >= 3:
                    print("  ... 还有更多合约")
                    break
                print(f"  合约: {p.contract_id} | 投机保证金率: {p.spec_buy_rate:.2%} | "
                      f"涨停: {p.rise_limit:.0f} | 跌停: {p.fall_limit:.0f}")
        except Exception as e:
            print(f"错误: {e}")

        # 获取合约信息
        try:
            print("\n--- GetContractInfo 获取合约信息 (玉米 c) ---")
            req = ContractInfoRequest(
                variety_id="c",
                trade_type="1",
                lang="zh"
            )
            contracts = self.client.trade.get_contract_info(req)
            print(f"合约数量: {len(contracts)}")
            for i, c in enumerate(contracts):
                if i >= 3:
                    print("  ... 还有更多合约")
                    break
                print(f"  合约: {c.contract_id} | 品种: {c.variety} | "
                      f"交易单位: {c.unit} | 最后交易日: {c.end_trade_date}")
        except Exception as e:
            print(f"错误: {e}")

        # 获取套利合约
        try:
            print("\n--- GetArbitrageContract 获取套利合约 ---")
            contracts = self.client.trade.get_arbitrage_contract("zh")
            print(f"套利合约数量: {len(contracts)}")
            for i, a in enumerate(contracts):
                if i >= 3:
                    print("  ... 还有更多套利合约")
                    break
                print(f"  {a.arbi_name} | {a.variety_name} | "
                      f"{a.arbi_contract_id} | 最大手数: {a.max_hand}")
        except Exception as e:
            print(f"错误: {e}")

    def run_settle_examples(self):
        """运行结算服务示例."""
        print("\n" + "=" * 60)
        print("SettleService 结算服务示例")
        print("=" * 60)

        try:
            print("\n--- GetSettleParam 获取结算参数 (豆粕 m) ---")
            req = SettleParamRequest(
                variety_id="m",
                trade_date="20251230",
                trade_type="1",
                lang="zh"
            )
            params = self.client.settle.get_settle_param(req)
            print(f"结算参数数量: {len(params)}")
            for i, s in enumerate(params):
                if i >= 3:
                    print("  ... 还有更多合约")
                    break
                print(f"  合约: {s.contract_id} | 结算价: {s.clear_price} | "
                      f"投机买保证金率: {s.spec_buy_rate} | 开仓手续费: {s.open_fee}")
        except Exception as e:
            print(f"错误: {e}")

    def run_member_examples(self):
        """运行会员服务示例."""
        print("\n" + "=" * 60)
        print("MemberService 会员服务示例")
        print("=" * 60)

        try:
            print("\n--- GetDailyRanking 获取日成交持仓排名 (豆一 a) ---")
            req = DailyRankingRequest(
                variety_id="a",
                contract_id="a2505",
                trade_date="20251230",
                trade_type="1"
            )
            ranking = self.client.member.get_daily_ranking(req)
            
            # 成交量排名
            if ranking.qty_future_list:
                print("成交量排名 (前3):")
                for i, r in enumerate(ranking.qty_future_list):
                    if i >= 3:
                        break
                    print(f"  {r.rank}. {r.qty_abbr} | 成交量: {r.today_qty} | "
                          f"增减: {r.qty_sub:+d}")
            
            # 持买排名
            if ranking.buy_future_list:
                print("持买排名 (前3):")
                for i, r in enumerate(ranking.buy_future_list):
                    if i >= 3:
                        break
                    print(f"  {r.rank}. {r.buy_abbr} | 持买量: {r.today_buy_qty} | "
                          f"增减: {r.buy_sub:+d}")
        except Exception as e:
            print(f"错误: {e}")

        try:
            print("\n--- GetPhaseRanking 获取阶段成交排名 (豆一 a) ---")
            req = PhaseRankingRequest(
                variety="a",
                start_month="202512",
                end_month="202512",
                trade_type="1"
            )
            rankings = self.client.member.get_phase_ranking(req)
            print(f"阶段排名数量: {len(rankings)}")
            for i, r in enumerate(rankings):
                if i >= 3:
                    print("  ... 还有更多")
                    break
                print(f"  {r.seq}. {r.member_name} | 月成交量: {r.month_qty:.0f} | "
                      f"占比: {r.qty_ratio:.2f}%")
        except Exception as e:
            print(f"错误: {e}")

    def run_delivery_examples(self):
        """运行交割服务示例."""
        print("\n" + "=" * 60)
        print("DeliveryService 交割服务示例")
        print("=" * 60)

        print("\n注意: 交割服务的部分接口可能需要特定权限或参数格式")

        try:
            print("\n--- GetDeliveryData 获取交割数据 (豆一 a) ---")
            print("  (交割数据接口可能需要特定权限)")
            req = DeliveryDataRequest(
                variety_code="a",
                trade_date="20251230"
            )
            data = self.client.delivery.get_delivery_data(req)
            print(f"  交割数据数量: {len(data)}")
            for i, d in enumerate(data):
                if i >= 3:
                    print("    ... 还有更多")
                    break
                print(f"    品种: {d.variety_code} | 交割月: {d.delivery_month} | "
                      f"交割量: {d.delivery_volume}")
        except Exception as e:
            print(f"  错误: {e}")

        try:
            print("\n--- GetWarehouseReceipt 获取仓单数据 (豆一 a) ---")
            print("  (仓单数据接口可能需要特定权限)")
            req = WarehouseReceiptRequest(
                variety_code="a",
                trade_date="20251230"
            )
            receipts = self.client.delivery.get_warehouse_receipt(req)
            print(f"  仓单数据数量: {len(receipts)}")
            for i, r in enumerate(receipts):
                if i >= 3:
                    print("    ... 还有更多")
                    break
                print(f"    品种: {r.variety_code} | 仓库: {r.warehouse_name} | "
                      f"数量: {r.quantity}")
        except Exception as e:
            print(f"  错误: {e}")

        try:
            print("\n--- GetDeliveryCost 获取交割费用 (豆一 a) ---")
            print("  (交割费用接口可能需要特定权限)")
            cost = self.client.delivery.get_delivery_cost("a")
            print(f"    品种: {cost.variety_code} | 交割费: {cost.delivery_fee:.2f} | "
                  f"检验费: {cost.inspection_fee:.2f} | 仓储费: {cost.storage_fee:.2f}")
        except Exception as e:
            print(f"  错误: {e}")

        try:
            print("\n--- GetWarehousePremium 获取仓库升贴水 (玉米 c) ---")
            print("  (仓库升贴水接口可能需要特定权限)")
            premiums = self.client.delivery.get_warehouse_premium("c")
            print(f"  仓库升贴水数量: {len(premiums)}")
            for i, p in enumerate(premiums):
                if i >= 3:
                    print("    ... 还有更多")
                    break
                print(f"    品种: {p.variety_code} | 仓库: {p.warehouse_name} | "
                      f"升贴水: {p.premium:.2f}")
        except Exception as e:
            print(f"  错误: {e}")

    def run_error_handling_examples(self):
        """运行错误处理示例."""
        print("\n" + "=" * 60)
        print("错误处理示例")
        print("=" * 60)

        # 1. 验证错误
        print("\n1. 验证错误示例...")
        try:
            config = Config(api_key="", secret="test")
        except ValidationError as e:
            print(f"   ✓ 捕获验证错误: {e.field} - {e.message}")

        # 2. 无效的 columnId
        print("\n2. 无效参数示例...")
        try:
            req = GetArticleByPageRequest(
                column_id="999",  # 无效的 columnId
                page_no=1,
                page_size=10
            )
            self.client.news.get_article_by_page(req)
        except ValidationError as e:
            print(f"   ✓ 捕获验证错误: {e.message}")

    def run_all(self):
        """运行所有示例."""
        print("\nDCE API Python SDK - 完整功能演示")
        print("=" * 60)
        
        self.run_common_examples()
        self.run_news_examples()
        self.run_market_examples()
        self.run_trade_examples()
        self.run_settle_examples()
        self.run_member_examples()
        self.run_delivery_examples()
        self.run_error_handling_examples()
        
        print("\n" + "=" * 60)
        print("演示完成！")
        print("=" * 60)


def main():
    """主函数."""
    demo = DCEAPIDemo()
    demo.run_all()


if __name__ == "__main__":
    main()
