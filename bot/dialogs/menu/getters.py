from typing import TYPE_CHECKING

from aiogram.enums import ContentType
from aiogram.types import User
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import User as DBUser
from bot.database.requests import get_supers_ids, get_user_by_id, get_user_tests
from configs import Questions, Config

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner


async def menu_getter(
        dialog_manager: DialogManager,
        session: AsyncSession,
        i18n: TranslatorRunner,
        questions_dict: dict[str, Questions],
        config: Config,
        **_kwargs
):
    user: User = dialog_manager.middleware_data['event_from_user']
    db_user: DBUser | None = await get_user_by_id(session, user.id)
    assert db_user
    user_tests = await get_user_tests(session, user.id)

    supers_ids = await get_supers_ids(session)
    user_points = str(int(db_user.user_points))
    len_user_tests = str(len(user_tests))
    len_total_test = str(len(questions_dict))

    text = i18n.menu.message(
        points=user_points,
        user_tests=len_user_tests,
        total_tests=len_total_test,
    )

    pic_attachment = None
    if config.menu_pic is not None:
        pic_attachment = MediaAttachment(ContentType.PHOTO, path=str(config.menu_pic))

    return {
        "text": text,
        "start_admin_button": "Панель",
        "start_statistics_button": i18n.statistics.button(),
        "start_secrets_button": i18n.secrets.button(),
        "start_where_to_go_button": i18n.wheretogo.button(),
        "is_super": user.id in supers_ids,

        "pic": pic_attachment,
    }
