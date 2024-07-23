from typing import Annotated

from aiogram.types import Update
from fastapi import FastAPI, Header

from bot.setup import setup_dp, setup_bot, setup_webhook


async def get_app(config, logger) -> FastAPI:
    dp = await setup_dp(config)
    bot = await setup_bot(config)
    await setup_webhook(bot, config, logger)

    # @asynccontextmanager  # type: ignore
    # async def lifespan(_app: FastAPI):
    #     await setup_webhook(bot, config, logger)
    #     yield

    # app = FastAPI(lifespan=lifespan)  # type: ignore
    app = FastAPI()

    @app.post(config.webhook_path)
    async def webhook(
            request: Update,
            secret_token: Annotated[str | None, Header()] = None
    ) -> None | dict:
        """ Register webhook endpoint for telegram bot"""
        if secret_token != config.telegram_secret_token:
            logger.error("Wrong secret token !")
            return {"status": "error", "message": "Wrong secret token !"}
        await dp.feed_webhook_update(bot=bot, update=request)

    return app
