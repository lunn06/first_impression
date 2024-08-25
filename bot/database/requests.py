from typing import Optional

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from bot.configs.questions import Questions
from bot.database import User, UserTest, Test
from bot.database.models import Super, SuperTest


async def prepare_database(session: AsyncSession, questions_dict: dict[str, Questions]):
    for question_name, questions in questions_dict.items():
        test = Test(test_name=question_name, test_type=questions.type)
        session.add(test)

    await session.commit()


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    stmt = select(User).where(User.telegram_id == user_id)

    return await session.scalar(stmt)


async def get_super_by_id(session: AsyncSession, user_id: int) -> Super | None:
    stmt = select(Super).where(Super.telegram_id == user_id)

    return await session.scalar(stmt)


async def get_user_tests(session: AsyncSession, user_id: int) -> list[str]:
    stmt = select(User.tests).where(User.telegram_id == user_id)
    res = await session.execute(stmt)

    user_tests = [r[0] for r in res]

    return user_tests


async def get_admins_ids(session: AsyncSession) -> list[int]:
    stmt = select(Super.telegram_id).where(Super.is_admin)
    res = await session.execute(stmt)

    return [r[0] for r in res]


async def get_moderators_ids(session: AsyncSession) -> list[int]:
    stmt = select(Super.telegram_id).where(Super.is_moderator)
    res = await session.execute(stmt)

    return [r[0] for r in res]


async def get_supers_ids(session: AsyncSession) -> list[User]:
    stmt = select(Super.telegram_id).where(or_(Super.is_moderator, Super.is_admin))
    res = await session.execute(stmt)

    return [r[0] for r in res]


async def get_users_ids(session: AsyncSession) -> list[int]:
    stmt = select(User.telegram_id)
    res = await session.execute(stmt)

    return [r[0] for r in res]


async def get_top_users(session: AsyncSession) -> list[int]:
    stmt = select(User.telegram_id).order_by(User.user_points)
    res = await session.execute(stmt)

    return [r[0] for r in res]


async def get_test_by_name(session: AsyncSession, test_name: str) -> Test | None:
    stmt = select(Test).where(Test.test_name == test_name)

    return await session.scalar(stmt)


async def ensure_super(
        session: AsyncSession,
        user_id: int,
        is_admin: bool = False,
        is_moderator: bool = False,
) -> None:
    super_ = Super(
        telegram_id=user_id,
        is_admin=is_admin,
        is_moderator=is_moderator,
    )
    session.add(super_)

    await session.commit()


async def ensure_user(
        session: AsyncSession,
        user_id: int,
        user_name: Optional[str],
        is_admin: bool = False,
        is_moderator: bool = False,
) -> None:
    existing_user = await get_user_by_id(session, user_id)
    if existing_user is not None:
        return

    user = User(
        telegram_id=user_id,
        user_name=user_name,
    )
    session.add(user)
    await session.commit()

    if is_admin or is_moderator:
        await ensure_super(session, user_id, is_admin, is_moderator)


async def ensure_user_test(session: AsyncSession, user_id: int, test_name: str, test_points: float) -> None:
    existed_user_test = await get_test_by_name(session, test_name)
    if existed_user_test is None:
        return

    user_test = UserTest(telegram_id=user_id, test_name=test_name, test_points=test_points)
    session.add(user_test)
    await session.commit()


async def ensure_super_tests(session: AsyncSession, user_id: int, tests_names: list[str]) -> None:
    for test_name in tests_names:
        existed_user_test = await get_test_by_name(session, test_name)
        if existed_user_test is None:
            return

        user_test = SuperTest(telegram_id=user_id, test_name=test_name)
        session.add(user_test)

    await session.commit()


async def test_connection(session: AsyncSession) -> None:
    stmt = select(1)
    return await session.scalar(stmt)
