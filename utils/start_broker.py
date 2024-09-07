import asyncio

from aiogram import Bot
from nats.aio.client import Client
from nats.js import JetStreamContext
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker

from configs import Config
from utils.start_notifications_consumer import start_notifications_consumer
from utils.start_top_consumer import start_delayed_consumer
from utils.start_top_publisher import start_delayed_publisher


async def start_broker(
        nc: Client,
        js: JetStreamContext,
        config: Config,
        cache: Redis,
        session_maker: async_sessionmaker,
        bot: Bot,
):
    await asyncio.gather(
        start_delayed_consumer(
            js=js,
            subject=config.nats_delayed_consumer_subject,
            stream=config.nats_delayed_consumer_stream,
            durable_name=config.nats_delayed_consumer_durable_name,
            cache=cache,
        ),

        start_delayed_publisher(
            js=js,
            stream=config.nats_delayed_consumer_stream,
            session_maker=session_maker,
            subject=config.nats_delayed_consumer_subject,
            delay=config.top_getting_delay,
        ),

        start_notifications_consumer(
            nc=nc,
            subject=config.nats_notifications_consumer_subject,
            bot=bot,
        ),
    )
