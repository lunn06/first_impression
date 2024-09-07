from __future__ import annotations

import os
from dataclasses import dataclass
from enum import StrEnum
from glob import glob
from typing import override, Iterator, Literal, Union, Any

from pydantic import BaseModel, PositiveInt, Field, NonNegativeFloat, PositiveFloat
from pydantic_core import from_json

from configs.config import Config
from utils.last_updated_ordered_dict import LastUpdatedOrderedDict

MINUTE = 60
HOUR = MINUTE * 60
DAY = 24 * HOUR


@dataclass
class Defaults:
    decrease: float
    interval: int
    coast: int
    limit: int


class TestTypeEnum(StrEnum):
    lecture = "lecture"
    museum = "museum"
    sport = "sport"
    laboratory = "laboratory"
    building = "building"

    def on_russian(self):
        match self:
            case self.lecture:
                return "Лекция"
            case self.museum:
                return "Музей"
            case self.sport:
                return "Спорт"
            case self.laboratory:
                return "Лаборатория"
            case self.building:
                return "Корпус"

    def default(self):
        match self:
            case self.lecture:
                return Defaults(
                    decrease=0,
                    interval=int(HOUR * 1.5),
                    coast=0,
                    limit=50,
                )
            case self.museum:
                return Defaults(
                    decrease=0.01,
                    interval=DAY,
                    coast=0,
                    limit=50,
                )
            case self.sport:
                return Defaults(
                    decrease=0,
                    interval=HOUR,
                    coast=0,
                    limit=50,
                )
            case self.laboratory:
                return Defaults(
                    decrease=0.01,
                    interval=DAY,
                    coast=0,
                    limit=50,
                )
            case self.building:
                return Defaults(
                    decrease=0.01,
                    interval=DAY,
                    coast=0,
                    limit=50,
                )


class Questions(BaseModel):
    name: str
    description: str
    type: TestTypeEnum
    location: str
    audience: str

    interval: PositiveInt
    coast: PositiveFloat
    guest_count: Union[PositiveInt, Literal["all"]]
    decrease: NonNegativeFloat
    limit: PositiveInt = Field(ge=0, le=100, default=50)

    questions: list[Question]

    def __getitem__(self, index: int) -> Question:
        return self.questions[index]

    @override
    def __iter__(self) -> Iterator[Question]:  # type: ignore
        return self.questions.__iter__()

    def __len__(self) -> int:
        return len(self.questions)


class Question(BaseModel):
    text: str
    type: QuestionsTypeEnum
    answers: list[str]
    right_answers: list[str]


class QuestionsTypeEnum(StrEnum):
    multiselect = "multiselect"
    select = "select"
    text = "text"


def _questions_from_json(questions_json: dict[Any, Any]) -> Questions:
    questions = Questions.model_validate(questions_json)

    return questions


def _tests_path(models_path: str):
    return f"{models_path}{os.sep}tests{os.sep}"


def _json_name(json_path: str) -> str:
    """Парсит незвание json файла

    /path/to/file.json -> file"""
    json_name = json_path.split(os.sep)[-1].split('.')[0]

    return json_name


def _prepare_json(json: dict[Any, Any]) -> None:
    event_type = TestTypeEnum[json["type"]]
    defaults = event_type.default()

    if isinstance(json["guest_count"], int) and json["guest_count"] > len(json["questions"]):
        raise ValueError("guest_count > len(questions)")

    if json.get("decrease", None) is None:
        json["decrease"] = defaults.decrease

    if json.get("interval", None) is None:
        json["interval"] = defaults.interval

    if json.get("coast", None) is None:
        json["coast"] = defaults.coast

    if json.get("limit", None) is None:
        json["limit"] = defaults.limit


def parse_questions_dict(config: Config) -> dict[str, "Questions"]:
    questions_path = _tests_path(str(config.models_path))

    questions: dict[str, Questions] = LastUpdatedOrderedDict()
    for questions_json_path in glob(questions_path + "*"):
        questions_json_name = _json_name(questions_json_path)

        with open(questions_json_path, 'r') as json_file:
            questions_json: dict[Any, Any] = from_json(json_file.read(), cache_strings=True)
        _prepare_json(questions_json)
        questions_model = _questions_from_json(questions_json)

        questions[questions_json_name] = questions_model

    return questions

# if __name__ == '__main__':
#     ...
