from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.requests import (
    ensure_user_test as nocache_ensure_user_test,
    get_user_tests as nocache_get_user_tests,
)


async def ensure_user_test(session: AsyncSession, user_id: int, test_name: str, test_points: float, cache: Redis):
    await nocache_ensure_user_test(session, user_id, test_name, test_points)
    await cache.delete(str(user_id))


async def get_user_tests(session: AsyncSession, user_id: int, cache: Redis) -> list[str]:
    cache_exists = await cache.exists(str(user_id))
    if not cache_exists:
        user_tests = await nocache_get_user_tests(session, user_id)
        for user_test in user_tests:
            await cache.sadd(str(user_id), user_test)  # type: ignore
    else:
        user_tests = await cache.smembers(str(user_id))  # type: ignore
        user_tests = list(map(lambda x: x.decode("ascii"), user_tests))  # type: ignore

    return user_tests
