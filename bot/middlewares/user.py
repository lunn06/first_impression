from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.requests import ensure_user


class EnsureUserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        user: User = data.get("event_from_user")
        session: AsyncSession = data.get("session")

        # user_request_flag = get_flag(data, "user_request")
        # user_request_flag = check_flags(data, F.contains())
        user_name = user.username if user.username is not None else "no_user_name"
        dbuser = await ensure_user(session, user_id=user.id, user_name=user_name)
        ensured = dbuser is None
        # dbuser = await get_user_by_id(session, user_id=user.id)
        # data["user"] = dbuser
        data["ensured_user"] = ensured

        await handler(event, data)
