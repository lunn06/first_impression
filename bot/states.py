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
    top_users = State()


class WhereToGoStates(StatesGroup):
    types = State()
    locations = State()
    audiences = State()
    description = State()


class SecretsStates(StatesGroup):
    secrets = State()


class BackToMenuStates(StatesGroup):
    back_to_menu = State()


class SuperStates(StatesGroup):
    menu = State()
    view_top = State()


class ViewSecretsStates(StatesGroup):
    user_secrets = State()
    view_secret = State()


class EnsureSuperStates(StatesGroup):
    choose_type = State()
    ensure_super = State()
    choose_tests = State()


class DeleteSuperStates(StatesGroup):
    delete_super = State()
