from aiogram.types import User
from aiogram_dialog import DialogManager

from bot.dialogs.admin.super_enum import SuperEnum
from bot.utils.secrets import Secret


async def select_super_type_getter(**_kwargs):
    return {
        "choose_super_type_text": "Кого добавить?",
        "super_types": ((0, SuperEnum.admin), (1, SuperEnum.moderator)),
        "cancel_button_text": "Назад",
    }


async def ensure_super_getter(**_kwargs):
    return {
        "ensure_super_text": "Введите ID",
        "back_button_text": "Назад",
    }


async def choose_tests_getter(dialog_manager: DialogManager, **_kwargs):
    secrets_dict: dict[str, Secret] = dialog_manager.middleware_data["secrets_dict"]
    names = [secret.name for secret in secrets_dict.values()]

    return {
        "choose_tests_text": "Выберите что модерировать",
        "process_choose_button_text": "Готово",
        "back_button_text": "Назад",

        "tests": tuple(enumerate(names))
    }


async def replace_super_getter(dialog_manager: DialogManager, **_kwargs):
    default_admins = dialog_manager.middleware_data["default_admins"]
    user: User = dialog_manager.middleware_data["event_from_user"]

    super_type = dialog_manager.dialog_data["super_type"]
    if super_type == SuperEnum.admin:
        super_type_text = "админом"
    elif super_type == SuperEnum.moderator:
        super_type_text = "модератором"
    return {
        "replace_super_text": f"Пользователь уже является {super_type_text}",
        "back_button_text": "Назад",

        "is_moderator": super_type == SuperEnum.moderator,
        "is_admin": super_type == SuperEnum.admin,
        "user_is_default_admin": user.id in default_admins
    }
