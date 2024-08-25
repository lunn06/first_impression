from aiogram.types import User
from aiogram_dialog import DialogManager
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.requests import get_supers_ids


async def menu_getter(dialog_manager: DialogManager, **_kwargs):
    session: AsyncSession = dialog_manager.middleware_data["session"]
    user: User = dialog_manager.middleware_data['event_from_user']

    supers_ids = await get_supers_ids(session)

    return {
        "text": "Добро пожаловать в главное меню!",
        "start_admin_button": "Панель",
        "start_statistics_button": "Статистика",
        "start_secrets_button": "Ввести код",
        "start_where_to_go_button": "Куда пойти?",
        "is_super": user.id in supers_ids,
    }
