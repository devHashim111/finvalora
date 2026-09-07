from django.contrib import admin

from .models import (
    Exchange,
    Asset,
    TradingPair,
    Wallet,
    Portfolio,
    Position,
    FeeSchedule,
    Order,
    Trade,
    Transaction,
    Candle,
    OrderBookSnapshot,
    OrderBookLevel,
    Watchlist,
    Alert,
    IndicatorSnapshot,
)


# ==========================================================
# Exchange
# ==========================================================

@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "slug",
        "active",
        "website",
        "created_at",
    )

    list_filter = (
        "active",
        "created_at",
    )

    search_fields = (
        "name",
        "slug",
    )

    readonly_fields = (
        "id",
        "created_at",
    )

    ordering = (
        "name",
    )


# ==========================================================
# Asset
# ==========================================================

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):

    list_display = (
        "symbol",
        "name",
        "asset_type",
        "precision",
        "active",
        "created_at",
    )

    list_filter = (
        "asset_type",
        "active",
        "created_at",
    )

    search_fields = (
        "symbol",
        "name",
    )

    readonly_fields = (
        "id",
        "created_at",
    )

    ordering = (
        "symbol",
    )


# ==========================================================
# Trading Pair
# ==========================================================

@admin.register(TradingPair)
class TradingPairAdmin(admin.ModelAdmin):

    list_display = (
        "symbol",
        "exchange",
        "base_asset",
        "quote_asset",
        "active",
    )

    list_filter = (
        "exchange",
        "active",
    )

    search_fields = (
        "symbol",
        "exchange__name",
        "base_asset__symbol",
        "base_asset__name",
        "quote_asset__symbol",
        "quote_asset__name",
    )

    readonly_fields = (
        "id",
    )

    ordering = (
        "symbol",
    )

    list_select_related = (
        "exchange",
        "base_asset",
        "quote_asset",
    )


# ==========================================================
# Wallet
# ==========================================================

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "asset",
        "balance",
        "locked",
        "available_balance",
        "updated_at",
    )

    list_filter = (
        "asset",
        "updated_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "asset__symbol",
        "asset__name",
    )

    readonly_fields = (
        "id",
        "updated_at",
        "available_balance",
    )

    ordering = (
        "-updated_at",
    )

    list_select_related = (
        "user",
        "asset",
    )

    @admin.display(description="Available")
    def available_balance(self, obj):
        return obj.balance - obj.locked


# ==========================================================
# Portfolio
# ==========================================================

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "total_balance",
        "total_pnl",
        "updated_at",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    readonly_fields = (
        "id",
        "updated_at",
    )

    ordering = (
        "-updated_at",
    )

    list_select_related = (
        "user",
    )


# ==========================================================
# Position
# ==========================================================

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "pair",
        "quantity",
        "average_price",
        "opened_at",
    )

    list_filter = (
        "pair__exchange",
        "opened_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "pair__symbol",
    )

    readonly_fields = (
        "id",
        "opened_at",
    )

    ordering = (
        "-opened_at",
    )

    list_select_related = (
        "user",
        "pair",
    )


# ==========================================================
# Fee Schedule
# ==========================================================

@admin.register(FeeSchedule)
class FeeScheduleAdmin(admin.ModelAdmin):

    list_display = (
        "exchange",
        "maker_fee",
        "taker_fee",
        "updated_at",
    )

    list_filter = (
        "exchange",
        "updated_at",
    )

    search_fields = (
        "exchange__name",
    )

    readonly_fields = (
        "updated_at",
    )

    ordering = (
        "-updated_at",
    )

    list_select_related = (
        "exchange",
    )


# ==========================================================
# Order
# ==========================================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "pair",
        "side",
        "order_type",
        "quantity",
        "price",
        "status",
        "created_at",
    )

    list_filter = (
        "side",
        "order_type",
        "status",
        "pair__exchange",
        "created_at",
    )

    search_fields = (
        "id",
        "user__username",
        "user__email",
        "pair__symbol",
    )

    readonly_fields = (
        "id",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    list_select_related = (
        "user",
        "pair",
    )

    date_hierarchy = "created_at"


# ==========================================================
# Trade
# ==========================================================

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "order",
        "pair",
        "quantity",
        "price",
        "fee",
        "executed_at",
    )

    list_filter = (
        "pair__exchange",
        "executed_at",
    )

    search_fields = (
        "id",
        "order__id",
        "order__user__username",
        "order__user__email",
        "pair__symbol",
    )

    readonly_fields = (
        "id",
        "executed_at",
        "user",
    )

    ordering = (
        "-executed_at",
    )

    list_select_related = (
        "order",
        "order__user",
        "pair",
    )

    date_hierarchy = "executed_at"

    @admin.display(description="User")
    def user(self, obj):
        return obj.order.user


