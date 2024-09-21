from typing import Literal

    
class TranslatorRunner:
    def get(self, path: str, **kwargs) -> str: ...
    
    menu: Menu
    start: Start
    statistics: Statistics
    top: Top
    user: User
    wheretogo: Wheretogo
    secrets: Secrets
    back: Back


class Menu:
    @staticmethod
    def message(*, points, user_tests, total_tests) -> Literal["""{
    &#34;response_type&#34;: &#34;main_menu&#34;,
    &#34;user_points&#34;: { $points },
    &#34;user_completed_count&#34;: { $user_tests },
    &#34;total&#34;: { $total_tests }
}"""]: ...


class Start:
    @staticmethod
    def message() -> Literal["""101... точнее HELLO WORLD, программист! Ты попал на празднование профессионального празника всех айтишников.

Тебя ждёт b01010 тематических точек и float(&#39;infinity&#39;) пиццы и чая с синтаксическим сахаром"""]: ...

    @staticmethod
    def button() -> Literal["""python -m bot"""]: ...


class Statistics:
    @staticmethod
    def button() -> Literal["""Метрики"""]: ...


class Top:
    users: TopUsers


class TopUsers:
    @staticmethod
    def button() -> Literal["""top_users.txt"""]: ...


class User:
    tests: UserTests

    @staticmethod
    def test(*, is_complete, test_name) -> Literal["""{ $is_complete -&gt;
[true] ✅
*[false] 
} { $test_name }"""]: ...


class UserTests:
    @staticmethod
    def button() -> Literal["""package user_completed"""]: ...


class Wheretogo:
    @staticmethod
    def button() -> Literal["""SELECT map FROM programming_day;"""]: ...


class Secrets:
    @staticmethod
    def button() -> Literal["""Enter captcha"""]: ...

    @staticmethod
    def message() -> Literal["""ДОКАЖИ, ЧТО ТЫ НЕ РОБОТ"""]: ...


class Back:
    to: BackTo
    section: BackSection


class BackTo:
    menu: BackToMenu


class BackToMenu:
    @staticmethod
    def button() -> Literal["""{back_to_main_menu_button_text}"""]: ...


class BackSection:
    @staticmethod
    def button() -> Literal["""Назад"""]: ...

