import logging

from nats.aio.client import Client
from nats.js import JetStreamContext
from sqlalchemy.ext.asyncio import async_sessionmaker

from services.top_users.publisher import TopUsersPublisher

logger = logging.getLogger(__name__)


async def start_delayed_publisher(
        js: JetStreamContext,
        stream: str,
        session_maker: async_sessionmaker,
        subject: str,
        delay: int,
) -> None:
    publisher = TopUsersPublisher(
        js=js,
        stream=stream,
        session_maker=session_maker,
        subject=subject,
        delay=delay,
    )

    logger.info('Start delayed message publisher')
    await publisher.init()
    await publisher.start()
