import asyncio
import logging
from datetime import datetime

import orjson
from nats.js.api import StorageType, StreamConfig
from nats.js.client import JetStreamContext
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.database.requests import get_top_users

logger = logging.getLogger(__name__)


class TopUsersPublisher:
    def __init__(
            self,
            js: JetStreamContext,
            subject: str,
            delay: int,
            session_maker: async_sessionmaker,
            stream: str,
    ) -> None:
        self.js = js
        self.subject = subject
        self.delay = delay
        self.session_maker = session_maker
        self.stream = stream

    async def init(self):
        await self.js.add_stream(
            config=StreamConfig(
                name=self.stream,
                subjects=[self.subject],
                storage=StorageType.MEMORY,
                max_bytes=1024 * 512,
            )
        )

    async def publish(self):
        async with self.session_maker() as session:
            top_users = await get_top_users(session)

        str_top_users = orjson.dumps(tuple((user.user_name, float(user.user_points)) for user in top_users))

        headers = {
            'Tg-Delayed-Msg-Timestamp': str(datetime.now().timestamp()),
            # 'Tg-Delayed-Msg-Delay': str(self.delay),
            # 'Tg-Delayed-Top-Users': str_top_users
        }
        # await self.nc.publish(subject=self.subject, headers=headers)
        await self.js.publish(subject=self.subject, headers=headers, payload=str_top_users)

    async def start(self):
        while True:
            await self.publish()
            await asyncio.sleep(self.delay - 5)
