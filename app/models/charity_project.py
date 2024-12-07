from sqlalchemy import Column, String, Text

from app.core.db import Base

from .base import CommonFields

MAX_STRING_LENGTH = 100


class CharityProject(Base, CommonFields):

    name = Column(String(MAX_STRING_LENGTH), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        base_repr = super().__repr__()
        description_length = len(self.description)
        return (
            f'{base_repr}, name={self.name}, '
            f'description_length={description_length}'
        )
