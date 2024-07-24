from aiogram_dialog import DialogManager


async def menu_getter(dialog_manager: DialogManager, **_kwargs):
    return {
        "text": "Добро пожаловать в главное меню!",
        "start_statistics_button": "Статистика",
        "start_secrets_button": "Ввести код"
    }
