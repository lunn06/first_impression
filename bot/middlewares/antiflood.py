import datetime
from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery, User


class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self, time_delta: int):
        self.time_updates: dict[int, datetime.datetime] = {}
        self.timedelta_limiter: datetime.timedelta = datetime.timedelta(seconds=time_delta)

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, (Message, CallbackQuery)):
            user: User = data.get('event_from_user')

            if user.id in self.time_updates.keys():
                if (datetime.datetime.now() - self.time_updates[user.id]) > self.timedelta_limiter:
                    self.time_updates[user.id] = datetime.datetime.now()
                    return await handler(event, data)
            else:
                self.time_updates[user.id] = datetime.datetime.now()
                return await handler(event, data)
