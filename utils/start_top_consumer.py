import logging

from nats.js.client import JetStreamContext
from redis.asyncio import Redis

from services.top_users.consumer import TopUsersConsumer

logger = logging.getLogger(__name__)


async def start_delayed_consumer(
        js: JetStreamContext,
        subject: str,
        stream: str,
        durable_name: str,
        cache: Redis,
) -> None:
    consumer = TopUsersConsumer(
        js=js,
        subject=subject,
        stream=stream,
        durable_name=durable_name,
        cache=cache,
    )

    logger.info('Start delayed message consumer')
    await consumer.start()
