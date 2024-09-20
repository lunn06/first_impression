import logging

from nats.aio.msg import Msg
from nats.js import JetStreamContext
from orjson import orjson
from redis.asyncio import Redis

from bot.database.cached_requests import ensure_top_users

logger = logging.getLogger(__name__)


class TopUsersConsumer:
    def __init__(
            self,
            js: JetStreamContext,
            subject: str,
            stream: str,
            durable_name: str,
            cache: Redis,
    ) -> None:
        self.js = js
        self.subject = subject
        self.stream = stream
        self.durable_name = durable_name
        self.cache = cache

    async def start(self) -> None:
        self.stream_sub = await self.js.subscribe(
            subject=self.subject,
            stream=self.stream,
            cb=self.on_message,
            durable=self.durable_name,
            # manual_ack=True
        )

    async def on_message(self, msg: Msg):
        sent_time = float(msg.headers.get('Tg-Delayed-Msg-Timestamp'))

        top_users = orjson.loads(msg.data)
        await ensure_top_users(self.cache, top_users, sent_time)  # type: ignore

    async def unsubscribe(self) -> None:
        if self.stream_sub:
            await self.stream_sub.unsubscribe()
            logger.info('Consumer unsubscribed')
