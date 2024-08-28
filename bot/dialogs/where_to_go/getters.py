from aiogram_dialog import DialogManager

from bot.configs.questions import Questions


async def locations_getter(dialog_manager: DialogManager, **_kwargs):
    questions_dict: dict[str, Questions] = dialog_manager.middleware_data["questions_dict"]
    locations_set = set(s.location for s in questions_dict.values())

    dialog_manager.dialog_data["locations"] = tuple(locations_set)

    return {
        "text": "Выберите адрес",
        "locations": tuple(enumerate(locations_set))
    }


async def audiences_getter(dialog_manager: DialogManager, **_kwargs):
    questions_dict: dict[str, Questions] = dialog_manager.middleware_data["questions_dict"]
    selected_location = dialog_manager.dialog_data["selected_location"]
    audiences = tuple(q.audience for q in questions_dict.values() if q.location == selected_location)

    dialog_manager.dialog_data["audiences"] = audiences

    return {
        "text": "Выберите аудторию",
        "audiences": tuple(enumerate(audiences)),

        "back_to_locations_button_text": "Назад",
    }


async def description_getter(dialog_manager: DialogManager, **_kwargs):
    selected_location = dialog_manager.dialog_data["selected_location"]
    selected_audience = dialog_manager.dialog_data["selected_audience"]
    questions_dict: dict[str, Questions] = dialog_manager.middleware_data["questions_dict"]

    selected_question = None
    for q in questions_dict.values():
        if q.location == selected_location and q.audience == selected_audience:
            selected_question = q
            break

    assert selected_question

    return {
        "text": selected_question.description,
        "back_button_text": "Назад",
    }
