import asyncio

from aiogram import Bot
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import ManagedMultiselect, Button, Select

from bot import states
from bot.configs.questions import Question, Questions, QuestionsTypeEnum

TEXT_SLEEP = 1.5


async def on_click_multiselect_button_next(
        callback: CallbackQuery,
        _widget: Button,
        manager: DialogManager,
) -> None:
    manager.show_mode = ShowMode.AUTO

    dialog_name = manager.start_data["dialog_name"]
    questions_index = manager.dialog_data.get("question_index", 0)
    questions: Questions = manager.middleware_data["questions_dict"][dialog_name]
    current_question: Question = questions[questions_index]

    managed_multiselect: ManagedMultiselect = manager.find("multiselect_question")  # type: ignore
    assert isinstance(managed_multiselect, ManagedMultiselect)

    sorted_checked = sorted(
        map(
            lambda x: current_question.answers[int(x) - 1],
            managed_multiselect.get_checked()
        )
    )

    if sorted_checked == current_question.right_answers:
        tries = manager.dialog_data.get("tries", 0)
        points_per_question = manager.start_data["points_per_question"]
        if tries == 0:
            manager.start_data["scores"][str(questions_index + 1)] += points_per_question
        else:
            manager.start_data["scores"][str(questions_index + 1)] += points_per_question / 2

        manager.dialog_data["question_index"] = questions_index + 1
        manager.dialog_data["tries"] = 0

        if questions_index + 1 == len(questions):
            await manager.switch_to(states.TestStates.results)
    else:
        tries = manager.dialog_data.get("tries", 0)
        manager.dialog_data["tries"] = tries + 1
        await callback.answer("Неверный ответ")  # type: ignore


async def on_click_select(
        callback: CallbackQuery,
        _widget: Select,
        manager: DialogManager,
        clicked_item: str
) -> None:
    manager.show_mode = ShowMode.AUTO

    dialog_name = manager.start_data["dialog_name"]
    questions_index = manager.dialog_data.get("question_index", 0)
    questions: Questions = manager.middleware_data["questions_dict"][dialog_name]
    current_question: Question = questions[questions_index]

    user_answer = current_question.answers[int(clicked_item) - 1]
    if user_answer == current_question.right_answers[0]:
        tries = manager.dialog_data.get("tries", 0)
        points_per_question = manager.start_data["points_per_question"]
        print(manager.start_data)
        if tries == 0:
            manager.start_data["scores"][str(questions_index + 1)] += points_per_question
        else:
            manager.start_data["scores"][str(questions_index + 1)] += points_per_question / 2

        manager.dialog_data["question_index"] = questions_index + 1
        manager.dialog_data["tries"] = 0

        if questions_index + 1 == len(questions):
            await manager.switch_to(states.TestStates.results)
    else:
        tries = manager.dialog_data.get("tries", 0)
        manager.dialog_data["tries"] = tries + 1
        await callback.answer("Неверный ответ")  # type: ignore


async def text_input_handler(
        message: Message,
        _text_input: ManagedTextInput,
        manager: DialogManager,
        text: str
) -> None:
    manager.show_mode = ShowMode.EDIT

    dialog_name = manager.start_data["dialog_name"]
    questions_index = manager.dialog_data.get("question_index", 0)
    questions: Questions = manager.middleware_data["questions_dict"][dialog_name]
    current_question: Question = questions[questions_index]

    if current_question.type != QuestionsTypeEnum.text:
        await message.delete()
        return

    wrong_answer = False
    if text.lower().strip() == current_question.right_answers[0].lower():
        tries = manager.dialog_data.get("tries", 0)
        points_per_question = manager.start_data["points_per_question"]
        if tries == 0:
            manager.start_data["scores"][str(questions_index + 1)] += points_per_question
        else:
            manager.start_data["scores"][str(questions_index + 1)] += points_per_question / 2

        manager.dialog_data["question_index"] = questions_index + 1
        manager.dialog_data["tries"] = 0

        if questions_index + 1 == len(questions):
            await manager.switch_to(states.TestStates.results)
    else:
        wrong_answer = True
        tries = manager.dialog_data.get("tries", 0)
        manager.dialog_data["tries"] = tries + 1
        await message.answer("Неверный ответ")  # type: ignore

    bot: Bot = manager.middleware_data["bot"]

    to_delete_messages = [message.message_id]
    if wrong_answer:
        to_delete_messages += [message.message_id + 1]

    await asyncio.sleep(TEXT_SLEEP)
    await bot.delete_messages(message.from_user.id, to_delete_messages)  # type: ignore
