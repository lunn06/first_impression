from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment

from configs import Questions, TestTypeEnum, Config
from configs.config import LocationMode


async def types_or_map_getter(dialog_manager: DialogManager, config: Config, **_kwargs):
    types = tuple(map(lambda v: v.value, TestTypeEnum))  # TODO: перенести в i18n
    dialog_manager.dialog_data["types"] = types

    map_attachment = None
    if config.location_mode == LocationMode.picture:
        assert config.map_path is not None
        map_attachment = MediaAttachment(ContentType.PHOTO, path=str(config.map_path))

    return {
        "buttons_text": "Выберите тип локации, которых хотите посетить",
        "map_text": "Выбирай куда пойти!",
        "map": map_attachment,

        "types": tuple(enumerate(map(lambda v: v.on_russian(), TestTypeEnum))),
        "back_to_menu_button_text": "Назад",

        "is_map_mode": config.location_mode == LocationMode.picture,
        "is_buttons_mode": config.location_mode == LocationMode.buttons,
    }


async def locations_getter(dialog_manager: DialogManager, **_kwargs):
    questions_dict: dict[str, Questions] = dialog_manager.middleware_data["questions_dict"]
    selected_type = dialog_manager.dialog_data["selected_type"]
    locations_set = set(s.location for s in questions_dict.values() if s.type == selected_type)

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
