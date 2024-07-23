from __future__ import annotations

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, FSInputFile, Message


def build_keyboard(*buttons_text: str, resize_keyboard: bool = True) -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text=text)] for text in buttons_text
    ]

    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=resize_keyboard)


map_file_id: str | None = None


async def send_map(msg: Message, file_path: str):
    global map_file_id

    if map_file_id is None:
        file = FSInputFile(path=file_path)
        sent_photo: Message = await msg.answer_photo(photo=file)
        map_file_id = sent_photo.photo[-1].file_id
        return
    await msg.answer_photo(photo=map_file_id)
