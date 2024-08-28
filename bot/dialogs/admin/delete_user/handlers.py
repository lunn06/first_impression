from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, ManagedMultiselect
from sqlalchemy.ext.asyncio import AsyncSession


async def process_delete_super_handler(
        _callback: CallbackQuery,
        _button: Button,
        dialog_manager: DialogManager,
):
    session: AsyncSession = dialog_manager.middleware_data["session"]

    managed_multiselect: ManagedMultiselect = dialog_manager.find("delete_super_multiselect")  # type: ignore
    assert isinstance(managed_multiselect, ManagedMultiselect)
