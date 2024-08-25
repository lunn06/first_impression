import asyncio
import re

from aiogram import Bot
from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.cached_requests import get_user_tests
from bot.dialogs.test_dialog.dialog import start_test_handler
from bot.utils.secrets import Secret

SECRET_RE = re.compile(r"(^\d{6}$)|(^\d{3} \d{3}$)|(^\d{2} \d{2} \d{2}$)")
ON_MESSAGE_SLEEP = 1.5


def validate_secret(text: str) -> str:
    if SECRET_RE.fullmatch(text) is not None:
        return ''.join(text.split())
    raise ValueError


async def text_input_on_success(
        message: Message,
        _text_input: ManagedTextInput,
        manager: DialogManager,
        text: str
) -> None:
    manager.show_mode = ShowMode.EDIT

    secrets_dict: dict[str, Secret] = manager.middleware_data["secrets_dict"]
    session: AsyncSession = manager.middleware_data["session"]
    cache: Redis = manager.middleware_data["cache"]

    wrong = False
    for dialog_name, secret in secrets_dict.items():
        if secret.verify(text):
            user_tests = await get_user_tests(session, message.from_user.id, cache)
            if dialog_name in user_tests:
                await message.answer("Это точку ты уже проходил!")
                wrong = True
            else:
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
