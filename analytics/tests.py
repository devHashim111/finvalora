from datetime import date, datetime
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from user.models import CustomUser
from finance.models import Exchange, Asset, TradingPair

from .models import (
    DailyPortfolioSnapshot,
    TradeStatistics,
    PerformanceMetrics,
    MarketStatistics,
    IndicatorHistory,
    StrategyPerformance,
    EquityCurve,
    DrawdownHistory,
)


class AnalyticsTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="trader",
            email="trader@example.com",
            password="TestPassword123"
        )

        self.exchange = Exchange.objects.create(
            name="Binance",
            slug="binance",
            website="https://binance.com",
            active=True
        )

        self.btc = Asset.objects.create(
            symbol="BTC",
            name="Bitcoin",
            asset_type="crypto",
            precision=8,
            active=True
        )

        self.usdt = Asset.objects.create(
            symbol="USDT",
            name="Tether",
            asset_type="crypto",
            precision=8,
            active=True
        )

        self.pair = TradingPair.objects.create(
            exchange=self.exchange,
            base_asset=self.btc,
            quote_asset=self.usdt,
            symbol="BTCUSDT",
            active=True
        )

        self.timestamp = timezone.now()

    def test_daily_portfolio_snapshot(self):
        snapshot = DailyPortfolioSnapshot.objects.create(
            user=self.user,
            total_balance=Decimal("10000.00"),
            total_pnl=Decimal("500.00"),
            total_assets=2,
            snapshot_date=date.today()
        )

        self.assertEqual(snapshot.user, self.user)
        self.assertEqual(snapshot.total_balance, Decimal("10000.00"))
        self.assertEqual(snapshot.total_pnl, Decimal("500.00"))
        self.assertEqual(snapshot.total_assets, 2)

    def test_trade_statistics(self):
        statistics = TradeStatistics.objects.create(
            user=self.user,
            total_trades=100,
            winning_trades=65,
            losing_trades=35,
            total_profit=Decimal("1500.00"),
            total_loss=Decimal("500.00")
        )

        self.assertEqual(statistics.user, self.user)
        self.assertEqual(statistics.total_trades, 100)
        self.assertEqual(statistics.winning_trades, 65)
        self.assertEqual(statistics.losing_trades, 35)
        self.assertEqual(statistics.total_profit, Decimal("1500.00"))
        self.assertEqual(statistics.total_loss, Decimal("500.00"))

    def test_performance_metrics(self):
        metrics = PerformanceMetrics.objects.create(
            user=self.user,
            sharpe_ratio=Decimal("1.5000"),
            sortino_ratio=Decimal("2.0000"),
            max_drawdown=Decimal("5.0000"),
            volatility=Decimal("3.5000")
        )

        self.assertEqual(metrics.user, self.user)
        self.assertEqual(metrics.sharpe_ratio, Decimal("1.5000"))
        self.assertEqual(metrics.sortino_ratio, Decimal("2.0000"))
        self.assertEqual(metrics.max_drawdown, Decimal("5.0000"))
        self.assertEqual(metrics.volatility, Decimal("3.5000"))

    def test_market_statistics(self):
        statistics = MarketStatistics.objects.create(
            pair=self.pair,
            volume_24h=Decimal("1000000.00"),
            high_24h=Decimal("65000.00"),
            low_24h=Decimal("58000.00"),
            change_24h=Decimal("4.2500")
        )

        self.assertEqual(statistics.pair, self.pair)
        self.assertEqual(statistics.volume_24h, Decimal("1000000.00"))
        self.assertEqual(statistics.high_24h, Decimal("65000.00"))
        self.assertEqual(statistics.low_24h, Decimal("58000.00"))
        self.assertEqual(statistics.change_24h, Decimal("4.2500"))

    def test_indicator_history(self):
        indicator = IndicatorHistory.objects.create(
            pair=self.pair,
            indicator="RSI",
            value=Decimal("55.0000000000"),
            interval="15m",
            timestamp=self.timestamp
        )

        self.assertEqual(indicator.pair, self.pair)
        self.assertEqual(indicator.indicator, "RSI")
        self.assertEqual(indicator.value, Decimal("55.0000000000"))
        self.assertEqual(indicator.interval, "15m")
        self.assertEqual(indicator.timestamp, self.timestamp)

    def test_strategy_performance(self):
        strategy = StrategyPerformance.objects.create(
            user=self.user,
            strategy_name="Moving Average",
            total_trades=50,
            net_profit=Decimal("750.00"),
            win_rate=Decimal("65.0000")
        )

        self.assertEqual(strategy.user, self.user)
        self.assertEqual(strategy.strategy_name, "Moving Average")
        self.assertEqual(strategy.total_trades, 50)
        self.assertEqual(strategy.net_profit, Decimal("750.00"))
        self.assertEqual(strategy.win_rate, Decimal("65.0000"))

    def test_equity_curve(self):
        equity = EquityCurve.objects.create(
            user=self.user,
            equity=Decimal("10750.00"),
            timestamp=self.timestamp
        )

        self.assertEqual(equity.user, self.user)
        self.assertEqual(equity.equity, Decimal("10750.00"))
        self.assertEqual(equity.timestamp, self.timestamp)

    def test_drawdown_history(self):
        drawdown = DrawdownHistory.objects.create(
            user=self.user,
            drawdown=Decimal("5.0000"),
            peak_value=Decimal("12000.00"),
            current_value=Decimal("11400.00"),
            timestamp=self.timestamp
        )

        self.assertEqual(drawdown.user, self.user)
        self.assertEqual(drawdown.drawdown, Decimal("5.0000"))
        self.assertEqual(drawdown.peak_value, Decimal("12000.00"))
        self.assertEqual(drawdown.current_value, Decimal("11400.00"))
        self.assertEqual(drawdown.timestamp, self.timestamp)