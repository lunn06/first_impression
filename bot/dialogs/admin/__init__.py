from aiogram_dialog import Dialog

from bot.dialogs.admin import menu, ensure_user


def get_dialogs() -> list[Dialog]:
    return [
        menu.get_dialog(),
        ensure_user.get_dialog(),
    ]
