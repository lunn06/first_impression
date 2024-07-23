import operator
from typing import Any

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager, ShowMode
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Multiselect, Select, Button
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.text import List, Multi

from bot import states
from bot.configs.questions import Questions, QuestionsTypeEnum
from bot.dialogs.test_dialog.getters import get_test_getter
from bot.dialogs.test_dialog.handlers import (
    get_on_click_multiselect_button_next,
    get_text_input_handler,
    get_on_click_select,
)


def get_start_data(questions: Questions) -> dict[int, float]:
    data = {i: 0. for i in range(len(questions))}
    return data


def get_start_test_handler(dialog_name: str) -> Any:
    async def start_test_handler(_callback: CallbackQuery, dialog_manager: DialogManager):
        questions: Questions = dialog_manager.middleware_data["questions_dict"][dialog_name]
        if questions[0].type == QuestionsTypeEnum.select:
            start_state = states.TestStates.select_question
        elif questions[0].type == QuestionsTypeEnum.multiselect:
            start_state = states.TestStates.multiselect_question
        else:
            start_state = states.TestStates.text_question

        print(start_state)
        await dialog_manager.start(
            state=start_state,
            data=get_start_data(questions),
            show_mode=ShowMode.AUTO
        )

    return start_test_handler


def get_dialog(dialog_name: str) -> Dialog:
    multiselect_window = Window(
        Multi(
            Format("{text}"),
            List(
                Format("{item[0]}. {item[1]}"),
                items="answers",
                # when=F.is_multiselect | F.is_select
            ),
            sep="\n\n",
        ),

        Multiselect(
            Format("✓ {item[0]}"),
            Format("{item[0]}"),
            id=f"{dialog_name}_multiselect_question",
            # on_state_changed=on_multiselect_state_change,
            item_id_getter=operator.itemgetter(0),
            items="answers",
            # when="is_multiselect"
        ),
        Button(
            Format("{button_next_text}"),
            id=f"{dialog_name}_multiselect_next_button",
            on_click=get_on_click_multiselect_button_next(dialog_name),
            # when="is_multiselect"
        ),

        state=states.TestStates.multiselect_question,
        getter=get_test_getter(dialog_name)
    )

    text_window = Window(
        Format("{text}"),

        TextInput(
            id=f"{dialog_name}_text_question",
            on_success=get_text_input_handler(dialog_name),
            # on_error=get_text_input_handler(dialog_name),
        ),
        MessageInput(
            func=get_text_input_handler(dialog_name)
        ),

        state=states.TestStates.text_question,
        getter=get_test_getter(dialog_name)
    )

    select_window = Window(
        Multi(
            Format("{text}"),
            List(
                Format("{item[0]}. {item[1]}"),
                items="answers",
                # when=F.is_multiselect | F.is_select
            ),
            sep="\n\n",
        ),

        Select(
            Format("{item[0]}"),
            id=f"{dialog_name}_select_question",
            on_click=get_on_click_select(dialog_name),
            item_id_getter=operator.itemgetter(0),
            items="answers",
            # when="is_select"
        ),

        state=states.TestStates.select_question,
        getter=get_test_getter(dialog_name)
    )
    # result_window = Window()

    dialog = Dialog(
        multiselect_window,
        select_window,
        text_window,
        # result_window,
        name=dialog_name
    )

    return dialog
