from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class DonationBase(BaseModel):
    """Базовая схема объекта пожертвования."""
    comment: Optional[str] = Field(None, title='Комментарий')
    full_amount: PositiveInt = Field(..., title='Сумма пожертвования')

    class Config:
        title = 'Базовая схема пожертвования'


class DonationCreate(DonationBase):
    """Схема пожертвования для создания."""

    class Config:
        extra = Extra.forbid
        title = 'Схема пожертвования для создания'
        schema_extra = {
            'example': {
                'comment': 'Помощь',
                'full_amount': 120
            }
        }


class DonationDB(DonationBase):
    """Схема пожертвования для получения из базы обычным пользователем."""
    id: int = Field(..., title='ID пожертвования')
    create_date: datetime = Field(..., title='Дата внесения пожертвования')

    class Config:
        title = 'Схема пожертвования для получения'
        orm_mode = True
        schema_extra = {
            'example': {
                'comment': 'Помощь',
                'full_amount': 120,
                'id': 2,
                'create_date': '2024-10-21T23:54:05.177Z'
            }
        }


class DonationDBSuper(DonationDB):
    """Схема пожертвования для получения из базы суперпользователем."""
    user_id: Optional[int] = Field(None, title='ID пользователя')
    invested_amount: int = Field(
        default=0,
        title='Сколько вложено',
    )
    fully_invested: bool = Field(False, title='Вложена полная сумма')
    close_date: Optional[datetime] = Field(None, title='Дата вложения')

    class Config:
        title = 'Схема пожертвования для получения (advanced)'
        orm_mode = True
        schema_extra = {
            'example': {
                'comment': 'На благотворительность',
                'full_amount': 150,
                'id': 4,
                'create_date': '2024-10-21T23:54:05.177Z',
                'user_id': 1,
                'invested_amount': 100,
                'fully_invested': 0
            }
        }
