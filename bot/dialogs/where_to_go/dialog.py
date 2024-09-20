import operator

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel, ScrollingGroup, Select, SwitchTo, Group
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.where_to_go.getters import locations_getter, audiences_getter, description_getter, types_or_map_getter
from bot.dialogs.where_to_go.handlers import select_locations_on_click, select_audience_on_click, select_types_on_click
from bot.states import WhereToGoStates


def get_dialog() -> Dialog:
    types_or_map_window = Window(
        Format("{map_text}"),
        DynamicMedia(
            "map",
            when="is_map_mode"
        ),

        Format("{buttons_text}", when="is_buttons_mode"),
        Group(
            Select(
                Format("{item[1]}"),
                items="types",
                item_id_getter=operator.itemgetter(0),
                id="select_types",
                on_click=select_types_on_click
            ),
            width=2,
            when="is_buttons_mode"
        ),

        Cancel(
            Format("{back_to_menu_button_text}"),
            id="back_to_menu",
        ),

        getter=types_or_map_getter,
        state=WhereToGoStates.types_or_map,
    )

    locations_window = Window(
        Format("{text}"),

        ScrollingGroup(
            Select(
                Format("{item[1]}"),
                items="locations",
                item_id_getter=operator.itemgetter(0),
                id="select_locations",
                on_click=select_locations_on_click
            ),
            width=1,
            height=5,
            id="scrolling_locations"
        ),

        SwitchTo(
            Const("Назад"),
            id="back_to_types",
            state=WhereToGoStates.types_or_map,
            # mode=StartMode.RESET_STACK,
        ),

        getter=locations_getter,
        state=WhereToGoStates.locations,
    )

    audiences_window = Window(
        Format("{text}"),

        ScrollingGroup(
            Select(
                Format("{item[1]}"),
                items="audiences",
                item_id_getter=operator.itemgetter(0),
                on_click=select_audience_on_click,
                id="select_where_to_go",
            ),
            width=1,
            height=5,
            id="scrolling_where_to_go"
        ),

        SwitchTo(
            Format("{back_to_locations_button_text}"),
            id="back_to_locations",
            state=WhereToGoStates.locations,
        ),

        getter=audiences_getter,
        state=WhereToGoStates.audiences,
    )

    description_window = Window(
        Format("{text}"),
        SwitchTo(
            Format("{back_button_text}"),
            id="back_to_locations",
            state=WhereToGoStates.audiences
        ),

        getter=description_getter,
        state=WhereToGoStates.description
    )

    dialog = Dialog(
        types_or_map_window,
        locations_window,
        audiences_window,
        description_window,
    )

    return dialog
