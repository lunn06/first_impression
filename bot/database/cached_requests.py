import datetime

import orjson
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.requests import (
    ensure_user_test as nocache_ensure_user_test,
    get_user_tests as nocache_get_user_tests,
)


async def ensure_top_users(cache: Redis, top_users: str, sent_time: datetime):
    # now = datetime.datetime.now(tz=datetime.timezone.utc)
    # key = f"top:{now.date()}:{now.hour}:{now.minute}"
    # for user in top_users:
    #     await cache.append(
    #         key,
    #         orjson.dumps(
    #             (user.user_name, float(user.user_points))
    #         )
    #     )  # type: ignore
    #
    if await cache.exists("last_top"):
        await cache.delete("last_top")
        await cache.delete("last_top_time")
    await cache.setnx("last_top", top_users)
    await cache.setnx("last_top_time", sent_time)


async def get_top_users(cache: Redis) -> (str, tuple[tuple[str, ...], datetime]):
    # last_top = await cache.get("last_top")
    top_users_str = orjson.loads(await cache.get("last_top"))
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
