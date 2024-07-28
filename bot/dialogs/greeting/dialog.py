from aiogram.filters import CommandObject
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button, Url, Start
from aiogram_dialog.widgets.text import Format

from bot.dialogs.greeting.getters import greeting_getter, auth_getter
from bot.dialogs.greeting.handlers import on_click_greeting_button
from bot.states import GreetingStates, MenuStates


async def start_handler(message: CallbackQuery, command: CommandObject, dialog_manager: DialogManager):
    await dialog_manager.start(
        state=GreetingStates.greeting,
        data={
            "oauth": command.args
        }
    )


def get_dialog() -> Dialog:
    greeting_window = Window(
        Format("{text}"),
        Button(
            Format("{start_button_text}"),
            id="greeting_start_button",
            on_click=on_click_greeting_button  # type: ignore
        ),

        state=GreetingStates.greeting,
        getter=greeting_getter,
    )

    auth_window = Window(
        Format("{text}"),
        Url(
            text=Format("{url_text}"),
            url=Format("{url}"),
        ),
        Start(
            Format("Фальшивая"),
            id="switch_to_main",
            state=MenuStates.menu,
            mode=StartMode.RESET_STACK
        ),

        state=GreetingStates.auth,
        getter=auth_getter
    )

    dialog = Dialog(greeting_window, auth_window)

    return dialog
