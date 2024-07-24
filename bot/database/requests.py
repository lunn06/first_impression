from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.configs.questions import Questions
from bot.database import User, Test


async def prepare_database(session: AsyncSession, questions_dict: dict[str, Questions]):
    for question_name, questions in questions_dict.items():
        test = Test(test_name=question_name, test_type=questions.type)
        session.add(test)
    await session.commit()


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    """
    Получает пользователя по его айди.
    :param session: объект AsyncSession
    :param user_id: айди пользователя
    :return: объект User или None
    """
    stmt = select(User).where(User.telegram_id == user_id)
    return await session.scalar(stmt)


async def get_test_by_name(session: AsyncSession, test_name: str) -> Test | None:
    stmt = select(Test).where(Test.test_name == test_name)
    return await session.scalar(stmt)


async def ensure_user(session: AsyncSession, user_id: int, user_name: str):
    """
    Создаёт пользователя, если его раньше не было
    :param session: объект AsyncSession
    :param user_id: айди пользователя
    :param user_name: ну ты понял
    """
    existing_user = await get_user_by_id(session, user_id)
    if existing_user is not None:
        return
    user = User(telegram_id=user_id, user_name=user_name)
    session.add(user)
    await session.commit()


async def test_connection(session: AsyncSession):
    """
    Проверка соединения с СУБД
    :param session: объект AsyncSession
    """
    stmt = select(1)
    return await session.scalar(stmt)
