from typing import TYPE_CHECKING

from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment
from fluentogram import TranslatorRunner

from configs import Config

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner


async def greeting_getter(dialog_manager: DialogManager, i18n: TranslatorRunner, config: Config, **_kwargs):
    pic_attachment = None
    if config.greeting_pic is not None:
        pic_attachment = MediaAttachment(ContentType.PHOTO, path=str(config.greeting_pic))
    return {
        "text": i18n.start.message(),
        "start_button_text": i18n.start.button(),

        "pic": pic_attachment,
    }


async def auth_getter(dialog_manager: DialogManager, **_kwargs):
    return {
        "text": "Для начала нужно авторизоваться!",
        "url_text": "Авторизоваться",
        "url": "https://tpu.ru"  # TODO: перенести в конфиг
    }
