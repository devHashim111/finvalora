# analytics/serializers.py

from rest_framework import serializers

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


# ==========================================================
# DAILY PORTFOLIO SNAPSHOT
# ==========================================================

class DailyPortfolioSnapshotSerializer(serializers.ModelSerializer):

    class Meta:
        model = DailyPortfolioSnapshot
        fields = "__all__"

        read_only_fields = [
            "id",
            "user",
            "created_at",
        ]


# ==========================================================
# TRADE STATISTICS
# ==========================================================

class TradeStatisticsSerializer(serializers.ModelSerializer):

    class Meta:
        model = TradeStatistics
        fields = "__all__"

        read_only_fields = [
            "user",
            "updated_at",
        ]


# ==========================================================
# PERFORMANCE METRICS
# ==========================================================

class PerformanceMetricsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PerformanceMetrics
        fields = "__all__"

        read_only_fields = [
            "user",
            "updated_at",
        ]


# ==========================================================
# MARKET STATISTICS
# ==========================================================

class MarketStatisticsSerializer(serializers.ModelSerializer):

    class Meta:
        model = MarketStatistics
        fields = "__all__"

        read_only_fields = [
            "id",
            "updated_at",
        ]


# ==========================================================
# INDICATOR HISTORY
# ==========================================================

class IndicatorHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = IndicatorHistory
        fields = "__all__"

        read_only_fields = [
            "id",
        ]


# ==========================================================
# STRATEGY PERFORMANCE
# ==========================================================

class StrategyPerformanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = StrategyPerformance
        fields = "__all__"

        read_only_fields = [
            "id",
            "user",
            "updated_at",
        ]


# ==========================================================
# EQUITY CURVE
# ==========================================================

class EquityCurveSerializer(serializers.ModelSerializer):

    class Meta:
        model = EquityCurve
        fields = "__all__"

        read_only_fields = [
            "id",
            "user",
        ]


# ==========================================================
# DRAWDOWN HISTORY
# ==========================================================

class DrawdownHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = DrawdownHistory
        fields = "__all__"

        read_only_fields = [
            "id",
            "user",
        ]