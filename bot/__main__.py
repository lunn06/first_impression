import logging

import uvicorn
import uvloop

from bot.app import get_app
from bot.polling import run_polling
from configs.config import parse_config

config = parse_config()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


async def main():
    if config.debug_mode:
        return await run_polling(config)
    else:
        app = await get_app(config, logger)
        return app


if __name__ == "__main__":
    if config.debug_mode:
        uvloop.run(main())
    else:
        app = uvloop.run(main())
        uvicorn.run(
            app=app,  # type: ignore
            port=config.port,
            loop="uvloop",
            interface="auto"
        )
