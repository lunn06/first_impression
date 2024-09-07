
from redis.asyncio import Redis

from bot.database.cached_requests import get_top_users


async def statistics_getter(**_kwargs):
    return {
        "text": "Какую статистику смотрим?",
        "top_users_text": "Общий рейтинг",
        "back_to_menu_button_text": "Назад",
    }


async def top_users_getter(cache: Redis, **_kwargs):
    top_users, last_top = await get_top_users(cache)
    minutes = last_top.minute if last_top.minute > 9 else "0" + str(last_top.minute)
    last_top_str = f"{last_top.date()} {last_top.hour}:{minutes}"
    return {
        "last_top": f"Время обновление: {last_top_str}",
        "text": "Топ пользователей:",
        "top_users": tuple((i + 1, v[0], v[1]) for i, v in enumerate(top_users)),

        "back_button_text": "Назад"
    }
