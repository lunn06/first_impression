from aiogram.types import User
from aiogram_dialog import DialogManager, StartMode
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.requests import get_test_by_name, ensure_user_test
from bot.states import MenuStates
from configs import Questions, QuestionsTypeEnum

RESULT_ROUND = 2


async def description_getter(dialog_manager: DialogManager, **_kwargs):
    questions_json = dialog_manager.start_data["user_questions"]  # type: ignore
    questions = Questions.model_validate_json(questions_json)

    return {
        "text": questions.description,
        "next_text": "Понял!" if questions.only_info else "Начнём!"
    }


async def test_getter(dialog_manager: DialogManager, event_from_user: User, **_kwargs):
    questions_json = dialog_manager.start_data["user_questions"]  # type: ignore
    questions = Questions.model_validate_json(questions_json)
    question_index: int = dialog_manager.dialog_data.get("question_index", 0)

    current_question = questions[question_index]

    return {
        "text": current_question.text,
        "button_next_text": "Дальше",
        "back_to_menu_button_text": "Назад в главное меню",
        "answers": [(i + 1, a) for i, a in enumerate(current_question.answers)],
        "question_index": question_index,
        "is_multiselect": current_question.type == QuestionsTypeEnum.multiselect,
        "is_select": current_question.type == QuestionsTypeEnum.select,
        "is_text": current_question.type == QuestionsTypeEnum.text,
        "is_info": current_question.type == QuestionsTypeEnum.info,
    }


async def results_getter(session: AsyncSession, dialog_manager: DialogManager, **_kwargs):
    right_count_dict: dict[str, float] = dialog_manager.start_data["right_answers"]  # type: ignore
    right_count = round(sum(right_count_dict.values()), 3)
    questions_count: int = dialog_manager.start_data["questions_count"]  # type: ignore

    questions_json = dialog_manager.start_data["user_questions"]  # type: ignore
    user_questions = Questions.model_validate_json(questions_json)

    dialog_name = dialog_manager.start_data["dialog_name"]  # type: ignore

    test = await get_test_by_name(session, dialog_name)
    assert test

    limit_coast = user_questions.coast / (100 / user_questions.limit)
    decreased_count = user_questions.coast - test.complete_count * user_questions.decrease
    if decreased_count > limit_coast:
        user_questions.coast = decreased_count
    else:
        user_questions.coast = limit_coast

    points_per_question = user_questions.coast / questions_count
    test_total = round(user_questions.coast, RESULT_ROUND)
    rounded_results = tuple(map(
        lambda x: (x[0], round(x[1] * points_per_question, RESULT_ROUND)),
        right_count_dict.items()
    ))
    user_total = round(right_count * points_per_question, RESULT_ROUND)

    dialog_manager.dialog_data["result"] = user_total

    return {
        "results": rounded_results,
        "user_total": user_total,
        "test_total": test_total,
        "back_to_menu_button_text": "Назад в главное меню"
    }
