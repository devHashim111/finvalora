from django.contrib import admin

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
# Daily Portfolio Snapshot
# ==========================================================

@admin.register(DailyPortfolioSnapshot)
class DailyPortfolioSnapshotAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "snapshot_date",
        "total_balance",
        "total_pnl",
        "total_assets",
        "created_at",
    )

    list_filter = (
        "snapshot_date",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    readonly_fields = (
        "id",
        "created_at",
    )

    ordering = (
        "-snapshot_date",
        "-created_at",
    )

    date_hierarchy = "snapshot_date"

    list_select_related = (
        "user",
    )


# ==========================================================
# Trade Statistics
# ==========================================================

@admin.register(TradeStatistics)
class TradeStatisticsAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "total_trades",
        "winning_trades",
        "losing_trades",
        "total_profit",
        "total_loss",
        "updated_at",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    readonly_fields = (
        "updated_at",
    )

    ordering = (
        "-updated_at",
    )

    list_select_related = (
        "user",
    )


# ==========================================================
# Performance Metrics
# ==========================================================

@admin.register(PerformanceMetrics)
class PerformanceMetricsAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "sharpe_ratio",
        "sortino_ratio",
        "max_drawdown",
        "volatility",
        "updated_at",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    readonly_fields = (
        "updated_at",
    )

    ordering = (
        "-updated_at",
    )

    list_select_related = (
        "user",
    )


# ==========================================================
# Market Statistics
# ==========================================================

@admin.register(MarketStatistics)
class MarketStatisticsAdmin(admin.ModelAdmin):

    list_display = (
        "pair",
        "volume_24h",
        "high_24h",
        "low_24h",
        "change_24h",
        "updated_at",
    )

    list_filter = (
        "pair__exchange",
        "updated_at",
    )

    search_fields = (
        "pair__symbol",
        "pair__base_asset__symbol",
        "pair__base_asset__name",
        "pair__quote_asset__symbol",
        "pair__quote_asset__name",
        "pair__exchange__name",
    )

    readonly_fields = (
        "updated_at",
    )

    ordering = (
        "-updated_at",
    )

    list_select_related = (
        "pair",
        "pair__exchange",
        "pair__base_asset",
        "pair__quote_asset",
    )


# ==========================================================
# Indicator History
# ==========================================================

@admin.register(IndicatorHistory)
class IndicatorHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "pair",
        "indicator",
        "value",
        "interval",
        "timestamp",
    )

    list_filter = (
        "indicator",
        "interval",
        "pair__exchange",
        "timestamp",
    )

    search_fields = (
        "indicator",
        "pair__symbol",
        "pair__base_asset__symbol",
        "pair__quote_asset__symbol",
        "pair__exchange__name",
    )

    ordering = (
        "-timestamp",
    )

    list_select_related = (
        "pair",
        "pair__exchange",
        "pair__base_asset",
        "pair__quote_asset",
    )

    date_hierarchy = "timestamp"


# ==========================================================
# Strategy Performance
# ==========================================================

@admin.register(StrategyPerformance)
class StrategyPerformanceAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "strategy_name",
        "total_trades",
        "net_profit",
        "win_rate",
        "updated_at",
    )

    list_filter = (
        "strategy_name",
        "updated_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "strategy_name",
    )

    readonly_fields = (
        "updated_at",
    )

    ordering = (
        "-updated_at",
    )

    list_select_related = (
        "user",
    )


# ==========================================================
# Equity Curve
# ==========================================================

@admin.register(EquityCurve)
class EquityCurveAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "equity",
        "timestamp",
    )

    list_filter = (
        "timestamp",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    ordering = (
        "-timestamp",
    )

    list_select_related = (
        "user",
    )

    date_hierarchy = "timestamp"


# ==========================================================
# Drawdown History
# ==========================================================

@admin.register(DrawdownHistory)
class DrawdownHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "drawdown",
        "peak_value",
        "current_value",
        "timestamp",
    )

    list_filter = (
        "timestamp",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    ordering = (
        "-timestamp",
    )

    list_select_related = (
        "user",
    )

    date_hierarchy = "timestamp"