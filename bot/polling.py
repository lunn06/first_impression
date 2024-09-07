import asyncio
import logging

from bot.setup import setup, setup_bot
from configs.config import Config
from utils.start_broker import start_broker

logger = logging.getLogger(__name__)


async def run_polling(config: Config):
    dp, nc, js, session_maker = await setup(config)
    bot = await setup_bot(config)

    try:
        await asyncio.gather(
            dp.start_polling(bot),

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
