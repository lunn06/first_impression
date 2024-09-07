import logging
from contextlib import suppress

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from nats.aio.client import Client
from nats.aio.msg import Msg

logger = logging.getLogger(__name__)


class NotificationsConsumer:
    def __init__(
            self,
            nc: Client,
            subject: str,
            bot: Bot,
    ) -> None:
        self.nc = nc
        self.subject = subject
        self.bot = bot

    async def start(self) -> None:
        self.nc_sub = await self.nc.subscribe(
            subject=self.subject,
            # stream=self.stream,
            cb=self.on_message,
            # durable=self.durable_name,
            # manual_ack=True
        )

    async def on_message(self, msg: Msg):
        message_text = msg.data.decode()
        chat_id = int(msg.headers.get('Tg-Chat-Id'))  # type: ignore
        with suppress(TelegramBadRequest):
            await self.bot.send_message(chat_id=chat_id, text=message_text)

    # async def on_message(self, msg: Msg):
    #     tz = timezone(timedelta(hours=7))
    #
    #     sent_time = datetime.fromtimestamp(
    #         float(msg.headers.get('Tg-Delayed-Msg-Timestamp')),  # type: ignore
    #         tz=tz
    #     )
    #     delay = int(msg.headers.get('Tg-Msg-Delay'))  # type: ignore
    #
    #     if sent_time + timedelta(seconds=delay) > datetime.now().astimezone(tz=tz):
    #         new_delay = (sent_time + timedelta(seconds=delay) - datetime.now().astimezone(tz=tz)).total_seconds()
    #         await msg.nak(delay=new_delay)
    #     else:
    #         message_text = msg.data.decode()
    #         chat_id = int(msg.headers.get('Tg-Chat-Id'))  # type: ignore
    #         with suppress(TelegramBadRequest):
    #             await self.bot.send_message(chat_id=chat_id, text=message_text)
    #         await msg.ack()

    async def unsubscribe(self) -> None:
        if self.nc_sub:
            await self.nc_sub.unsubscribe()
            logger.info('Consumer unsubscribed')
