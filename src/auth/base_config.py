import redis.asyncio
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import BearerTransport, RedisStrategy, AuthenticationBackend

from auth.manager import get_user_manager
from database import User

bearer_transport = BearerTransport(tokenUrl="auth/login")
redis = redis.asyncio.from_url("redis://localhost:6379", decode_responses=True)


def get_redis_strategy() -> RedisStrategy:
    return RedisStrategy(redis, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="bearer",
    transport=bearer_transport,
    get_strategy=get_redis_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)

current_user = fastapi_users.current_user()
