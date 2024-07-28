from aiogram_dialog import DialogManager

from bot.configs.questions import Questions, QuestionsTypeEnum

RESULT_ROUND = 2


async def description_getter(dialog_manager: DialogManager, **_kwargs):
    questions_json = dialog_manager.start_data["user_questions"]
    questions = Questions.model_validate_json(questions_json)

    return {
        "text": questions.description,
        "next_text": "Начнём!"
    }


async def test_getter(dialog_manager: DialogManager, **_kwargs):
    questions_json = dialog_manager.start_data["user_questions"]
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
    }


async def results_getter(dialog_manager: DialogManager, **_kwargs):
    scores: dict[str, float] = dialog_manager.start_data["scores"]
    test_total = dialog_manager.start_data["points_per_test"]
    rounded_results = tuple(map(lambda x: (x[0], round(x[1], RESULT_ROUND)), scores.items()))
    user_total = round(sum(scores.values()), RESULT_ROUND)

    dialog_manager.dialog_data["result"] = user_total

    return {
        "results": rounded_results,
        "user_total": user_total,
        "test_total": test_total,
        "back_to_menu_button_text": "Назад в главное меню"
    }
