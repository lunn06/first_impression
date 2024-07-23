from aiogram.fsm.state import StatesGroup, State


class TestStates(StatesGroup):
    test = State()
    # text_question = State()
    # select_question = State()
    # multiselect_question = State()
    results = State()
