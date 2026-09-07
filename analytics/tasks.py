from celery import shared_task
from django.utils import timezone

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

@shared_task
def generate_daily_portfolio_snapshot(user_id):
    print("task triggered successfully")
    from finance.models import Portfolio

    portfolio = Portfolio.objects.filter(
        user_id=user_id
    ).first()

    if not portfolio:
        return "No portfolio found."

    snapshot, created = DailyPortfolioSnapshot.objects.update_or_create(
        user_id=user_id,
        snapshot_date=timezone.now().date(),
        defaults={
            "total_balance": getattr(
                portfolio,
                "balance",
                0,
            ),
            "total_pnl": getattr(
                portfolio,
                "pnl",
                0,
            ),
            "total_assets": 0,
        },
    )

    return f"Daily snapshot {'created' if created else 'updated'}."
    

# ==========================================================
# TRADE STATISTICS
# ==========================================================

@shared_task
def update_trade_statistics(user_id):

    from finance.models import Trade

    trades = Trade.objects.filter(
        user_id=user_id
    )

    total_trades = trades.count()

    # Keep calculations compatible with your current
    # lean models. Add detailed P/L calculation later
    # when the Trade model has the required fields.

    statistics, _ = TradeStatistics.objects.update_or_create(
        user_id=user_id,
        defaults={
            "total_trades": total_trades,
        },
    )

    return f"Trade statistics updated for user {user_id}."


# ==========================================================
# PERFORMANCE METRICS
# ==========================================================

@shared_task
def update_performance_metrics(user_id):

    metrics, _ = PerformanceMetrics.objects.update_or_create(
        user_id=user_id,
    )

    # Detailed Sharpe, Sortino, volatility, etc.
    # can be calculated here later.

    return f"Performance metrics updated for user {user_id}."


# ==========================================================
# MARKET STATISTICS
# ==========================================================

@shared_task
def update_market_statistics():

    # This task can later consume Binance/exchange
    # market data and update MarketStatistics.

    return "Market statistics update completed."


# ==========================================================
# INDICATOR HISTORY
# ==========================================================

@shared_task
def update_indicator_history():

    # RSI / EMA / MACD calculations can be performed here.
    # Realtime calculations should remain in FastAPI.

    return "Indicator history update completed."


# ==========================================================
# STRATEGY PERFORMANCE
# ==========================================================

@shared_task
def update_strategy_performance(user_id):

    strategies = StrategyPerformance.objects.filter(
        user_id=user_id
    )

    # Detailed strategy calculations can be added later.

    return f"Updated {strategies.count()} strategies."


# ==========================================================
# EQUITY CURVE
# ==========================================================

@shared_task
def generate_equity_curve(user_id):

    # Calculate equity from user's portfolio/trades
    # and create EquityCurve records here.

    return f"Equity curve generated for user {user_id}."


# ==========================================================
# DRAWDOWN HISTORY
# ==========================================================

@shared_task
def generate_drawdown_history(user_id):

    # Calculate drawdown from equity curve here.

    return f"Drawdown history generated for user {user_id}."