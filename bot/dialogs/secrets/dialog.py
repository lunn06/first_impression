from aiogram_dialog import Dialog, Window, StartMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Format

from bot.dialogs.secrets.handlers import validate_secret, text_input_on_error, text_input_on_success
from bot.dialogs.secrets.getters import secrets_getter
from bot.states import MenuStates, SecretsStates


def get_dialog() -> Dialog:
    secrets_window = Window(
        Format("{text}"),
        Start(
            Format("{back_to_menu_button_text}"),
            id="switch_to_menu",
            state=MenuStates.menu,
            mode=StartMode.RESET_STACK,
        ),

        TextInput(
            type_factory=validate_secret,
            on_success=text_input_on_success,
            on_error=text_input_on_error,

            id="parse_secret_input"
        ),

        state=SecretsStates.secrets,
        getter=secrets_getter,
    )

    dialog = Dialog(secrets_window)

    return dialog
