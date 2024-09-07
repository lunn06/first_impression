from aiogram import Bot
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import ManagedMultiselect, Button, Select, Start

from bot import states
from bot.database.requests import ensure_user_test
from configs import Question, Questions, QuestionsTypeEnum


# TEXT_SLEEP = 1.5


async def ensure_test_handler(
        callback: CallbackQuery,
        _widget: Button,
        manager: DialogManager,
):
    session = manager.middleware_data["session"]
    # cache = manager.middleware_data["cache"]
    test_name = manager.start_data["dialog_name"]
    result = manager.dialog_data["result"]
    await ensure_user_test(session, callback.from_user.id, test_name, result)


async def on_click_multiselect_button_next(
        _callback: CallbackQuery,
        _widget: Button,
        manager: DialogManager,
) -> None:
    manager.show_mode = ShowMode.AUTO

    questions_index = manager.dialog_data.get("question_index", 0)
    questions_json = manager.start_data["user_questions"]
    questions = Questions.model_validate_json(questions_json)
    current_question: Question = questions[questions_index]

    managed_multiselect: ManagedMultiselect = manager.find("multiselect_question")  # type: ignore
    assert isinstance(managed_multiselect, ManagedMultiselect)

    checked = map(
        lambda x: current_question.answers[int(x) - 1],
        managed_multiselect.get_checked()
    )

    test_right_count = len(current_question.right_answers)
    for right_answer in current_question.right_answers:
        if right_answer in checked:
            manager.start_data["right_answers"][str(questions_index + 1)] += 1 / test_right_count

    manager.dialog_data["question_index"] = questions_index + 1
    if questions_index + 1 == len(questions):
        await manager.switch_to(states.TestStates.results)


async def on_click_select(
        _callback: CallbackQuery,
        _widget: Select,
        manager: DialogManager,
        clicked_item: str
) -> None:
    manager.show_mode = ShowMode.AUTO

    questions_index = manager.dialog_data.get("question_index", 0)
    questions_json = manager.start_data["user_questions"]
    questions = Questions.model_validate_json(questions_json)
    current_question: Question = questions[questions_index]

    user_answer = current_question.answers[int(clicked_item) - 1]
    if user_answer == current_question.right_answers[0]:
        # points_per_question = manager.start_data["points_per_question"]
        # manager.start_data["scores"][str(questions_index + 1)] += points_per_question
        manager.start_data["right_answers"][str(questions_index + 1)] = 1

    manager.dialog_data["question_index"] = questions_index + 1
    if questions_index + 1 == len(questions):
        await manager.switch_to(states.TestStates.results)


async def text_input_handler(
        message: Message,
        _text_input: ManagedTextInput,
        manager: DialogManager,
        text: str
) -> None:
    manager.show_mode = ShowMode.EDIT

    questions_index = manager.dialog_data.get("question_index", 0)
    questions_json = manager.start_data["user_questions"]
    questions = Questions.model_validate_json(questions_json)
    current_question: Question = questions[questions_index]

    if current_question.type != QuestionsTypeEnum.text:
        await message.delete()
        return

    if text.lower().strip() == current_question.right_answers[0].lower():
        # points_per_question = manager.start_data["points_per_question"]
        # manager.start_data["scores"][str(questions_index + 1)] += points_per_question
        manager.start_data["right_answers"][str(questions_index + 1)] = 1

    bot: Bot = manager.middleware_data["bot"]
    await bot.delete_message(message.from_user.id, message.message_id)  # type: ignore

    manager.dialog_data["question_index"] = questions_index + 1

    if questions_index + 1 == len(questions):
        await manager.switch_to(states.TestStates.results)


async def process_back_to_menu_button(
        _callback: CallbackQuery,
        start_widget: Start,
        manager: DialogManager,
):
    start_widget.start_data = manager.start_data
