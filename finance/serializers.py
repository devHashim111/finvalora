# finance/serializers.py

from rest_framework import serializers

from .models import (
    Exchange,
    Asset,
    TradingPair,
    Wallet,
    Portfolio,
    Position,
    Order,
    Trade,
    Transaction,
    Candle,
    OrderBookSnapshot,
    Watchlist,
    Alert,
    IndicatorSnapshot,
    FeeSchedule,
)


# ==========================================================
# EXCHANGE
# ==========================================================

class ExchangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exchange
        fields = "__all__"


# ==========================================================
# ASSET
# ==========================================================

class AssetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Asset
        fields = "__all__"


# ==========================================================
# TRADING PAIR
# ==========================================================

class TradingPairSerializer(serializers.ModelSerializer):

    class Meta:
        model = TradingPair
        fields = "__all__"


# ==========================================================
# WALLET
# ==========================================================

class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = "__all__"

        read_only_fields = [
            "id",
            "user",
            "created_at",
            "updated_at",
        ]


# ==========================================================
# PORTFOLIO
# ==========================================================

class PortfolioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Portfolio
        fields = "__all__"

        read_only_fields = [
            "id",
            "user",
            "created_at",
            "updated_at",
        ]


# ==========================================================
# POSITION
# ==========================================================

class PositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Position
        fields = "__all__"

        read_only_fields = [
            "id",
            "user",
            "created_at",
            "updated_at",
        ]


# ==========================================================
# ORDER
# ==========================================================

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"

        read_only_fields = [
            "id",
            "user",
            "status",
            "filled_quantity",
            "average_price",
            "created_at",
            "updated_at",
        ]


# ==========================================================
# TRADE
# ==========================================================

class TradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trade
        fields = "__all__"

        read_only_fields = [
            "id",
            "user",
            "created_at",
        ]


# ==========================================================
# TRANSACTION
# ==========================================================

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = "__all__"

        read_only_fields = [
            "id",
            "user",
            "created_at",
        ]


# ==========================================================
# CANDLE / OHLCV
# ==========================================================

class CandleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Candle
        fields = "__all__"

        read_only_fields = [
            "id",
        ]


# ==========================================================
# ORDER BOOK
# ==========================================================

class OrderBookSnapshotSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderBookSnapshot
        fields = "__all__"

        read_only_fields = [
            "id",
        ]


# ==========================================================
# WATCHLIST
# ==========================================================

class WatchlistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Watchlist
        fields = "__all__"

        read_only_fields = [
            "id",
            "user",
            "created_at",
        ]


# ==========================================================
# ALERT
# ==========================================================

class AlertSerializer(serializers.ModelSerializer):

    class Meta:
        model = Alert
        fields = "__all__"

        read_only_fields = [
            "id",
            "user",
            "created_at",
            "updated_at",
        ]


# ==========================================================
# INDICATOR SNAPSHOT
# ==========================================================

class IndicatorSnapshotSerializer(serializers.ModelSerializer):

    class Meta:
        model = IndicatorSnapshot
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
        ]


# ==========================================================
# FEE SCHEDULE
# ==========================================================

class FeeScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeeSchedule
        fields = "__all__"