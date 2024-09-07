import asyncio
import logging
from datetime import datetime

from nats.aio.client import Client
from nats.js import JetStreamContext
from nats.js.api import StreamConfig, StorageType
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.database.requests import get_users_ids

logger = logging.getLogger(__name__)


class NotificationsPublisher:
    def __init__(
            self,
            nc: Client,
            subject: str,
            delay: int,
            session_maker: async_sessionmaker,
    ) -> None:
        self.nc = nc
        self.subject = subject
        self.delay = delay
        self.session_maker = session_maker

    # async def init(self):
    #     await self.js.add_stream(
    #         config=StreamConfig(
    #             name=self.stream,
    #             subjects=[self.subject],
    #             storage=StorageType.MEMORY,
    #             max_bytes=1024 * 512,
    #         )
    #     )

    async def publish(self, message_text: str):
        async with self.session_maker() as session:
            users_ids = await get_users_ids(session)

        for user_id in users_ids:
            headers = {
                # 'Tg-Delayed-Msg-Timestamp': str(datetime.now().timestamp()),
                # 'Tg-Msg-Delay': str(self.delay),
                'Tg-Chat-Id': str(user_id),
            }
            await self.nc.publish(subject=self.subject, headers=headers, payload=message_text.encode())
            await asyncio.sleep(delay=self.delay)
