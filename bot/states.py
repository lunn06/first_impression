from aiogram.fsm.state import StatesGroup, State


class TestStates(StatesGroup):
    text_question = State()
    select_question = State()
    multiselect_question = State()
    results = State()
