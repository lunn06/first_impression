from typing import Any

from aiogram_dialog import DialogManager

from bot.configs.questions import Questions, QuestionsTypeEnum


def get_test_getter(questions_name: str) -> Any:
    async def test_getter(questions_dict: dict[str, Questions], dialog_manager: DialogManager, **_kwargs):
        questions = questions_dict[questions_name]
        question_index: int = dialog_manager.dialog_data.get("question_index", 0)

        current_question = questions[question_index]

        return {
            "text": current_question.text,
            "button_next_text": "Дальше",
            "answers": [(i+1, a) for i, a in enumerate(current_question.answers)],
            "question_index": question_index,
            "is_multiselect": current_question.type == QuestionsTypeEnum.multiselect,
            "is_select": current_question.type == QuestionsTypeEnum.select,
            "is_text": current_question.type == QuestionsTypeEnum.text,
        }

    return test_getter
