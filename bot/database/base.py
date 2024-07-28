from sqlalchemy import String
from sqlalchemy.dialects.mysql import REAL
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    type_annotation_map = {
        str: String(30),
        float: REAL(
            precision=6,
            scale=2,
            unsigned=True
        )
    }
