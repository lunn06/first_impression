from __future__ import annotations

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def build_keyboard(*buttons_text: str, resize_keyboard: bool = True) -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text=text)] for text in buttons_text
    ]

    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=resize_keyboard)
