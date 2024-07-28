from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.configs.questions import Questions
from bot.database import User, UserTest, Test


async def prepare_database(session: AsyncSession, questions_dict: dict[str, Questions]):
    for question_name, questions in questions_dict.items():
        test = Test(test_name=question_name, test_type=questions.type)
        session.add(test)

    await session.commit()


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    stmt = select(User).where(User.telegram_id == user_id)

    return await session.scalar(stmt)


async def get_user_tests(session: AsyncSession, user_id: int) -> list[str]:
    stmt = select(UserTest.test_name).where(UserTest.telegram_id == user_id)
    res = await session.execute(stmt)

    return [r[0] for r in res]


async def get_users_ids(session: AsyncSession) -> list[int]:
    stmt = select(User.telegram_id)
    res = await session.execute(stmt)

    return [r[0] for r in res]


async def get_test_by_name(session: AsyncSession, test_name: str) -> Test | None:
    stmt = select(Test).where(Test.test_name == test_name)

    return await session.scalar(stmt)


async def ensure_user(session: AsyncSession, user_id: int, user_name: str) -> None:
    existing_user = await get_user_by_id(session, user_id)
    if existing_user is not None:
        return

    user = User(telegram_id=user_id, user_name=user_name)
    session.add(user)
    await session.commit()


async def ensure_user_test(session: AsyncSession, user_id: int, test_name: str, test_points: float) -> None:
    existed_user_test = await get_test_by_name(session, test_name)
    if existed_user_test is not None:
        return

    user_test = UserTest(telegram_id=user_id, test_name=test_name, test_points=test_points)
    session.add(user_test)
    await session.commit()


async def test_connection(session: AsyncSession) -> None:
    stmt = select(1)
    return await session.scalar(stmt)
