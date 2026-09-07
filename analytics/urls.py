from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    DailyPortfolioSnapshotViewSet,
    TradeStatisticsViewSet,
    PerformanceMetricsViewSet,
    MarketStatisticsViewSet,
    IndicatorHistoryViewSet,
    StrategyPerformanceViewSet,
    EquityCurveViewSet,
    DrawdownHistoryViewSet,
)


router = DefaultRouter()


router.register(
    r"daily-snapshots",
    DailyPortfolioSnapshotViewSet,
    basename="daily-snapshots",
)

router.register(
    r"trade-statistics",
    TradeStatisticsViewSet,
    basename="trade-statistics",
)

router.register(
    r"performance",
    PerformanceMetricsViewSet,
    basename="performance",
)

router.register(
    r"market-statistics",
    MarketStatisticsViewSet,
    basename="market-statistics",
)

router.register(
    r"indicators",
    IndicatorHistoryViewSet,
    basename="indicators",
)

router.register(
    r"strategies",
    StrategyPerformanceViewSet,
    basename="strategies",
)

router.register(
    r"equity-curve",
    EquityCurveViewSet,
    basename="equity-curve",
)

router.register(
    r"drawdowns",
    DrawdownHistoryViewSet,
    basename="drawdowns",
)


urlpatterns = [
    path("", include(router.urls)),
]