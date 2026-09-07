from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

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

from .serializers import (
    DailyPortfolioSnapshotSerializer,
    TradeStatisticsSerializer,
    PerformanceMetricsSerializer,
    MarketStatisticsSerializer,
    IndicatorHistorySerializer,
    StrategyPerformanceSerializer,
    EquityCurveSerializer,
    DrawdownHistorySerializer,
)
from .tasks import (
    generate_daily_portfolio_snapshot,
    update_trade_statistics,
    update_performance_metrics,
    update_market_statistics,
    update_indicator_history,
    update_strategy_performance,
    generate_equity_curve,
    generate_drawdown_history,
)


# ==========================================================
# DAILY PORTFOLIO SNAPSHOT
# ==========================================================

class DailyPortfolioSnapshotViewSet(
    viewsets.ReadOnlyModelViewSet
):

    serializer_class = DailyPortfolioSnapshotSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return DailyPortfolioSnapshot.objects.filter(
            user=self.request.user
        ).order_by("-snapshot_date")

    def list(self, request, *args, **kwargs):

        generate_daily_portfolio_snapshot.delay(
            str(request.user.id)
        )

        return super().list(
            request,
            *args,
            **kwargs
        )

# ==========================================================
# TRADE STATISTICS
# ==========================================================

class TradeStatisticsViewSet(
    viewsets.ReadOnlyModelViewSet
):

    serializer_class = TradeStatisticsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return TradeStatistics.objects.filter(
            user=self.request.user
        )


# ==========================================================
# PERFORMANCE METRICS
# ==========================================================

class PerformanceMetricsViewSet(
    viewsets.ReadOnlyModelViewSet
):

    serializer_class = PerformanceMetricsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return PerformanceMetrics.objects.filter(
            user=self.request.user
        )


# ==========================================================
# MARKET STATISTICS
# ==========================================================

class MarketStatisticsViewSet(
    viewsets.ReadOnlyModelViewSet
):

    queryset = MarketStatistics.objects.all()
    serializer_class = MarketStatisticsSerializer
    permission_classes = [IsAuthenticated]


# ==========================================================
# INDICATOR HISTORY
# ==========================================================

class IndicatorHistoryViewSet(
    viewsets.ReadOnlyModelViewSet
):

    queryset = IndicatorHistory.objects.all()
    serializer_class = IndicatorHistorySerializer
    permission_classes = [IsAuthenticated]


# ==========================================================
# STRATEGY PERFORMANCE
# ==========================================================

class StrategyPerformanceViewSet(
    viewsets.ReadOnlyModelViewSet
):

    serializer_class = StrategyPerformanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return StrategyPerformance.objects.filter(
            user=self.request.user
        ).order_by("-updated_at")


# ==========================================================
# EQUITY CURVE
# ==========================================================

class EquityCurveViewSet(
    viewsets.ReadOnlyModelViewSet
):

    serializer_class = EquityCurveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return EquityCurve.objects.filter(
            user=self.request.user
        ).order_by("timestamp")


# ==========================================================
# DRAWDOWN HISTORY
# ==========================================================

class DrawdownHistoryViewSet(
    viewsets.ReadOnlyModelViewSet
):

    serializer_class = DrawdownHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return DrawdownHistory.objects.filter(
            user=self.request.user
        ).order_by("timestamp")