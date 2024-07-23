import logging

import uvicorn
import uvloop

from bot.app import get_app
from bot.configs.config import parse_config
from bot.polling import run_polling

config = parse_config()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    if config.debug_mode:
        uvloop.run(run_polling(config))
    else:
        app = get_app(config, logger)
        uvicorn.run(
            app=app,  # type: ignore
            port=config.port,
            loop="uvloop",
            interface="auto"
        )
