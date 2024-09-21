from typing import TYPE_CHECKING

from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment
from fluentogram import TranslatorRunner

from configs import Config

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner


async def secrets_getter(dialog_manager: DialogManager, i18n: TranslatorRunner, config: Config, **_kwargs):
    pic_attachment = None
    if config.secrets_pic is not None:
        pic_attachment = MediaAttachment(ContentType.PHOTO, path=str(config.secrets_pic))

    return {
        "text": i18n.secrets.message(),
        "back_to_menu_button_text": i18n.back.to.menu.button(),

        "pic": pic_attachment,
    }
