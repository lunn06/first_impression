import operator

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import ScrollingGroup, Multiselect, Button, Cancel
from aiogram_dialog.widgets.text import Format

from bot.dialogs.admin.delete_user.getters import delete_super_getter
from bot.dialogs.admin.delete_user.handlers import process_delete_super_handler
from bot.states import DeleteSuperStates


def get_dialog() -> Dialog:
    delete_super_window = Window(
        Format("{delete_super_text}"),

        ScrollingGroup(
            Multiselect(
                Format("✅ {item[1]}"),  # тут зелёная галочка в начале строки
                Format("{item[1]}"),
                id="delete_super_multiselect",
                item_id_getter=operator.itemgetter(0),
                items="supers",
            ),
            width=1,
            height=5,
            id="delete_super_scrolling",
        ),

        Button(
            Format("{process_delete_super_text}"),
            id="delete_super_button",
            on_click=process_delete_super_handler,
        ),

        Cancel(
            Format("{back_button_text}"),
            id="back_to_menu",
        ),

        getter=delete_super_getter,
        state=DeleteSuperStates.delete_super,
    )

    return Dialog(
        delete_super_window
    )
