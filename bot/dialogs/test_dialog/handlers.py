from aiogram import Bot
from aiogram.types import CallbackQuery, Message, User
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import ManagedMultiselect, Button, Select, Start

from bot import states
from bot.database.requests import ensure_user_test
from bot.dialogs.test_dialog.getters import results_getter
from bot.states import MenuStates, TestStates
from configs import Question, Questions, QuestionsTypeEnum


# TEXT_SLEEP = 1.5

async def on_click_description(
        _callback: CallbackQuery,
        _widget: Button,
        dialog_manager: DialogManager,
):
    event_from_user: User = dialog_manager.middleware_data["event_from_user"]
    questions_json = dialog_manager.start_data["user_questions"]  # type: ignore
    questions = Questions.model_validate_json(questions_json)

    if len(questions) == 0:
        session = dialog_manager.middleware_data["session"]
        test_name = dialog_manager.start_data["dialog_name"]  # type: ignore
        await ensure_user_test(session, event_from_user.id, test_name, questions.coast)
        await dialog_manager.start(MenuStates.menu, mode=StartMode.RESET_STACK)
    else:
        await dialog_manager.switch_to(TestStates.test)


async def ensure_test_handler(
        callback: CallbackQuery,
        _widget: Button,
        manager: DialogManager,
):
    session = manager.middleware_data["session"]
    # cache = manager.middleware_data["cache"]
    test_name = manager.start_data["dialog_name"]  # type: ignore
    result = manager.dialog_data["result"]
    await ensure_user_test(session, callback.from_user.id, test_name, result)


async def on_click_info_button_next(
        callback: CallbackQuery,
        _widget: Button,
        manager: DialogManager,
):
    questions_index = manager.dialog_data.get("question_index", 0)
    questions_json = manager.start_data["user_questions"]  # type: ignore
    questions = Questions.model_validate_json(questions_json)

    manager.start_data["right_answers"][str(questions_index + 1)] = 1  # type: ignore

    manager.dialog_data["question_index"] = questions_index + 1
    if questions_index + 1 == len(questions):
        if not questions.only_info:
            await manager.switch_to(states.TestStates.results)
        else:
            session = manager.middleware_data["session"]
            results = await results_getter(session, manager)
            user_total: float = results["user_total"]
            test_name = manager.start_data["dialog_name"]
            await ensure_user_test(session, callback.from_user.id, test_name, user_total)
            await manager.start(MenuStates.menu, mode=StartMode.RESET_STACK)


async def on_click_multiselect_button_next(
        _callback: CallbackQuery,
        _widget: Button,
        manager: DialogManager,
) -> None:
    manager.show_mode = ShowMode.AUTO

    questions_index = manager.dialog_data.get("question_index", 0)
    questions_json = manager.start_data["user_questions"]  # type: ignore
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
            manager.start_data["right_answers"][str(questions_index + 1)] += 1 / test_right_count  # type: ignore

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
