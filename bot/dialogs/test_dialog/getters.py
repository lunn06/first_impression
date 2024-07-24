from aiogram_dialog import DialogManager

from bot.configs.questions import Questions, QuestionsTypeEnum


async def description_getter(questions_dict: dict[str, Questions], dialog_manager: DialogManager, **_kwargs):
    questions_name = dialog_manager.start_data["dialog_name"]
    questions = questions_dict[questions_name]

    return {
        "text": questions.description,
        "next_text": "Начнём!"
    }


async def test_getter(questions_dict: dict[str, Questions], dialog_manager: DialogManager, **_kwargs):
    questions_name = dialog_manager.start_data["dialog_name"]
    questions = questions_dict[questions_name]
    question_index: int = dialog_manager.dialog_data.get("question_index", 0)

    current_question = questions[question_index]

    return {
        "text": current_question.text,
        "button_next_text": "Дальше",
        "answers": [(i + 1, a) for i, a in enumerate(current_question.answers)],
        "question_index": question_index,
        "is_multiselect": current_question.type == QuestionsTypeEnum.multiselect,
        "is_select": current_question.type == QuestionsTypeEnum.select,
        "is_text": current_question.type == QuestionsTypeEnum.text,
    }


async def results_getter(dialog_manager: DialogManager, **_kwargs):
    scores: dict[str, float] = dialog_manager.start_data["scores"]
    test_total = dialog_manager.start_data["points_per_test"]

    return {
        "results": list(scores.items()),
        "user_total": sum(scores.values()),
        "test_total": test_total,
        "back_to_menu_button_text": "Назад в главное меню"
    }
