from aiogram_dialog import Dialog

from bot.dialogs import greeting, menu, statistic, secrets, where_to_go, test_dialog, back_to_menu


def get_dialogs() -> list[Dialog]:
    return [
        greeting.get_dialog(),
        menu.get_dialog(),
        statistic.get_dialog(),
        secrets.get_dialog(),
        where_to_go.get_dialog(),
        test_dialog.get_dialog(),
        back_to_menu.get_dialog(),
    ]
