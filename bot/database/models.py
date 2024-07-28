from sqlalchemy import ForeignKey, text
from sqlalchemy.dialects.mysql import BIGINT, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from bot.database.base import Base


# class utcnow(expression.FunctionElement):
#     type = DateTime()
#     inherit_cache = True
# 
# 
# @compiles(utcnow, 'mysql')
# def mysql_utcnow(_element, _compiler, **_kwargs):
#     return "text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')"

def utcnow():
    return text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')


class User(Base):
    __tablename__ = "users"
    telegram_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True
    )
    user_name: Mapped[str] = mapped_column(
        nullable=True
    )
    registered_at: Mapped[int] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=utcnow()
    )
    user_points: Mapped[float] = mapped_column(
        nullable=False,
        default=0.
    )
    is_admin: Mapped[bool] = mapped_column(
        nullable=False,
        default=False
    )


class Test(Base):
    __tablename__ = "tests"
    # test_id: Mapped[int] = mapped_column(
    #     INTEGER,
    #     primary_key=True,
    #     autoincrement=True,
    # )
    test_name: Mapped[str] = mapped_column(
        primary_key=True,
        nullable=False
    )
    test_type: Mapped[str] = mapped_column(
        nullable=False
    )


class UserTest(Base):
    __tablename__ = "user_tests"
    telegram_id: Mapped[int] = mapped_column(
        ForeignKey("users.telegram_id"),
        primary_key=True
    )
    test_name: Mapped[str] = mapped_column(
        ForeignKey("tests.test_name"),
        primary_key=True
    )
    completed_at: Mapped[int] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=utcnow()
    )
    test_points: Mapped[float] = mapped_column(
        default=0.,
        nullable=False
    )
