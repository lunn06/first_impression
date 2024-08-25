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


class WhereToGoStates(StatesGroup):
    where_to_go = State()


class SecretsStates(StatesGroup):
    secrets = State()


class BackToMenuStates(StatesGroup):
    back_to_menu = State()


class SuperStates(StatesGroup):
    menu = State()
    view_secrets = State()
    view_top = State()


class EnsureSuperStates(StatesGroup):
    choose_type = State()
    ensure_super = State()
    delete_super = State()
    choose_tests = State()
