from aiogram_dialog import DialogManager

from bot.dialogs.admin.super_enum import SuperEnum
from utils.secrets import Secret


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
