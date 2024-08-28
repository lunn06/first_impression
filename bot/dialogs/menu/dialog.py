from aiogram_dialog import Dialog, Window, StartMode
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory
from aiogram_dialog.widgets.text import Format

from bot.dialogs.menu.handlers import delete_clicked_menu_button
from bot.dialogs.menu.getters import menu_getter
from bot.states import MenuStates, StatisticStates, SecretsStates, WhereToGoStates, SuperStates


def get_dialog() -> Dialog:
    menu_window = Window(
        Format("{text}"),

        Start(
            Format("{start_admin_button}"),
            id="start_admin_section",
            # on_click=delete_clicked_menu_button,  # type: ignore
            state=SuperStates.menu,
            mode=StartMode.NORMAL,
            when="is_super",
        ),

        Start(
            Format("{start_statistics_button}"),
            id="start_statistic_section",
            # on_click=delete_clicked_menu_button,  # type: ignore
            state=StatisticStates.statistic,
            mode=StartMode.NORMAL,
        ),

        Start(
            Format("{start_where_to_go_button}"),
            id="start_where_to_go_section",
            # on_click=delete_clicked_menu_button,  # type: ignore
            state=WhereToGoStates.locations,
            mode=StartMode.NORMAL,
        ),

        Start(
            Format("{start_secrets_button}"),
            id="start_secrets_section",
            # on_click=delete_clicked_menu_button,  # type: ignore
            state=SecretsStates.secrets,
            mode=StartMode.NORMAL,
        ),

        state=MenuStates.menu,
        getter=menu_getter,
        # markup_factory=ReplyKeyboardFactory(
        #     resize_keyboard=True,
        #     one_time_keyboard=True,
        # )
    )

    dialog = Dialog(menu_window)

    return dialog
