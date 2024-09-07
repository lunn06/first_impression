from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Start

from bot.database.requests import get_test_by_name, ensure_user_test
from configs import Questions


async def process_back_to_menu_button(
        callback: CallbackQuery,
        _start_widget: Start,
        dialog_manager: DialogManager
):
    session = dialog_manager.middleware_data["session"]
    right_count_dict: dict[str, float] = dialog_manager.start_data["right_answers"]
    right_count = round(sum(right_count_dict.values()), 3)
    questions_count: int = dialog_manager.start_data["questions_count"]

    questions_json = dialog_manager.start_data["user_questions"]
    user_questions = Questions.model_validate_json(questions_json)

    dialog_name = dialog_manager.start_data["dialog_name"]

    test = await get_test_by_name(session, dialog_name)
    assert test

    limit_coast = user_questions.coast / (100 / user_questions.limit)
    decreased_count = user_questions.coast - test.complete_count * user_questions.decrease
    if decreased_count > limit_coast:
        user_questions.coast = decreased_count
    else:
        user_questions.coast = limit_coast

    points_per_question = user_questions.coast / questions_count
    user_total = round(right_count * points_per_question, 3)

    await ensure_user_test(session, callback.from_user.id, dialog_name, user_total)
