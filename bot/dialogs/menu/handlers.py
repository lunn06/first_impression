from aiogram_dialog import DialogManager
from aiogram_dialog.api.internal import ReplyCallbackQuery
from aiogram_dialog.widgets.kbd import Start


async def delete_clicked_menu_button(callback: ReplyCallbackQuery, _button: Start, manager: DialogManager, **_kwargs):
    await callback.original_message.delete()
