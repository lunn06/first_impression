import datetime

import orjson
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.requests import (
    ensure_user_test as nocache_ensure_user_test,
    get_user_tests as nocache_get_user_tests,
)


async def ensure_top_users(cache: Redis, top_users: tuple[tuple[str, float]], sent_time: float):
    async with cache.pipeline(transaction=True) as pipe:
        await pipe.delete("last_top")
        for item in top_users:
            await pipe.rpush("last_top", orjson.dumps(item))  # type: ignore
        await pipe.set("last_top_time", sent_time)

        await pipe.execute()


async def get_top_users(cache: Redis) -> (str, tuple[tuple[str, ...], datetime]):
    # last_top = await cache.get("last_top")
    top_users_list = await cache.lrange("last_top", 0, -1)  # type: ignore
    top_users_str = [orjson.loads(item) for item in top_users_list]
    top_time = datetime.datetime.fromtimestamp(
        float(await cache.get("last_top_time")),
        tz=datetime.timezone(datetime.timedelta(hours=7))
    )

    return top_users_str, top_time


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
