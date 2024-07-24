import asyncio
import re

from aiogram import Bot
from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput

from bot.dialogs.test_dialog.dialog import start_test_handler
from bot.utils.secrets import Secret

SECRET_RE = re.compile(r"(^\d{6}$)|(^\d{3} \d{3}$)|(^\d{2} \d{2} \d{2}$)")
ON_MESSAGE_SLEEP = 1.5


def validate_secret(text: str) -> str:
    if SECRET_RE.fullmatch(text) is not None:
        return text
    raise ValueError


async def text_input_on_success(message: Message, _text_input: ManagedTextInput, manager: DialogManager, text: str):
    manager.show_mode = ShowMode.EDIT

    secrets_dict: dict[str, Secret] = manager.middleware_data["secrets_dict"]

    wrong = False
    for dialog_name, secret in secrets_dict.items():
        if secret.verify(text):
            await start_test_handler(message, manager, dialog_name)  # type: ignore
            break
    else:
        wrong = True
        await message.answer("Неверный код(")

    await asyncio.sleep(ON_MESSAGE_SLEEP)

    bot: Bot = manager.middleware_data["bot"]
    await bot.delete_messages(
        message.from_user.id,  # type: ignore
        [message.message_id + 1, message.message_id] if wrong else [message.message_id]
    )


async def text_input_on_error(message: Message, _text_input: ManagedTextInput, manager: DialogManager, _err):
    manager.show_mode = ShowMode.EDIT

    await message.answer("Это не похоже на код :(")

    await asyncio.sleep(ON_MESSAGE_SLEEP)

    bot: Bot = manager.middleware_data["bot"]
    await bot.delete_messages(
        message.from_user.id,  # type: ignore
        [message.message_id, message.message_id + 1]
    )
