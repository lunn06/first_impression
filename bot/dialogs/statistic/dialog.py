from aiogram_dialog import Dialog, Window, StartMode
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const

from bot.states import StatisticStates, MenuStates


def get_dialog() -> Dialog:
    statistic_window = Window(
        Const("Модуль не готов"),
        Start(
            Const("Назад"),
            id="switch_to_menu",
            state=MenuStates.menu,
            mode=StartMode.RESET_STACK,
        ),

        state=StatisticStates.statistic
    )

    dialog = Dialog(statistic_window)

    return dialog
