from typing import Annotated

from aiogram.types import Update
from fastapi import FastAPI, Header

from bot.setup import setup, setup_bot, setup_webhook
from utils.start_broker import start_broker


async def get_app(config, logger) -> FastAPI:
    dp, nc, js, session_maker = await setup(config)
    bot = await setup_bot(config)
    await setup_webhook(bot, config, logger)

    app = FastAPI()

    @app.on_event("startup")
    async def startup():
        try:
            await start_broker(
                nc=nc, js=js,
                config=config,
                cache=dp["cache"],
                session_maker=session_maker,
                bot=bot
            )
        except Exception as e:
            logger.exception(e)

    @app.on_event("shutdown")
    async def shutdown():
        await nc.close()

    @app.post(config.webhook_path)
    async def webhook(
            request: Update,
            secret_token: Annotated[str | None, Header()] = None
    ) -> None | dict:
        """ Register webhook endpoint for telegram bot"""
        if secret_token != config.telegram_secret_token:
            logger.error("Wrong secret token !")
            return {"status": "error", "message": "Wrong secret token!"}
        await dp.feed_webhook_update(bot=bot, update=request)

    return app
