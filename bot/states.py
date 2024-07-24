from aiogram.fsm.state import StatesGroup, State


class TestStates(StatesGroup):
    description = State()
    test = State()
    results = State()


class GreetingStates(StatesGroup):
    greeting = State()
    auth = State()


class MenuStates(StatesGroup):
    menu = State()


class StatisticStates(StatesGroup):
    statistic = State()


class SecretsStates(StatesGroup):
    secrets = State()
