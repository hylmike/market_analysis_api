from contextlib import asynccontextmanager

from fastapi import FastAPI
from dotenv import load_dotenv

from api.ai_assistant.assistant_router import ai_assistant_router

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Function handles app startup and shutdown events"""
    yield


server = FastAPI(lifespan=lifespan, debug=True)


@server.get("/status")
async def check_api():
    return {"status": "Connected to API successfully"}


# Routers
server.include_router(
    ai_assistant_router,
    prefix="/api/ai_assistant",
    tags=["ai_assistant"],
    responses={404: {"description": "Not Found"}},
)
