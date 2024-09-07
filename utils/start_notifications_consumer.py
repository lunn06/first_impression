import logging

from aiogram import Bot
from nats.aio.client import Client

from services.notifications.consumer import NotificationsConsumer

logger = logging.getLogger(__name__)


async def start_notifications_consumer(
        nc: Client,
        subject: str,
        bot: Bot,
) -> None:
    consumer = NotificationsConsumer(
        nc=nc,
        subject=subject,
        bot=bot,
    )

    logger.info('Start delayed message consumer')
    await consumer.start()
