from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from agents.router import router as agents_router
from auth.base_config import fastapi_users, auth_backend
from auth.schemas import UserRead, UserCreate
from providers.router import router as sellers_router
from clients.router import router as clients_router
from deals.router import router as purchases_router
from contracts.router import router as contracts_router
from stats.router import router as stats_router

from redis import asyncio as aioredis


app = FastAPI(title="Arbitrage statistic documentation",
              description="Description of REST routes for working with statistics.")

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"]
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"]
)

app.include_router(agents_router)
app.include_router(sellers_router)
app.include_router(clients_router)
app.include_router(purchases_router)
app.include_router(contracts_router)
app.include_router(stats_router)


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("redis://localhost:6379", encoding="utf-8", decode_response=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
