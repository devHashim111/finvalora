from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

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

from .serializers import (
    ExchangeSerializer,
    AssetSerializer,
    TradingPairSerializer,
    WalletSerializer,
    PortfolioSerializer,
    PositionSerializer,
    OrderSerializer,
    TradeSerializer,
    TransactionSerializer,
    CandleSerializer,
    OrderBookSnapshotSerializer,
    WatchlistSerializer,
    AlertSerializer,
    IndicatorSnapshotSerializer,
    FeeScheduleSerializer,
)


# ==========================================================
# EXCHANGE
# ==========================================================

class ExchangeViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializer
    permission_classes = [IsAuthenticated]


# ==========================================================
# ASSET
# ==========================================================

class AssetViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated]


# ==========================================================
# TRADING PAIR
# ==========================================================

class TradingPairViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = TradingPair.objects.all()
    serializer_class = TradingPairSerializer
    permission_classes = [IsAuthenticated]


# ==========================================================
# WALLET
# ==========================================================

class WalletViewSet(viewsets.ModelViewSet):

    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Wallet.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )


# ==========================================================
# PORTFOLIO
# ==========================================================

class PortfolioViewSet(viewsets.ModelViewSet):

    serializer_class = PortfolioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Portfolio.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )


# ==========================================================
# POSITION
# ==========================================================

class PositionViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Position.objects.filter(
            user=self.request.user
        )


# ==========================================================
# ORDER
# ==========================================================

class OrderViewSet(viewsets.ModelViewSet):

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Order.objects.filter(
            user=self.request.user
        ).order_by("-created_at")

    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )


# ==========================================================
# TRADE
# ==========================================================

class TradeViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = TradeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Trade.objects.filter(
            order__user=self.request.user
        ).order_by("-executed_at")

# ==========================================================
# TRANSACTION
# ==========================================================

class TransactionViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Transaction.objects.filter(
            user=self.request.user
        ).order_by("-created_at")


# ==========================================================
# CANDLES
# ==========================================================

class CandleViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Candle.objects.all()
    serializer_class = CandleSerializer
    permission_classes = [IsAuthenticated]


# ==========================================================
# ORDER BOOK
# ==========================================================

class OrderBookSnapshotViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = OrderBookSnapshot.objects.all()
    serializer_class = OrderBookSnapshotSerializer
    permission_classes = [IsAuthenticated]


# ==========================================================
# WATCHLIST
# ==========================================================

class WatchlistViewSet(viewsets.ModelViewSet):

    serializer_class = WatchlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Watchlist.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )


# ==========================================================
# ALERT
# ==========================================================

class AlertViewSet(viewsets.ModelViewSet):

    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Alert.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )


# ==========================================================
# INDICATORS
# ==========================================================

class IndicatorSnapshotViewSet(
    viewsets.ReadOnlyModelViewSet
):

    queryset = IndicatorSnapshot.objects.all()
    serializer_class = IndicatorSnapshotSerializer
    permission_classes = [IsAuthenticated]


# ==========================================================
# FEE SCHEDULE
# ==========================================================

class FeeScheduleViewSet(
    viewsets.ReadOnlyModelViewSet
):

    queryset = FeeSchedule.objects.all()
    serializer_class = FeeScheduleSerializer
    permission_classes = [IsAuthenticated]