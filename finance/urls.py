from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ExchangeViewSet,
    AssetViewSet,
    TradingPairViewSet,
    WalletViewSet,
    PortfolioViewSet,
    PositionViewSet,
    OrderViewSet,
    TradeViewSet,
    TransactionViewSet,
    CandleViewSet,
    OrderBookSnapshotViewSet,
    WatchlistViewSet,
    AlertViewSet,
    IndicatorSnapshotViewSet,
    FeeScheduleViewSet,
)


router = DefaultRouter()


router.register(
    r"exchanges",
    ExchangeViewSet,
    basename="exchanges",
)

router.register(
    r"assets",
    AssetViewSet,
    basename="assets",
)

router.register(
    r"trading-pairs",
    TradingPairViewSet,
    basename="trading-pairs",
)

router.register(
    r"wallets",
    WalletViewSet,
    basename="wallets",
)

router.register(
    r"portfolios",
    PortfolioViewSet,
    basename="portfolios",
)

router.register(
    r"positions",
    PositionViewSet,
    basename="positions",
)

router.register(
    r"orders",
    OrderViewSet,
    basename="orders",
)

router.register(
    r"trades",
    TradeViewSet,
    basename="trades",
)

router.register(
    r"transactions",
    TransactionViewSet,
    basename="transactions",
)

router.register(
    r"candles",
    CandleViewSet,
    basename="candles",
)

router.register(
    r"order-book",
    OrderBookSnapshotViewSet,
    basename="order-book",
)

router.register(
    r"watchlists",
    WatchlistViewSet,
    basename="watchlists",
)

router.register(
    r"alerts",
    AlertViewSet,
    basename="alerts",
)

router.register(
    r"indicators",
    IndicatorSnapshotViewSet,
    basename="indicators",
)

router.register(
    r"fee-schedules",
    FeeScheduleViewSet,
    basename="fee-schedules",
)


urlpatterns = [
    path("", include(router.urls)),
]