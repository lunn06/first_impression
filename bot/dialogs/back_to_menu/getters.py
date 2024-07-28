from aiogram_dialog import DialogManager


async def back_to_menu_getter(**_kwargs):
    return {
        "text": "Уверен, что хочешь вернуться в главное меню?",
        "back_to_menu_button": "Главное меню",
        "back_to_preview_button": "Назад"
    }