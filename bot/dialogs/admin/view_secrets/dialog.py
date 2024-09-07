import operator

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Button, SwitchTo, Cancel
from aiogram_dialog.widgets.text import Format, Multi

from bot.dialogs.admin.view_secrets.getters import user_secrets_getter, view_secret_getter
from bot.dialogs.admin.view_secrets.handlers import select_user_secrets_on_click
from bot.states import ViewSecretsStates


def get_dialog() -> Dialog:
    user_secrets_window = Window(
        Format("{text}"),

        ScrollingGroup(
            Select(
                Format("{item[1]}"),
                items="user_secrets",
                item_id_getter=operator.itemgetter(0),
                on_click=select_user_secrets_on_click,
                id="select_user_secrets",
            ),
            id="scrolling_user_secrets",
            width=1,
            height=5,
        ),
        Cancel(
            Format("{back_button_text}")
        ),
        getter=user_secrets_getter,
        state=ViewSecretsStates.user_secrets,
    )

    view_secret_window = Window(
        Multi(
            Format("{name}"),
            Format("{interval}"),
            Format("{count}"),
            Format("{totp}"),
            Format("{location}"),
            Format("{audience}"),

            sep="\n\n"
        ),
        Button(
            Format("{update_button_text}"),
            id="update_secret_button",
        ),
        SwitchTo(
            Format("{back_button_text}"),
            id="back_to_user_secrets",
            state=ViewSecretsStates.user_secrets,
        ),

        getter=view_secret_getter,
        state=ViewSecretsStates.view_secret,
    )

    return Dialog(
        user_secrets_window,
        view_secret_window
    )
