from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select

from bot.states import ViewSecretsStates


async def select_user_secrets_on_click(
        _callback: CallbackQuery,
        _select: Select,
        dialog_manager: DialogManager,
        item: str
):
    # secrets_dict: dict[str, Secret] = dialog_manager.middleware_data["secrets_dict"]
    selected_secret_id = int(item)
    # selected_secret_name = tuple(secrets_dict.values())[selected_secret_name_id]

    dialog_manager.dialog_data["selected_secret_id"] = selected_secret_id

    await dialog_manager.switch_to(ViewSecretsStates.view_secret)
