import asyncio
from typing import Any

from aiogram import Bot
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import ManagedMultiselect, Button, Select

from bot import states
from bot.configs.questions import Question, Questions

TEXT_SLEEP = 1.5


def get_on_click_multiselect_button_next(dialog_name: str) -> Any:
    async def on_click_multiselect_button_next(
            callback: CallbackQuery,
            _widget: Button,
            manager: DialogManager,
            # clicked_item: str
    ) -> None:
        questions_index = manager.dialog_data.get("question_index", 0)
        questions: Questions = manager.middleware_data["questions_dict"][dialog_name]
        current_question: Question = questions[questions_index]

        managed_multiselect: ManagedMultiselect = manager.find(f"{dialog_name}_multiselect_question")  # type: ignore
        assert isinstance(managed_multiselect, ManagedMultiselect)

        sorted_checked = sorted(
            map(
                lambda x: current_question.answers[int(x) - 1],
                managed_multiselect.get_checked()
            )
        )

        if sorted_checked == current_question.right_answers:
            manager.dialog_data["question_index"] = questions_index + 1

            if questions_index + 1 == len(questions):
                await manager.switch_to(states.TestStates.results)
        else:
            await callback.answer("Неверный ответ")  # type: ignore

    return on_click_multiselect_button_next


def get_on_click_select(dialog_name: str) -> Any:
    async def on_click_select(
            callback: CallbackQuery,
            _widget: Select,
            manager: DialogManager,
            clicked_item: str
    ) -> None:
        questions_index = manager.dialog_data.get("question_index", 0)
        questions: Questions = manager.middleware_data["questions_dict"][dialog_name]
        current_question: Question = questions[questions_index]

        user_answer = current_question.answers[int(clicked_item) - 1]
        if user_answer == current_question.right_answers[0]:
            manager.dialog_data["question_index"] = questions_index + 1

            if questions_index + 1 == len(questions):
                await manager.switch_to(states.TestStates.results)
        else:
            await callback.answer("Неверный ответ")  # type: ignore

    return on_click_select


def get_text_input_handler(dialog_name: str) -> Any:
    async def text_input_handler(
            message: Message,
            _text_input: ManagedTextInput,
            manager: DialogManager,
            text: str
    ) -> None:
        questions_index = manager.dialog_data.get("question_index", 0)
        questions: Questions = manager.middleware_data["questions_dict"][dialog_name]
        current_question: Question = questions[questions_index]

        wrong_answer = False
        if text.lower().strip() == current_question.right_answers[0].lower():
            manager.dialog_data["question_index"] = questions_index + 1

            if questions_index + 1 == len(questions):
                await manager.switch_to(states.TestStates.results)
        else:
            wrong_answer = True
            await message.answer("Неверный ответ")  # type: ignore

        bot: Bot = manager.middleware_data["bot"]
        if wrong_answer:
            to_delete_messages = list(range(message.message_id - 1, message.message_id + 2))
        else:
            to_delete_messages = list(range(message.message_id - 1, message.message_id + 1))

        await asyncio.sleep(TEXT_SLEEP)
        await bot.delete_messages(message.from_user.id, to_delete_messages)  # type: ignore

    return text_input_handler
