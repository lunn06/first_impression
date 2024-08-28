from aiogram_dialog import DialogManager


async def greeting_getter(dialog_manager: DialogManager, **_kwargs):
    return {
        "text": "Привет! Начнём?",
        "start_button_text": "Полетели"
    }


async def auth_getter(dialog_manager: DialogManager, **_kwargs):
    return {
        "text": "Для начала нужно авторизоваться!",
        "url_text": "Авторизоваться",
        "url": "https://tpu.ru"  # TODO: перенести в конфиг
    }
