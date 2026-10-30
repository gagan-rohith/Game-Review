from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from redis.asyncio import Redis
from sqlalchemy import text

from app.config import get_settings
from app.db import SessionDep, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = Redis.from_url(get_settings().redis_url)
    yield
    await app.state.redis.aclose()
    await engine.dispose()


app = FastAPI(title="Review site API", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health(request: Request, session: SessionDep):
    """Reports whether the API can reach Postgres and Redis."""
    checks = {}
    try:
        await session.execute(text("SELECT 1"))
        checks["postgres"] = "ok"
    except Exception:
        checks["postgres"] = "down"
    try:
        await request.app.state.redis.ping()
        checks["redis"] = "ok"
    except Exception:
        checks["redis"] = "down"

    healthy = all(v == "ok" for v in checks.values())
    return JSONResponse(
        {"status": "ok" if healthy else "degraded", **checks},
        status_code=200 if healthy else 503,
    )
