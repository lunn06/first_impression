from aiogram.filters import BaseFilter
from aiogram.types import Message


class AdminFilter(BaseFilter):
    def __init__(self, admins: list[int]):
        self.admins = admins

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admins  # type: ignore
