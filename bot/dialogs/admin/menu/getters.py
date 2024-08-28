from aiogram.types import User
from aiogram_dialog import DialogManager
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.requests import get_super_by_id


async def menu_getter(session: AsyncSession, dialog_manager: DialogManager, **_kwargs):
    user: User = dialog_manager.middleware_data["event_from_user"]
    super_ = await get_super_by_id(session, user.id)

    assert super_

    user_status = "админа" if super_.is_admin else "модератора"

    return {
        "admin_menu_greeting": f"Добро пожаловать в панель {user_status}",
        "ensure_super_button_text": "Добавить супер-пользователя",
        "delete_super_button_text": "Удалить супер-пользователя",
        "view_top_button_text": "Посмотреть топ пользователей",
        "view_secrets_button_text": "Доступные коды",
        "back_to_menu_button_text": "Назад в меню",

        "is_admin": super_.is_admin,
    }
