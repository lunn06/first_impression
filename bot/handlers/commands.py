from pprint import pprint

from aiogram import Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message

router = Router()


@router.message(CommandStart(), flags={'chat_action': 'typing', 'rate_limit': {'rate': 5}})
async def start_handler(msg: Message, command: CommandObject):
    pprint(command.args)
