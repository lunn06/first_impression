import sqlalchemy.exc
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Select, Button, ManagedMultiselect
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.requests import ensure_super, ensure_super_tests, get_super_by_id
from bot.dialogs.admin.super_enum import SuperEnum
from bot.states import EnsureSuperStates
from bot.utils.secrets import Secret


def telegram_id_validator(text: str) -> str:
    if all(c.isdigit() for c in text):
        return text
    raise ValueError


async def super_id_on_success(
        message: Message,
        _text_input: ManagedTextInput,
        dialog_manager: DialogManager,
        item: str
) -> None:
    session = dialog_manager.middleware_data["session"]
    user_id = int(item)
    dialog_manager.dialog_data["new_super_id"] = user_id

    super_type = dialog_manager.dialog_data["super_type"]
    is_admin = super_type == SuperEnum.admin
    is_moderator = super_type == SuperEnum.moderator

    try:
        super_ = await get_super_by_id(session, user_id)
        print(super_)
        if super_ is None:
            await ensure_super(session, user_id, is_admin, is_moderator)
            await message.answer(f"{super_type} успешно добавлен")
        else:
            if super_.is_moderator:
                dialog_manager.dialog_data["super_type"] = SuperEnum.moderator
            elif super_.is_admin:
                dialog_manager.dialog_data["super_type"] = SuperEnum.admin
            await dialog_manager.switch_to(EnsureSuperStates.delete_super)
            return
    except sqlalchemy.exc.IntegrityError:
        await message.answer("Пользователь не найдем в базе данныx")

    if is_moderator:
        await dialog_manager.switch_to(EnsureSuperStates.choose_tests)


async def super_id_on_error(
        message: Message,
        _text_input: ManagedTextInput,
        _dialog_manager: DialogManager,
        _error,
) -> None:
    await message.answer("Это не телеграм id")


async def select_super_type_handler(
        _callback: CallbackQuery,
        _select: Select,
        dialog_manager: DialogManager,
        item: str
) -> None:
    if int(item) == 0:
        dialog_manager.dialog_data["super_type"] = SuperEnum.admin
    elif int(item) == 1:
        dialog_manager.dialog_data["super_type"] = SuperEnum.moderator
    else:
        raise ValueError

    await dialog_manager.switch_to(EnsureSuperStates.ensure_super)


async def process_choose_button_handler(
        _callback: CallbackQuery,
        _button: Button,
        dialog_manager: DialogManager,
) -> None:
    session: AsyncSession = dialog_manager.middleware_data["session"]
    new_super_id = dialog_manager.dialog_data["new_super_id"]

    secrets_dict: dict[str, Secret] = dialog_manager.middleware_data["secrets_dict"]
    tests = [secret.secret for secret in secrets_dict.values()]

    managed_multiselect: ManagedMultiselect = dialog_manager.find("choose_tests_multiselect")  # type: ignore
    assert isinstance(managed_multiselect, ManagedMultiselect)

    chosen_tests = list(map(
        lambda x: tests[int(x)],
        managed_multiselect.get_checked()
    ))

    print(chosen_tests)

    await ensure_super_tests(session, new_super_id, chosen_tests)
    await dialog_manager.switch_to(EnsureSuperStates.ensure_super)
