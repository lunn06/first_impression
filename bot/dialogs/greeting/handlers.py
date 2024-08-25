from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bot.database.requests import ensure_user, get_super_by_id
from bot.states import GreetingStates, MenuStates


async def on_click_greeting_button(callback: CallbackQuery, _button: Button, manager: DialogManager):
    session = manager.middleware_data["session"]
    default_admins = manager.middleware_data["default_admins"]
    super_ = await get_super_by_id(session, callback.from_user.id)
    is_admin = super_ is not None and super_.is_admin
    is_moderator = super_ is not None and super_.is_moderator

    await ensure_user(
        session,
        callback.from_user.id,
        callback.from_user.username,
        is_admin=callback.from_user.id in default_admins or is_admin,
        is_moderator=is_moderator
    )

    oauth_credentials = manager.start_data.get("oauth", None)
    if oauth_credentials is None:
        await manager.switch_to(GreetingStates.auth)
    else:
        await manager.switch_to(MenuStates.menu)
