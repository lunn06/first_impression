from aiogram_dialog import Dialog, Window, StartMode
from aiogram_dialog.widgets.kbd import Start, Cancel
from aiogram_dialog.widgets.text import Const

from bot.states import WhereToGoStates


def get_dialog() -> Dialog:
    where_to_go_window = Window(
        Const("Модуль не готов"),
        Cancel(
            Const("Назад"),
            id="switch_to_menu",
            # state=MenuStates.menu,
            # mode=StartMode.RESET_STACK,
        ),

        state=WhereToGoStates.where_to_go
    )

    dialog = Dialog(where_to_go_window)

    return dialog
