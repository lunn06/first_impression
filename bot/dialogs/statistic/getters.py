from typing import TYPE_CHECKING

from aiogram.enums import ContentType
from aiogram.types import User
from aiogram_dialog.api.entities import MediaAttachment
from fluentogram import TranslatorRunner
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.cached_requests import get_top_users
from bot.database.requests import get_user_tests
from configs import Config, Questions

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner


async def statistics_getter(i18n: TranslatorRunner, **_kwargs):
    return {
        "text": "Какие метрики смотрим?",
        "top_users_text": i18n.top.users.button(),
        "user_tests_text": i18n.user.tests.button(),
        "back_to_menu_button_text": i18n.back.to.menu.button(),
    }


async def top_users_getter(cache: Redis, i18n: TranslatorRunner, config: Config, **_kwargs):
    top_users, last_top = await get_top_users(cache)
    minutes = last_top.minute if last_top.minute > 9 else "0" + str(last_top.minute)
    last_top_str = f"{last_top.date()} {last_top.hour}:{minutes}"

    pic_attachment = None
    if config.top_users_pic is not None:
        pic_attachment = MediaAttachment(ContentType.PHOTO, path=str(config.top_users_pic))

    return {
        "last_top": last_top_str,
        "top_users": tuple((i + 1, v[0], v[1]) for i, v in enumerate(top_users)),

        "back_button_text": i18n.back.section.button(),
        "pic": pic_attachment,
    }


async def user_tests_getter(
        session: AsyncSession,
        questions_dict: dict[str, Questions],
        event_from_user: User,
        i18n: TranslatorRunner,
        **_kwargs
):
    user_tests = await get_user_tests(session, event_from_user.id)
    user_tests_str = [test.test_name for test in user_tests]
    tests = [
        i18n.user.test(
            test_name=questions_dict[test].name,
            is_complete="true" if test in user_tests_str else "false"
        ) for test in questions_dict.keys()
    ]

    return {
        "text": "Твои тесты:",
        "tests": enumerate(tests),
        "back_button_text": i18n.back.section.button(),
    }
