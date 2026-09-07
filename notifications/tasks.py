
import requests

from celery import shared_task
from django.core.cache import cache

import redis


@shared_task
def fetch_crypto_market():

    symbols = [
        "bitcoin",
        "ethereum",
        "binancecoin",
        "solana",
        "ripple",
    ]

    try:

        response = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={
                "ids": ",".join(symbols),
                "vs_currencies": "usd",
                "include_24hr_change": "true",
            },
            timeout=None,
        )

        response.raise_for_status()

        data = response.json()

        # Save latest market data in Django Redis cache
        cache.set(
            "crypto:market",
            data,
            timeout=None,
        )

        for symbol, market_data in data.items():

            cache.set(
                f"crypto:{symbol}",
                market_data,
                timeout=None,
            )

        # Redis Pub/Sub
        redis_client = redis.Redis(
            host="127.0.0.1",
            port=6379,
            db=2,
        )

        redis_client.publish(
            "crypto_market_updates",
            __import__("json").dumps(data)
        )

        return data

    except Exception as e:

        return {
            "error": str(e)
        }