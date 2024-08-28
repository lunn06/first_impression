import operator

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Select, Multiselect, ScrollingGroup, Button, Cancel, SwitchTo
from aiogram_dialog.widgets.text import Format

from bot.dialogs.admin.ensure_user.getters import (
    select_super_type_getter,
    ensure_super_getter,
    choose_tests_getter
)
from bot.dialogs.admin.ensure_user.handlers import (
    telegram_user_name_validator,
    select_super_type_handler,
    super_id_on_success,
    super_id_on_error,
    process_choose_button_handler
)
from bot.states import EnsureSuperStates


def get_dialog() -> Dialog:
    choose_type_window = Window(
        Format("{choose_super_type_text}"),

        Select(
            Format("{item[1]}"),
            id="select_super_type",
            on_click=select_super_type_handler,
            item_id_getter=operator.itemgetter(0),
            items="super_types",
        ),
        Cancel(
            Format("{cancel_button_text}")
        ),
        getter=select_super_type_getter,
        state=EnsureSuperStates.choose_type,
    )

    ensure_super_window = Window(
        Format("{ensure_super_text}"),
        TextInput(
            type_factory=telegram_user_name_validator,
            on_success=super_id_on_success,
            on_error=super_id_on_error,

            id="ensure_super_text_input",
        ),
        SwitchTo(
            Format("{back_button_text}"),
            state=EnsureSuperStates.choose_type,
            id="back_to_ensure_super",
        ),
        getter=ensure_super_getter,
        state=EnsureSuperStates.ensure_super
    )

    choose_tests_window = Window(
        Format("{choose_tests_text}"),

        ScrollingGroup(
            Multiselect(
                Format("✅ {item[1]}"),  # тут зелёная галочка в начале строки
                Format("{item[1]}"),
                id="choose_tests_multiselect",
                item_id_getter=operator.itemgetter(0),
                items="tests",
            ),
            width=1,
            height=5,
            id="choose_tests_scrolling",
        ),

        Button(
            Format("{process_choose_button_text}"),
            id="process_choose_button",
            on_click=process_choose_button_handler,
        ),

        SwitchTo(
            Format("{back_button_text}"),
            state=EnsureSuperStates.ensure_super,
            id="back_to_ensure_super",
        ),

        getter=choose_tests_getter,
        state=EnsureSuperStates.choose_tests
    )

    return Dialog(
        choose_type_window,
        ensure_super_window,
        choose_tests_window,
    )
