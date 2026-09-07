import uuid

from django.conf import settings
from django.db import models


# ==========================================================
# Choices
# ==========================================================

class AssetType(models.TextChoices):
    CRYPTO = "crypto", "Crypto"
    STOCK = "stock", "Stock"
    FOREX = "forex", "Forex"
    COMMODITY = "commodity", "Commodity"
    INDEX = "index", "Index"


class OrderSide(models.TextChoices):
    BUY = "buy", "Buy"
    SELL = "sell", "Sell"


class OrderType(models.TextChoices):
    MARKET = "market", "Market"
    LIMIT = "limit", "Limit"
    STOP = "stop", "Stop"


class OrderStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    OPEN = "open", "Open"
    FILLED = "filled", "Filled"
    CANCELLED = "cancelled", "Cancelled"


class TransactionType(models.TextChoices):
    DEPOSIT = "deposit", "Deposit"
    WITHDRAW = "withdraw", "Withdraw"
    BUY = "buy", "Buy"
    SELL = "sell", "Sell"
    FEE = "fee", "Fee"
    TRANSFER = "transfer", "Transfer"


class CandleInterval(models.TextChoices):
    M1 = "1m", "1 Minute"
    M5 = "5m", "5 Minute"
    M15 = "15m", "15 Minute"
    H1 = "1h", "1 Hour"
    H4 = "4h", "4 Hour"
    D1 = "1d", "1 Day"


# ==========================================================
# Exchange
# ==========================================================

class Exchange(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=100, unique=True)

    slug = models.SlugField(unique=True)

    website = models.URLField(blank=True)

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    

    def __str__(self):
        return self.name


# ==========================================================
# Asset
# ==========================================================

class Asset(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    symbol = models.CharField(max_length=20, unique=True)

    name = models.CharField(max_length=100)

    asset_type = models.CharField(
        max_length=20,
        choices=AssetType.choices,
        default=AssetType.CRYPTO,
    )

    precision = models.PositiveSmallIntegerField(default=8)

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.symbol


# ==========================================================
# Trading Pair
# ==========================================================

class TradingPair(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    exchange = models.ForeignKey(
        Exchange,
        on_delete=models.CASCADE,
        related_name="pairs",
    )

    base_asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="base_pairs",
    )

    quote_asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="quote_pairs",
    )

    symbol = models.CharField(max_length=30)

    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("exchange", "symbol")

    

    def __str__(self):
        return self.symbol


# ==========================================================
# Wallet
# ==========================================================

class Wallet(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wallets",
    )

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
    )

    balance = models.DecimalField(
        max_digits=30,
        decimal_places=10,
        default=0,
    )

    locked = models.DecimalField(
        max_digits=30,
        decimal_places=10,
        default=0,
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "asset")

    
    def __str__(self):
        return f"{self.user} - {self.asset}"


# ==========================================================
# Portfolio
# ==========================================================

class Portfolio(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="portfolio",
    )

    total_balance = models.DecimalField(
        max_digits=30,
        decimal_places=10,
        default=0,
    )

    total_pnl = models.DecimalField(
        max_digits=30,
        decimal_places=10,
        default=0,
    )

    updated_at = models.DateTimeField(auto_now=True)


# ==========================================================
# Position
# ==========================================================

class Position(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    pair = models.ForeignKey(
        TradingPair,
        on_delete=models.CASCADE,
    )

    quantity = models.DecimalField(
        max_digits=30,
        decimal_places=10,
    )

    average_price = models.DecimalField(
        max_digits=30,
        decimal_places=10,
    )

    opened_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user} - {self.pair}"


# ==========================================================
# Fee Schedule
# ==========================================================

