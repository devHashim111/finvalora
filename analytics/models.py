import uuid

from django.conf import settings
from django.db import models


# ==========================================================
# Daily Portfolio Snapshot
# Generated daily by Celery
# ==========================================================

class DailyPortfolioSnapshot(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="daily_snapshots",
    )

    total_balance = models.DecimalField(
        max_digits=30,
        decimal_places=10,
    )

    total_pnl = models.DecimalField(
        max_digits=30,
        decimal_places=10,
        default=0,
    )

    total_assets = models.PositiveIntegerField(default=0)

    snapshot_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "snapshot_date")

  
# ==========================================================
# Trade Statistics
# ==========================================================

class TradeStatistics(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="trade_statistics",
    )

    total_trades = models.PositiveIntegerField(default=0)

    winning_trades = models.PositiveIntegerField(default=0)

    losing_trades = models.PositiveIntegerField(default=0)

    total_profit = models.DecimalField(
        max_digits=30,
        decimal_places=10,
        default=0,
    )

    total_loss = models.DecimalField(
        max_digits=30,
        decimal_places=10,
        default=0,
    )

    updated_at = models.DateTimeField(auto_now=True)



# ==========================================================
# Performance Metrics
# ==========================================================

class PerformanceMetrics(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="performance_metrics",
    )

    sharpe_ratio = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=0,
    )

    sortino_ratio = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=0,
    )

    max_drawdown = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=0,
    )

    volatility = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=0,
    )

    updated_at = models.DateTimeField(auto_now=True)

  

# ==========================================================
# Market Statistics
# ==========================================================

class MarketStatistics(models.Model):

    pair = models.ForeignKey(
        "finance.TradingPair",
        on_delete=models.CASCADE,
    )

    volume_24h = models.DecimalField(
        max_digits=30,
        decimal_places=10,
    )

    high_24h = models.DecimalField(
        max_digits=30,
        decimal_places=10,
    )

    low_24h = models.DecimalField(
        max_digits=30,
        decimal_places=10,
    )

    change_24h = models.DecimalField(
        max_digits=10,
        decimal_places=4,
    )

    updated_at = models.DateTimeField(auto_now=True)



# ==========================================================
# Indicator History
# ==========================================================

class IndicatorHistory(models.Model):

    pair = models.ForeignKey(
        "finance.TradingPair",
        on_delete=models.CASCADE,
    )

    indicator = models.CharField(max_length=50)

    value = models.DecimalField(
        max_digits=30,
        decimal_places=10,
    )

    interval = models.CharField(max_length=10)

    timestamp = models.DateTimeField()

 

    def __str__(self):
        return f"{self.pair} - {self.indicator}"


# ==========================================================
# Strategy Performance
# ==========================================================

class StrategyPerformance(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    strategy_name = models.CharField(max_length=100)

    total_trades = models.PositiveIntegerField(default=0)

    net_profit = models.DecimalField(
        max_digits=30,
        decimal_places=10,
        default=0,
    )

    win_rate = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=0,
    )

    updated_at = models.DateTimeField(auto_now=True)

    # TODO:
    # average_trade
    # average_hold_time
    # sharpe_ratio


# ==========================================================
# Equity Curve
# ==========================================================

class EquityCurve(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="equity_curve",
    )

    equity = models.DecimalField(
        max_digits=30,
        decimal_places=10,
    )

    timestamp = models.DateTimeField()

  
    def __str__(self):
        return f"{self.user} - {self.timestamp}"


# ==========================================================
# Drawdown History
# ==========================================================

class DrawdownHistory(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="drawdowns",
    )

    drawdown = models.DecimalField(
        max_digits=10,
        decimal_places=4,
    )

    peak_value = models.DecimalField(
        max_digits=30,
        decimal_places=10,
    )

    current_value = models.DecimalField(
        max_digits=30,
        decimal_places=10,
    )

    timestamp = models.DateTimeField()

  