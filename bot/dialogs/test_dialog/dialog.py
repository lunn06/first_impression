import operator
import random
from copy import deepcopy

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager, StartMode, LaunchMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Multiselect, Select, Button, SwitchTo, Start
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.text import List, Multi

from bot.dialogs.test_dialog.getters import (
    results_getter, description_getter, test_getter
)
from bot.dialogs.test_dialog.handlers import (
    on_click_multiselect_button_next, on_click_select, text_input_handler, ensure_test_handler,
    process_back_to_menu_button, on_click_info_button_next, on_click_description
)
from bot.states import BackToMenuStates, TestStates, MenuStates
from configs import Questions


def get_start_data(questions: Questions) -> dict[str, float]:
    data = {str(i + 1): 0. for i in range(len(questions))}
    return data


async def start_test_handler(
        _callback: CallbackQuery,
        dialog_manager: DialogManager,
        dialog_name: str,
) -> None:
    # session = dialog_manager.middleware_data["session"]
    questions: Questions = dialog_manager.middleware_data["questions_dict"][dialog_name]
    if isinstance(questions.guest_count, int):
        questions_count = questions.guest_count
    else:
        questions_count = len(questions)

    # test = await get_test_by_name(session, dialog_name)
    # assert test

    user_questions = deepcopy(questions)
    user_questions.questions = random.sample(questions.questions, questions_count)

    await dialog_manager.start(
        state=TestStates.description,
        data={
            "dialog_name": dialog_name,
            "user_questions": user_questions.model_dump_json(),
            "right_answers": get_start_data(user_questions),
            "questions_count": questions_count,
            # "points_per_question": questions.coast / questions_count,
            # "points_per_test": questions.coast,
        },
        mode=StartMode.NORMAL,
    )


def get_dialog() -> Dialog:
    description_window = Window(
        Format("{text}"),
        Button(
            Format("{next_text}"),
            id="switch_to_test",
            on_click=on_click_description
        ),

        getter=description_getter,
        state=TestStates.description
    )

    test_window = Window(
        Multi(
            Format("{text}"),
            List(
                Format("{item[0]}. {item[1]}"),
                items="answers",
                when=~F.is_multiselect & ~F.is_select
            ),
            sep="\n\n",
        ),

        Multiselect(
            Format("✓ {item[0]}"),
            Format("{item[0]}"),
            id="multiselect_question",
            item_id_getter=operator.itemgetter(0),
            items="answers",
            when="is_multiselect"
        ),
        Button(
            Format("{button_next_text}"),
            id="multiselect_next_button",
            on_click=on_click_multiselect_button_next,
            when="is_multiselect"
        ),

        Select(
            Format("{item[0]}"),
            id="select_question",
            on_click=on_click_select,
            item_id_getter=operator.itemgetter(0),
            items="answers",
            when="is_select"
        ),

        Button(
            Format("{button_next_text}"),
            id="info_next_button",
            on_click=on_click_info_button_next,
            when="is_info",
        ),

        TextInput(
            id="text_question",
            on_success=text_input_handler,
        ),

        Start(
            Format("{back_to_menu_button_text}"),
            id="back_to_menu_button",
            state=BackToMenuStates.back_to_menu,
            on_click=process_back_to_menu_button,  # type: ignore
            mode=StartMode.NORMAL,
            when=F.is_info
        ),

        state=TestStates.test,
        getter=test_getter
    )

    result_window = Window(
        Multi(
            Const("Результаты теста"),
            List(
                Format("Вопрос {item[0]}: {item[1]}"),
                items="results",
            ),
            Format("Общий счёт: {user_total}/{test_total}"),
            sep="\n\n",
        ),

        Start(
            Format("{back_to_menu_button_text}"),
            id="switch_to_main",
            state=MenuStates.menu,
            on_click=ensure_test_handler,
            mode=StartMode.RESET_STACK
        ),

        state=TestStates.results,
        getter=results_getter
    )

    dialog = Dialog(
        description_window,
        test_window,
        result_window,

        # launch_mode=LaunchMode.SINGLE_TOP
    )

    return dialog
