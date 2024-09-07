from aiogram.types import User
from aiogram_dialog import DialogManager
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.requests import get_super_by_id, get_super_tests, get_test_by_name
from configs import Questions
from utils import Secret


async def user_secrets_getter(
        session: AsyncSession,
        event_from_user: User,
        secrets_dict: dict[str, Secret],
        **_kwargs
):
    super_ = await get_super_by_id(session, event_from_user.id)
    assert super_

    if super_.is_moderator:
        super_tests = await get_super_tests(session, event_from_user.id)
        user_secrets_names = [s.name for s in secrets_dict.values() if s.secret in super_tests]
    else:
        user_secrets_names = [s.name for s in secrets_dict.values()]

    # dialog_manager.dialog_data["user_secrets_names"] = user_secrets_names

    return {
        "text": "Выберите, какой код вы хотите узнать",
        "user_secrets": tuple(enumerate(user_secrets_names)),
        "back_button_text": "Назад",
    }


async def view_secret_getter(
        session: AsyncSession,
        secrets_dict: dict[str, Secret],
        questions_dict: dict[str, Questions],
        dialog_manager: DialogManager,
        **_kwargs,
):
    selected_secret_id = dialog_manager.dialog_data["selected_secret_id"]
    selected_secret: Secret = tuple(secrets_dict.values())[selected_secret_id]

    test = await get_test_by_name(session, selected_secret.secret)
    questions = questions_dict[selected_secret.secret]

    return {
        "name": f"Название: {questions.name}",
        "interval": f"Интревал обновления кода: {questions.interval} с.",
        "count": f"Количество прохождений: {test.complete_count}",
        "totp": f"Секретный код: {selected_secret.totp.now()}",
        "location": f"Адрес: {questions.location}",
        "audience": f"Аудитория: {questions.audience}",

        "update_button_text": "Обновить",
        "back_button_text": "Назад",
    }
