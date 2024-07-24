import operator

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Multiselect, Select, Button, SwitchTo, Start
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.text import List, Multi

from bot import states
from bot.configs.questions import Questions
from bot.dialogs.test_dialog.getters import results_getter, description_getter, \
    test_getter
from bot.dialogs.test_dialog.handlers import (
    on_click_multiselect_button_next, on_click_select, text_input_handler,
)
from bot.states import MenuStates


def get_start_data(questions: Questions) -> dict[int, float]:
    data = {i + 1: 0. for i in range(len(questions))}
    return data


async def start_test_handler(_callback: CallbackQuery, dialog_manager: DialogManager, dialog_name: str):
    questions: Questions = dialog_manager.middleware_data["questions_dict"][dialog_name]

    await dialog_manager.start(
        state=states.TestStates.description,
        data={
            "dialog_name": dialog_name,
            "scores": get_start_data(questions),
            "points_per_question": 10 / len(questions),
            "points_per_test": 10,
        },
        mode=StartMode.NORMAL,
    )


def get_dialog() -> Dialog:
    description_window = Window(
        Format("{text}"),
        SwitchTo(
            Format("{next_text}"),
            id="switch_to_test",
            state=states.TestStates.test
        ),

        getter=description_getter,
        state=states.TestStates.description
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

        TextInput(
            id="text_question",
            on_success=text_input_handler,
        ),

        state=states.TestStates.test,
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
            mode=StartMode.NORMAL
        ),

        state=states.TestStates.results,
        getter=results_getter
    )

    dialog = Dialog(
        description_window,
        test_window,
        result_window,
    )

    return dialog
