from aiogram import Router

from bot.handlers import commands


def get_routers() -> tuple[Router]:
    return (
        commands.router,
    )
