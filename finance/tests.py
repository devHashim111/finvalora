from decimal import Decimal

from django.test import TestCase

from user.models import CustomUser
from .models import (
    Exchange,
    Asset,
    TradingPair,
    Wallet,
    Portfolio,
    Order,
)


class FinanceTest(TestCase):

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

    def test_asset_creation(self):
        self.assertEqual(self.btc.symbol, "BTC")
        self.assertEqual(self.btc.name, "Bitcoin")
        self.assertTrue(self.btc.active)

    def test_trading_pair_relationships(self):
        self.assertEqual(self.pair.exchange, self.exchange)
        self.assertEqual(self.pair.base_asset, self.btc)
        self.assertEqual(self.pair.quote_asset, self.usdt)
        self.assertEqual(self.pair.symbol, "BTCUSDT")

    def test_wallet_balance(self):
        wallet = Wallet.objects.create(
            user=self.user,
            asset=self.usdt,
            balance=Decimal("1000.00"),
            locked=Decimal("250.00")
        )

        self.assertEqual(wallet.balance, Decimal("1000.00"))
        self.assertEqual(wallet.locked, Decimal("250.00"))
        self.assertEqual(
            wallet.balance - wallet.locked,
            Decimal("750.00")
        )

    def test_portfolio_belongs_to_user(self):
        portfolio = Portfolio.objects.create(
            user=self.user,
            total_balance=Decimal("1000.00"),
            total_pnl=Decimal("100.00")
        )

        self.assertEqual(portfolio.user, self.user)
        self.assertEqual(portfolio.total_balance, Decimal("1000.00"))
        self.assertEqual(portfolio.total_pnl, Decimal("100.00"))

    def test_order_creation(self):
        order = Order.objects.create(
            user=self.user,
            pair=self.pair,
            side="buy",
            order_type="limit",
            quantity=Decimal("0.01000000"),
            price=Decimal("60000.00")
        )

        self.assertEqual(order.user, self.user)
        self.assertEqual(order.pair, self.pair)
        self.assertEqual(order.side, "buy")
        self.assertEqual(order.order_type, "limit")
        self.assertEqual(order.quantity, Decimal("0.01000000"))
        self.assertEqual(order.price, Decimal("60000.00"))