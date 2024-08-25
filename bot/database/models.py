from __future__ import annotations

from sqlalchemy import ForeignKey, text
from sqlalchemy.dialects.mysql import BIGINT, TIMESTAMP, BOOLEAN
from sqlalchemy.orm import Mapped, mapped_column, relationship

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
    return text('CURRENT_TIMESTAMP')


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

    tests: Mapped[list[UserTest]] = relationship(back_populates="user")


class Super(Base):
    __tablename__ = "supers"
    telegram_id: Mapped[int] = mapped_column(
        ForeignKey("users.telegram_id"),
        primary_key=True
    )
    is_admin: Mapped[bool] = mapped_column(
        BOOLEAN,
        nullable=False,
        default=False,
    )
    is_moderator: Mapped[bool] = mapped_column(
        BOOLEAN,
        nullable=False,
        default=False
    )

    tests: Mapped[list[SuperTest]] = relationship(back_populates="super")


class Test(Base):
    __tablename__ = "tests"
    # test_id: Mapped[int] = mapped_column(
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

    users: Mapped[list[UserTest]] = relationship(back_populates="test")
    supers: Mapped[list[SuperTest]] = relationship(back_populates="test")


class SuperTest(Base):
    __tablename__ = "super_tests"
    telegram_id: Mapped[int] = mapped_column(
        ForeignKey("supers.telegram_id"),
        primary_key=True
    )
    test_name: Mapped[str] = mapped_column(
        ForeignKey("tests.test_name"),
        primary_key=True
    )

    super: Mapped[Super] = relationship(back_populates="tests")
    test: Mapped[Test] = relationship(back_populates="supers")


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

    user: Mapped[User] = relationship(back_populates="tests")
    test: Mapped[Test] = relationship(back_populates="users")
