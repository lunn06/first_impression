from __future__ import annotations

import decimal
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
    user_points: Mapped[decimal.Decimal] = mapped_column(
        nullable=False,
        default=0.
    )


class Super(Base):
    __tablename__ = "supers"

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


class Test(Base):
    __tablename__ = "tests"
    test_name: Mapped[str] = mapped_column(
        primary_key=True,
        nullable=False
    )
    test_type: Mapped[str] = mapped_column(
        nullable=False
    )
    complete_count: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
    )


class SuperTest(Base):
    __tablename__ = "super_tests"
    telegram_id: Mapped[int] = mapped_column(
        ForeignKey(Super.telegram_id),
        primary_key=True
    )
    test_name: Mapped[str] = mapped_column(
        ForeignKey(Test.test_name),
        primary_key=True
    )


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
