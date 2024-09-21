menu-message =
    {"{"}
        "response_type": "main_menu",
        "user_points": { $points },
        "user_completed_count": { $user_tests },
        "total": { $total_tests }
    {"}"}

start-message =
    101... точнее HELLO WORLD, программист! Ты попал на празднование профессионального празника всех айтишников.

    Тебя ждёт b01010 тематических точек и float('infinity') пиццы и чая с синтаксическим сахаром

start-button = python -m bot

statistics-button = Метрики

top-users-button = top_users.txt

user-tests-button = package user_completed

wheretogo-button = SELECT map FROM programming_day;

secrets-button = Enter captcha

wheretogo-message = {""}

secrets-message = ДОКАЖИ, ЧТО ТЫ НЕ РОБОТ

back-to-menu-button = {"{"}back_to_main_menu_button_text{"}"}

back-section-button = Назад

user-test = { $is_complete ->
        [true] ✅
        *[false] {""}
    } { $test_name }
