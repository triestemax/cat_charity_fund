from datetime import datetime
from typing import List, Optional, Type, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation

'''
 Попробовал через | выдает ошибку.
 В мануале написано, что Union можно заменить на |
 только с версии 3.10 и выше, а мы работаем в 3.9
'''
MyComplexType = Union[Donation, CharityProject]


def funds_distribution(
        opened_items: Optional[List[MyComplexType]],
        funds: MyComplexType,
) -> MyComplexType:
    if opened_items:
        for item in opened_items:
            funds_diff = funds.full_amount - funds.invested_amount
            item_diff = item.full_amount - item.invested_amount
            if funds_diff >= item_diff:
                funds.invested_amount += item_diff
                item.invested_amount = item.full_amount
                close_item(item)
                if funds_diff == item_diff:
                    close_item(funds)
            else:
                item.invested_amount += funds_diff
                funds.invested_amount = funds.full_amount
                close_item(funds)
                break
    return funds


def close_item(item: MyComplexType) -> MyComplexType:
    item.fully_invested = True
    item.close_date = datetime.now()
    return item


async def get_uninvested_objects(
        obj_model: Type[MyComplexType],
        session: AsyncSession,
) -> Optional[List[MyComplexType]]:
    uninvested_objects = await session.execute(
        select(obj_model).where(
            obj_model.fully_invested.is_(False)
        ).order_by(obj_model.create_date)
    )
    return uninvested_objects.scalars().all()
