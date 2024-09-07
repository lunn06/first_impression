from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel, SwitchTo
from aiogram_dialog.widgets.text import Format, Multi, List

from bot.dialogs.statistic.getters import statistics_getter, top_users_getter
from bot.states import StatisticStates


def get_dialog() -> Dialog:
    statistic_window = Window(
        Format("{text}"),

        SwitchTo(
            Format("{top_users_text}"),
            id="switch_to_top_users",
            state=StatisticStates.top_users
        ),

        Cancel(
            Format("{back_to_menu_button_text}"),
            id="back_to_menu",
            # state=MenuStates.menu,
            # mode=StartMode.RESET_STACK,
        ),

        getter=statistics_getter,
        state=StatisticStates.statistic,
    )

    top_users_window = Window(
        Multi(
            Format("{text}"),
            List(
                Format("{item[0]}. {item[1]} -> {item[2]}"),
                items="top_users",
            ),
            Format("{last_top}"),
        ),

        SwitchTo(
            Format("{back_button_text}"),
            id="back_to_statistics",
            state=StatisticStates.statistic,
        ),

        getter=top_users_getter,
        state=StatisticStates.top_users,
    )

    dialog = Dialog(
        statistic_window,
        top_users_window,
    )

    return dialog
