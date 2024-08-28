from aiogram.types import User
from aiogram_dialog import DialogManager

from bot.database.requests import get_supers


async def delete_super_getter(dialog_manager: DialogManager, **_kwargs):
    user: User = dialog_manager.middleware_data["event_from_user"]
    session = dialog_manager.middleware_data["session"]
    default_admins = dialog_manager.middleware_data["default_admins"]

    supers = await get_supers(session)
    is_default = user.id in default_admins

    supers_to_delete = []
    supers_to_delete_id = []
    for s in supers:
        name = s.telegram_id if s.user is None else s.user.user_name
        if s not in default_admins and s.telegram_id != user.id:
            if is_default and s.is_admin:
                supers_to_delete += [name]
                supers_to_delete_id += [s.telegram_id]
            elif s.is_moderator:
                supers_to_delete += [name]
                supers_to_delete_id += [s.telegram_id]

    dialog_manager.dialog_data["supers_to_delete_id"] = supers_to_delete_id

    return {
        "delete_super_text": "Выберите, кого вы хотите удалить",
        "back_button_text": "Назад",
        "supers": supers_to_delete
    }