# ==========================================================
# Transaction
# ==========================================================

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "wallet",
        "transaction_type",
        "amount",
        "reference",
        "created_at",
    )

    list_filter = (
        "transaction_type",
        "created_at",
    )

    search_fields = (
        "id",
        "user__username",
        "user__email",
        "wallet__asset__symbol",
        "reference",
    )

    readonly_fields = (
        "id",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    list_select_related = (
        "user",
        "wallet",
        "wallet__asset",
    )

    date_hierarchy = "created_at"


# ==========================================================
# Candle
# ==========================================================

@admin.register(Candle)
class CandleAdmin(admin.ModelAdmin):

    list_display = (
        "pair",
        "interval",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "timestamp",
    )

    list_filter = (
        "interval",
        "pair__exchange",
        "timestamp",
    )

    search_fields = (
        "pair__symbol",
        "pair__base_asset__symbol",
        "pair__quote_asset__symbol",
    )

    ordering = (
        "-timestamp",
    )

    list_select_related = (
        "pair",
    )

    date_hierarchy = "timestamp"


# ==========================================================
# Order Book Snapshot
# ==========================================================

@admin.register(OrderBookSnapshot)
class OrderBookSnapshotAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "pair",
        "created_at",
        "level_count",
    )

    list_filter = (
        "pair__exchange",
        "created_at",
    )

    search_fields = (
        "id",
        "pair__symbol",
    )

    readonly_fields = (
        "id",
        "created_at",
        "level_count",
    )

    ordering = (
        "-created_at",
    )

    list_select_related = (
        "pair",
    )

    date_hierarchy = "created_at"

    @admin.display(description="Levels")
    def level_count(self, obj):
        return obj.levels.count()


# ==========================================================
# Order Book Level
# ==========================================================

@admin.register(OrderBookLevel)
class OrderBookLevelAdmin(admin.ModelAdmin):

    list_display = (
        "snapshot",
        "pair",
        "side",
        "price",
        "quantity",
    )

    list_filter = (
        "side",
        "snapshot__pair__exchange",
    )

    search_fields = (
        "snapshot__pair__symbol",
        "snapshot__id",
    )

    ordering = (
        "price",
    )

    list_select_related = (
        "snapshot",
        "snapshot__pair",
    )

    @admin.display(description="Pair")
    def pair(self, obj):
        return obj.snapshot.pair


# ==========================================================
# Watchlist
# ==========================================================

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "pair",
        "added_at",
    )

    list_filter = (
        "pair__exchange",
        "added_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "pair__symbol",
    )

    readonly_fields = (
        "added_at",
    )

    ordering = (
        "-added_at",
    )

    list_select_related = (
        "user",
        "pair",
    )


# ==========================================================
# Alert
# ==========================================================

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "pair",
        "target_price",
        "triggered",
        "created_at",
    )

    list_filter = (
        "triggered",
        "pair__exchange",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "pair__symbol",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    list_select_related = (
        "user",
        "pair",
    )


# ==========================================================
# Indicator Snapshot
# ==========================================================

@admin.register(IndicatorSnapshot)
class IndicatorSnapshotAdmin(admin.ModelAdmin):

    list_display = (
        "pair",
        "interval",
        "rsi",
        "ema_20",
        "ema_50",
        "macd",
        "signal",
        "updated_at",
    )

    list_filter = (
        "interval",
        "pair__exchange",
        "updated_at",
    )

    search_fields = (
        "pair__symbol",
        "pair__base_asset__symbol",
        "pair__quote_asset__symbol",
    )

    readonly_fields = (
        "updated_at",
    )

    ordering = (
        "-updated_at",
    )

    list_select_related = (
        "pair",
    )