from fastapi import FastAPI

from api.routes import router as api_router
from api.websockets import router as websocket_router
from services.routes import router as services_router
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI(title="Fintech Realtime")

app.include_router(api_router)
app.include_router(services_router)
app.include_router(websocket_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
	import uvicorn

	uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)