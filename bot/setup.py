import orjson
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.types import WebhookInfo
from aiogram_dialog import setup_dialogs
from fluentogram import TranslatorHub  # type: ignore
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot import dialogs
from bot.configs.config import Config
from bot.configs.questions import parse_questions_dict, Questions
from bot.database.base import Base
from bot.database.requests import test_connection, prepare_database
from bot.middlewares import TranslatorRunnerMiddleware, DbSessionMiddleware, AntiFloodMiddleware
from bot.utils.i18n import create_translator_hub
from bot.utils.secrets import Secret


async def setup_bot(config: Config) -> Bot:
    bot = Bot(
        token=config.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    await bot.delete_webhook(drop_pending_updates=True)

    return bot


def setup_cache(dp: Dispatcher):
    dragonfly = Redis(db=1)
    dp["cache"] = dragonfly


async def setup_db(dp: Dispatcher, config: Config, questions_dict: dict[str, Questions]):
    engine = create_async_engine(url=str(config.db_url), echo=config.debug_mode)

    if config.empty_db:
        meta = Base.metadata
        async with engine.begin() as conn:
            if config.debug_mode:
                await conn.run_sync(meta.drop_all)
            await conn.run_sync(meta.create_all)

    session_maker = async_sessionmaker(engine, expire_on_commit=config.debug_mode)

    async with session_maker() as session:
        await test_connection(session)
        if config.debug_mode:
            await prepare_database(session, questions_dict)

    dp.update.middleware(DbSessionMiddleware(session_pool=session_maker))


def setup_i18n(dp: Dispatcher, config: Config):
    translator_hub: TranslatorHub = create_translator_hub(config.locales_path)

    dp.update.middleware(TranslatorRunnerMiddleware())
    dp["_translator_hub"] = translator_hub


async def setup_dp(config: Config) -> Dispatcher:
    storage = RedisStorage(
        redis=Redis(),
        key_builder=DefaultKeyBuilder(with_destiny=True),
        # json_loads=orjson.loads,
        # json_dumps=orjson.dumps,
    )
    dp = Dispatcher(storage=storage)
    questions_dict = parse_questions_dict(config)

    dp.include_routers(*dialogs.get_dialogs())

    secrets_dict: dict[str, Secret] = {}
    for questions_filename, questions in questions_dict.items():
        secrets_dict[questions_filename] = Secret(
            name=questions.name,
            secret=questions_filename,
            interval=questions.interval,
        )

    dp.message.register(greeting.start_handler, CommandStart())

    setup_cache(dp)
    setup_dialogs(dp)
    setup_i18n(dp, config)
    await setup_db(dp, config, questions_dict)

    dp.message.middleware(AntiFloodMiddleware(config.flood_awaiting))

    dp["config"] = config
    dp["secrets_dict"] = secrets_dict
    dp["questions_dict"] = questions_dict

    return dp


async def setup_webhook(bot: Bot, config: Config, logger) -> None:
    # Check and set webhook for Telegram
    async def check_webhook() -> WebhookInfo | None:
        try:
            webhook_info = await bot.get_webhook_info()
            return webhook_info
        except Exception as e:
            logger.error(f"Can't get webhook info - {e}")
            return None

    current_webhook_info = await check_webhook()

    assert current_webhook_info

    if config.debug_mode:
        logger.debug(f"Current bot info: {current_webhook_info}")
    try:
        await bot.set_webhook(
            f"{config.webhook_url}{config.webhook_path}",
            secret_token=config.telegram_secret_token,
            drop_pending_updates=current_webhook_info.pending_update_count > 0,
            # max_connections=40 if config.debug else 100,
        )
        if config.debug_mode:
            logger.debug(f"Updated bot info: {await check_webhook()}")
    except Exception as e:
        logger.error(f"Can't set webhook - {e}")
