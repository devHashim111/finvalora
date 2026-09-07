import asyncio
import json

import redis.asyncio as redis

from fastapi import APIRouter, WebSocket, WebSocketDisconnect


router = APIRouter(prefix="/ws", tags=["ws"])


@router.websocket("/market")
async def market_websocket(websocket: WebSocket):

    await websocket.accept()

    redis_client = redis.Redis(
        host="127.0.0.1",
        port=6379,
        db=2,
        decode_responses=True,
    )

    pubsub = redis_client.pubsub()

    await pubsub.subscribe("crypto_market_updates")

    try:

        while True:

            message = await pubsub.get_message(
                ignore_subscribe_messages=True,
                timeout=1.0,
            )

            if message:

                data = json.loads(message["data"])

                await websocket.send_json(data)

            await asyncio.sleep(0.01)

    except WebSocketDisconnect:

        print("WebSocket client disconnected")

    finally:

        await pubsub.unsubscribe(
            "crypto_market_updates"
        )

        await pubsub.close()

        await redis_client.aclose()