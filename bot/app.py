import asyncio
from typing import Annotated

import uvicorn
from aiogram.types import Update
from fastapi import FastAPI, Header

from bot.setup import setup, setup_bot, setup_webhook
from configs import Config
from utils.start_broker import start_broker


async def get_app(config: Config, logger):
    dp, nc, js, session_maker = await setup(config)
    bot = await setup_bot(config)
    await setup_webhook(bot, config, logger)

    app = FastAPI()

    @app.post(config.webhook_path)
    async def webhook(
            request: Update,
            x_telegram_bot_api_secret_token: Annotated[str | None, Header()] = None
    ) -> None | dict:
        """ Register webhook endpoint for telegram bot"""
        if x_telegram_bot_api_secret_token != config.telegram_secret_token:
            logger.error("Wrong secret token !")
            return {"status": "error", "message": "Wrong secret token!"}
        await dp.feed_webhook_update(bot=bot, update=request)

    server_config = uvicorn.Config(app, port=config.port)
    server = uvicorn.Server(server_config)

    try:
        await asyncio.gather(
            server.serve(),

            start_broker(
                nc=nc, js=js,
                config=config,
                cache=dp["cache"],
                session_maker=session_maker,
                bot=bot
            )
        )
    except Exception as e:
        logger.exception(e)
    finally:
        await nc.close()
