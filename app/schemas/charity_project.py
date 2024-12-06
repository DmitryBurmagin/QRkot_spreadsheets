from datetime import datetime as dt
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

MIN_STRING_LENGTH = 1
MAX_STRING_LENGTH = 100
DEFAULT_FULL_AMOUNT = 500000
DEFAULT_INVESTED_AMOUNT = 200000


class CharityProjectBase(BaseModel):
    name: str = Field(
        ...,
        min_length=MIN_STRING_LENGTH,
        max_length=MAX_STRING_LENGTH,
        description='Название проекта'
    )
    description: str = Field(
        ..., min_length=MIN_STRING_LENGTH, description='Описание проекта'
    )
    full_amount: PositiveInt = Field(
        ..., description='Полная сумма, которую нужно собрать для проекта'
    )

    class Config:
        extra = Extra.forbid
        schema_extra = {
            'example': {
                'name': 'Проект по спасению котиков',
                'description': 'Проект, направленный на'
                'спасение бездомных котиков.',
                'full_amount': DEFAULT_FULL_AMOUNT
            }
        }

    class Meta:
        sort_by = 'name'

    def __str__(self):
        return self.name


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectResponse(CharityProjectBase):
    id: int = Field(..., description='Идентификатор проекта')
    invested_amount: int = Field(
        ..., description='Сумма, которая уже была вложена в проект'
    )
    fully_invested: bool = Field(
        ..., description='Статус проекта: полностью ли собрана сумма?'
    )
    create_date: dt = Field(..., description='Дата создания проекта')
    close_date: Optional[dt] = Field(
        None, description='Дата закрытия проекта'
    )

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'id': 1,
                'name': 'Проект по спасению котиков',
                'description': 'Проект, направленный на'
                'спасение бездомных котиков.',
                'full_amount': DEFAULT_FULL_AMOUNT,
                'invested_amount': DEFAULT_INVESTED_AMOUNT,
                'fully_invested': False,
                'create_date': '2024-01-01T12:00:00Z',
                'close_date': None
            }
        }

    class Meta:
        sort_by = 'create_date'

    def __str__(self):
        return self.name


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(
        None, min_length=MIN_STRING_LENGTH, max_length=MAX_STRING_LENGTH,
        description='Новое название проекта'
    )
    description: Optional[str] = Field(None, min_length=MIN_STRING_LENGTH,
                                       description='Новое описание проекта')
    full_amount: Optional[PositiveInt] = Field(
        None, description='Новая полная сумма проекта'
    )

    class Config:
        schema_extra = {
            'example': {
                'name': 'Обновленный проект по спасению котиков',
                'description': 'Обновленное описание проекта.',
                'full_amount': DEFAULT_FULL_AMOUNT
            }
        }

    class Meta:
        sort_by = 'name'

    def __str__(self):
        return self.name
