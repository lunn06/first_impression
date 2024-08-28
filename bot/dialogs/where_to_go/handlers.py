from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select

from bot.states import WhereToGoStates


async def select_locations_on_click(
        _callback: CallbackQuery,
        _managed_select: Select,
        dialog_manager: DialogManager,
        item: str,
):
    locations = dialog_manager.dialog_data["locations"]
    selected_location_id = int(item)

    selected_location = locations[selected_location_id]
    dialog_manager.dialog_data["selected_location"] = selected_location

    await dialog_manager.switch_to(WhereToGoStates.audiences)


async def select_audience_on_click(
        _callback: CallbackQuery,
        _managed_select: Select,
        dialog_manager: DialogManager,
        item: str,
):
    audiences = dialog_manager.dialog_data["audiences"]
    selected_audience_id = int(item)

    selected_audience = audiences[selected_audience_id]
    dialog_manager.dialog_data["selected_audience"] = selected_audience

    await dialog_manager.switch_to(WhereToGoStates.description)
