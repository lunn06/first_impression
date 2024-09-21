from typing import TYPE_CHECKING

from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner


async def back_to_menu_getter(i18n: TranslatorRunner, **_kwargs):
    return {
        "text": "Уверен, что хочешь вернуться в главное меню? Ты получишь очки только за пройденные вопросы",
        "back_to_menu_button": i18n.back.to.menu.button(),
        "back_to_preview_button": "Назад"
    }
