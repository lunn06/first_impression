import datetime
import random
from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery, User
from redis.asyncio import Redis


class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self, time_delta: float, cache: Redis):
        self.cache: Redis = cache
        self.timedelta_limiter: datetime.timedelta = datetime.timedelta(seconds=time_delta)

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        user = data.get('event_from_user')
        assert isinstance(user, User)

        str_user_id = str(user.id)
        if not await self.cache.exists(str_user_id):
            await self.set_time_update(str_user_id, datetime.datetime.now().timestamp())
            return await handler(event, data)

    async def set_time_update(self, str_user_id: str, timestamp: float):
        px = datetime.timedelta(milliseconds=random.randrange(-50, 50 + 1))
        await self.cache.set(str_user_id, timestamp, px=self.timedelta_limiter + px)
