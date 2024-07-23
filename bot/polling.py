from bot.configs.config import Config
from bot.setup import setup_dp, setup_bot


async def run_polling(config: Config):
    dp = await setup_dp(config)
    bot = await setup_bot(config)

    await dp.start_polling(bot)
