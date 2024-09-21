import operator

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel, SwitchTo, ScrollingGroup, Select
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Format, Multi, List

from bot.dialogs.statistic.getters import statistics_getter, top_users_getter, user_tests_getter
from bot.states import StatisticStates


def get_dialog() -> Dialog:
    statistic_window = Window(
        Format("{text}"),

        SwitchTo(
            Format("{top_users_text}"),
            id="switch_to_top_users",
            state=StatisticStates.top_users
        ),

        SwitchTo(
            Format("{user_tests_text}"),
            id="switch_to_user_tests",
            state=StatisticStates.user_tests
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
        DynamicMedia("pic"),
        Multi(
            # Format("{text}"),
            List(
                Format("{item[1]} {item[2]}"),
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

    user_tests_window = Window(
        Format("{text}"),

        ScrollingGroup(
            Select(
                Format("{item[1]}"),
                id="user_tests_select",
                item_id_getter=operator.itemgetter(0),
                items="tests",
            ),
            width=1,
            height=5,
            id="choose_tests_scrolling",
        ),

        SwitchTo(
            Format("{back_button_text}"),
            id="back_to_statistics",
            state=StatisticStates.statistic,
        ),

        getter=user_tests_getter,
        state=StatisticStates.user_tests,
    )

    dialog = Dialog(
        statistic_window,
        top_users_window,
        user_tests_window,
    )

    return dialog
