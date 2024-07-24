from aiogram_dialog import DialogManager


async def secrets_getter(dialog_manager: DialogManager, **_kwargs):
    return {
        "text": "Здесь ты можешь ввести найденные коды",
        "back_to_menu_button_text": "Вернуться в главное меню"
    }