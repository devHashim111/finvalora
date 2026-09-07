import pickle

from fastapi import APIRouter, HTTPException
from redis.asyncio import Redis

router = APIRouter(
    prefix="/services",
    tags=["services"],
)

redis = Redis.from_url(
    "redis://127.0.0.1:6379/2",
    decode_responses=False,
)

COIN_MAP = {
    "BTC": "bitcoin",
    "BTCUSDT": "bitcoin",
    "BTCUSD": "bitcoin",
    "BTCUSDC": "bitcoin",
    "ETH": "ethereum",
    "ETHUSDT": "ethereum",
    "ETHUSD": "ethereum",
    "ETHUSDC": "ethereum",
    "BNB": "binancecoin",
    "BNBUSDT": "binancecoin",
    "BNBUSD": "binancecoin",
    "BNBUSDC": "binancecoin",
    "SOL": "solana",
    "SOLUSDT": "solana",
    "SOLUSD": "solana",
    "SOLUSDC": "solana",
    "XRP": "ripple",
    "XRPUSDT": "ripple",
    "XRPUSD": "ripple",
    "XRPUSDC": "ripple",
}

def normalize_coin(value: str) -> str:
    value = value.strip().upper()
    if value in COIN_MAP:
        return COIN_MAP[value]
    return value.lower()

@router.get("/market")
async def get_market():
    data = await redis.get(":1:crypto:market")

    if data is None:
        raise HTTPException(
            status_code=404,
            detail="Crypto market data not available",
        )

    try:
        market_data = pickle.loads(data)
        return {"data": market_data}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to decode market data: {str(e)}",
        )

@router.get("/market/{coin}")
async def get_coin(coin: str):
    redis_coin = normalize_coin(coin)
    data = await redis.get(f":1:crypto:{redis_coin}")

    if data is None:
        raise HTTPException(
            status_code=404,
            detail=f"{coin} data not available",
        )

    try:
        coin_data = pickle.loads(data)

        return {
            "coin": redis_coin,
            "symbol": coin.upper(),
            "data": coin_data,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to decode data: {str(e)}",
        )