from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bot.states import GreetingStates, MenuStates


async def on_click_greeting_button(_callback: CallbackQuery, _button: Button, manager: DialogManager):
    oauth_credentials = manager.start_data.get("oauth", None)
    if oauth_credentials is None:
        await manager.switch_to(GreetingStates.auth)
    else:
        await manager.switch_to(MenuStates.menu)  # TODO: сделать хандлер старта меню
