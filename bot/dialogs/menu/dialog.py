from aiogram_dialog import Dialog, Window, StartMode
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory
from aiogram_dialog.widgets.text import Format

from bot.dialogs.menu.getters import menu_getter
from bot.states import MenuStates, StatisticStates, SecretsStates


def get_dialog() -> Dialog:
    menu_window = Window(
        Format("{text}"),
        Start(
            Format("{start_statistics_button}"),
            id="start_statistic_section",
            state=StatisticStates.statistic,
            mode=StartMode.NORMAL,
        ),

        Start(
            Format("{start_secrets_button}"),
            id="start_secrets_section",
            state=SecretsStates.secrets,
            mode=StartMode.NORMAL,
        ),

        state=MenuStates.menu,
        getter=menu_getter,
        markup_factory=ReplyKeyboardFactory(
            resize_keyboard=True,
            one_time_keyboard=True,
        )
    )

    dialog = Dialog(menu_window)

    return dialog
