import logging

import uvicorn

from bot.app import get_app
from bot.polling import run_polling
from configs.config import parse_config

config = parse_config()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


async def main():
    if config.debug_mode:
        return run_polling(config)
    else:
        app = await get_app(config, logger)
        return app


if __name__ == "__main__":
    uvicorn.run(
        app=main,  # type: ignore
        port=config.port,
        loop="uvloop",
        interface="auto"
    )
