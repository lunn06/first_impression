from aiogram_dialog import Dialog, Window, StartMode
from aiogram_dialog.widgets.kbd import Start, Cancel, Row
from aiogram_dialog.widgets.text import Format

from bot.dialogs.back_to_menu.getters import back_to_menu_getter
from bot.dialogs.back_to_menu.handlers import process_back_to_menu_button
from bot.states import BackToMenuStates, MenuStates


def get_dialog() -> Dialog:
    back_to_menu_window = Window(
        Format("{text}"),
        Row(
            Cancel(
                Format("{back_to_preview_button}"),
                id="back_to_preview",
            ),
            Start(
                Format("{back_to_menu_button}"),
                id="back_to_menu",
                state=MenuStates.menu,
                on_click=process_back_to_menu_button,  # type: ignore
                mode=StartMode.RESET_STACK,
            ),
        ),

        state=BackToMenuStates.back_to_menu,
        getter=back_to_menu_getter
    )

    dialog = Dialog(back_to_menu_window)

    return dialog
