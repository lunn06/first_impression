from __future__ import annotations

from typing import Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.dialects.mysql import BIGINT, TIMESTAMP, BOOLEAN
from sqlalchemy.orm import Mapped, mapped_column

from bot.database.base import Base


class User(Base):
    __tablename__ = "users"
    telegram_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True
    )
    user_name: Mapped[Optional[str]] = mapped_column(
        nullable=True
    )
    registered_at: Mapped[int] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    user_points: Mapped[float] = mapped_column(
        nullable=False,
        default=0.
    )

    # super_id: Mapped[Optional[int]] = mapped_column(
    #     ForeignKey("supers.super_id")
    # )

    # tests: Mapped[list[UserTest]] = relationship(back_populates="user")
    # super_: Mapped[Optional[Super]] = relationship(back_populates="user", viewonly=True)


class Super(Base):
    __tablename__ = "supers"
    # super_id: Mapped[int] = mapped_column(
    #     primary_key=True,
    #     autoincrement=True,
    # )

    telegram_id: Mapped[int] = mapped_column(
        ForeignKey(User.telegram_id),
        primary_key=True,
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

    # user: Mapped[User] = relationship(back_populates="super_", viewonly=True)
    # tests: Mapped[list[SuperTest]] = relationship(back_populates="super_", viewonly=True)


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

    # users: Mapped[list[UserTest]] = relationship(back_populates="test")
    # supers: Mapped[list[SuperTest]] = relationship(back_populates="test")


class SuperTest(Base):
    __tablename__ = "super_tests"
    super_id: Mapped[int] = mapped_column(
        ForeignKey(Super.telegram_id),
        primary_key=True
    )
    test_name: Mapped[str] = mapped_column(
        ForeignKey(Test.test_name),
        primary_key=True
    )

    # super_: Mapped[Super] = relationship(back_populates="tests")
    # test: Mapped[Test] = relationship(back_populates="supers")


class UserTest(Base):
    __tablename__ = "user_tests"
    telegram_id: Mapped[int] = mapped_column(
        ForeignKey(User.telegram_id),
        primary_key=True
    )
    test_name: Mapped[str] = mapped_column(
        ForeignKey(Test.test_name),
        primary_key=True
    )
    completed_at: Mapped[int] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    test_points: Mapped[float] = mapped_column(
        default=0.,
        nullable=False
    )

    # user: Mapped[User] = relationship(back_populates="tests")
    # test: Mapped[Test] = relationship(back_populates="users")
