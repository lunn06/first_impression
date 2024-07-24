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

from bot.configs.config import Config
from bot.configs.questions import parse_questions_dict
from bot.database.base import Base
from bot.database.requests import test_connection, prepare_database
from bot.dialogs import test_dialog, greeting, menu, statistic, secrets
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


async def setup_dp(config: Config) -> Dispatcher:
    storage = RedisStorage(
        redis=Redis(),
        key_builder=DefaultKeyBuilder(with_destiny=True)
    )  # type: ignore
    # storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    questions_dict = parse_questions_dict(config)

    # dp.include_routers(*get_routers())
    # questions_names = list(questions_dict.keys())

    dp.include_router(greeting.get_dialog())
    dp.include_router(menu.get_dialog())
    dp.include_router(statistic.get_dialog())
    dp.include_router(secrets.get_dialog())
    dp.include_router(test_dialog.get_dialog())

    secrets_dict: dict[str, Secret] = {}
    for questions_filename, questions in questions_dict.items():
        secrets_dict[questions_filename] = Secret(
            name=questions.name,
            secret=questions_filename,
            # handler=test_dialog.get_start_test_handler(questions_filename),
            handler=None,
            interval=questions.interval,
        )

    dp.message.register(greeting.start_handler, CommandStart())

    setup_dialogs(dp)

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

    translator_hub: TranslatorHub = create_translator_hub(config.locales_path)

    dp.update.middleware(TranslatorRunnerMiddleware())
    dp.message.middleware(AntiFloodMiddleware(config.flood_awaiting))
    dp.update.middleware(DbSessionMiddleware(session_pool=session_maker))
    # dp.update.middleware(EnsureUserMiddleware())
    # dp.include_routers(*get_routers())

    dp["config"] = config
    dp["secrets_dict"] = secrets_dict
    dp["questions_dict"] = questions_dict
    dp["_translator_hub"] = translator_hub

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