class FeeSchedule(models.Model):

    exchange = models.ForeignKey(
        Exchange,
        on_delete=models.CASCADE,
    )

    maker_fee = models.DecimalField(
        max_digits=8,
        decimal_places=5,
    )

    taker_fee = models.DecimalField(
        max_digits=8,
        decimal_places=5,
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.exchange.name





# ==========================================================
# Order
# ==========================================================

class Order(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
    )

    pair = models.ForeignKey(
        TradingPair,
        on_delete=models.CASCADE,
    )

    side = models.CharField(
        max_length=10,
        choices=OrderSide.choices,
    )

    order_type = models.CharField(
        max_length=10,
        choices=OrderType.choices,
    )

    quantity = models.DecimalField(
        max_digits=30,
        decimal_places=10,
    )

    price = models.DecimalField(
        max_digits=30,
        decimal_places=10,
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return str(self.id)


# ==========================================================
# Trade
# ==========================================================

class Trade(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="trades",
    )

    pair = models.ForeignKey(
        TradingPair,
        on_delete=models.CASCADE,
    )

    quantity = models.DecimalField(
        max_digits=30,
        decimal_places=10,
    )

    price = models.DecimalField(
        max_digits=30,
        decimal_places=10,
    )

    fee = models.DecimalField(
        max_digits=20,
        decimal_places=10,
        default=0,
    )

    executed_at = models.DateTimeField(auto_now_add=True)

  

    def __str__(self):
        return str(self.id)


# ==========================================================
# Transaction
# ==========================================================

class Transaction(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transactions",
    )

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TransactionType.choices,
    )

    amount = models.DecimalField(
        max_digits=30,
        decimal_places=10,
    )

    reference = models.CharField(
        max_length=150,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

   

    def __str__(self):
        return f"{self.user} - {self.transaction_type}"


# ==========================================================
# Candle (OHLCV)
# ==========================================================

class Candle(models.Model):

    pair = models.ForeignKey(
        TradingPair,
        on_delete=models.CASCADE,
        related_name="candles",
    )

    interval = models.CharField(
        max_length=5,
        choices=CandleInterval.choices,
    )

    open = models.DecimalField(max_digits=30, decimal_places=10)
    high = models.DecimalField(max_digits=30, decimal_places=10)
    low = models.DecimalField(max_digits=30, decimal_places=10)
    close = models.DecimalField(max_digits=30, decimal_places=10)

    volume = models.DecimalField(
        max_digits=30,
        decimal_places=10,
    )

    timestamp = models.DateTimeField()

    class Meta:
        unique_together = ("pair", "interval", "timestamp")



    def __str__(self):
        return f"{self.pair} {self.interval}"


# ==========================================================
# Order Book Snapshot
# ==========================================================

class OrderBookSnapshot(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    pair = models.ForeignKey(
        TradingPair,
        on_delete=models.CASCADE,
        related_name="orderbooks",
    )

    created_at = models.DateTimeField(auto_now_add=True)

  
# ==========================================================
# Order Book Level
# ==========================================================

class OrderBookLevel(models.Model):

    snapshot = models.ForeignKey(
        OrderBookSnapshot,
        on_delete=models.CASCADE,
        related_name="levels",
    )

    side = models.CharField(max_length=4)      # bid / ask

    price = models.DecimalField(
        max_digits=30,
        decimal_places=10,
    )

    quantity = models.DecimalField(
        max_digits=30,
        decimal_places=10,
    )

  

# ==========================================================
# Watchlist
# ==========================================================

class Watchlist(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="watchlist",
    )

    pair = models.ForeignKey(
        TradingPair,
        on_delete=models.CASCADE,
    )

    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "pair")


# ==========================================================
# Alert
# ==========================================================

class Alert(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    pair = models.ForeignKey(
        TradingPair,
        on_delete=models.CASCADE,
    )

    target_price = models.DecimalField(
        max_digits=30,
        decimal_places=10,
    )

    triggered = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

  

# ==========================================================
# Indicator Snapshot
# ==========================================================

class IndicatorSnapshot(models.Model):

    pair = models.ForeignKey(
        TradingPair,
        on_delete=models.CASCADE,
    )

    interval = models.CharField(
        max_length=5,
        choices=CandleInterval.choices,
    )

    rsi = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True,
    )

    ema_20 = models.DecimalField(
        max_digits=30,
        decimal_places=10,
        null=True,
        blank=True,
    )

    ema_50 = models.DecimalField(
        max_digits=30,
        decimal_places=10,
        null=True,
        blank=True,
    )

    macd = models.DecimalField(
        max_digits=20,
        decimal_places=10,
        null=True,
        blank=True,
    )

    signal = models.DecimalField(
        max_digits=20,
        decimal_places=10,
        null=True,
        blank=True,
    )

    updated_at = models.DateTimeField(auto_now=True)

   