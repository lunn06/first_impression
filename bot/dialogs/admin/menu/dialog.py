from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo, Column, Cancel, Start
from aiogram_dialog.widgets.text import Format

from bot.dialogs.admin.menu.getters import menu_getter
from bot.states import SuperStates, EnsureSuperStates, DeleteSuperStates


def get_dialog() -> Dialog:
    menu_window = Window(
        Format("{admin_menu_greeting}"),

        Column(
            Start(
                Format("{ensure_super_button_text}"),
                id="ensure_super_button",
                state=EnsureSuperStates.choose_type,
            ),

            Start(
                Format("{delete_super_button_text}"),
                id="delete_super_button",
                state=DeleteSuperStates.delete_super,
            ),

            SwitchTo(
                Format("{view_top_button_text}"),
                id="view_top_button",
                state=SuperStates.view_top,
            ),

            when="is_admin",
        ),

        SwitchTo(
            Format("{view_secrets_button_text}"),
            id="view_secrets_button",
            state=SuperStates.view_secrets,
        ),

        Cancel(
            Format("{back_to_menu_button_text}"),
        ),

        getter=menu_getter,
        state=SuperStates.menu,

        # markup_factory=ReplyKeyboardFactory(
        #     resize_keyboard=True,
        #     one_time_keyboard=True,
        # )
    )

    return Dialog(
        menu_window,
    )
