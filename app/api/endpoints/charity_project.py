from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import DuplicateException
from app.api.validators import (
    check_invested_amount,
    check_investing_funds,
    check_name_duplicate,
    check_project_exists,
    check_project_open,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models import Donation
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.utils import (
    close_item,
    funds_distribution,
    get_uninvested_objects,
)

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Создание проектов. Только для суперюзеров."""
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    unallocated_donations = await get_uninvested_objects(Donation, session)
    try:
        funds_distribution(
            opened_items=unallocated_donations, funds=new_project
        )
        await session.commit()
        await session.refresh(new_project)
    except IntegrityError:
        await session.rollback()
        raise DuplicateException('Средства уже распределены')
    return new_project


@router.get(
    '/',
    response_model=Optional[List[CharityProjectDB]],
    response_model_exclude_none=True,
)
async def get_all_projects(session: AsyncSession = Depends(get_async_session)):
    """Получение проектов."""
    projects = await charity_project_crud.get_multi(session)
    return projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Редактирование проектов. Только для суперюзеров."""
    charity_project = await check_project_exists(project_id, session)
    await check_project_open(project_id, session)

    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount:
        await check_investing_funds(project_id, obj_in.full_amount, session)

    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    # на это вроде теста нет?..
    if obj_in.full_amount == charity_project.invested_amount:
        close_item(charity_project)
        await session.commit()
        await session.refresh(charity_project)

    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Удаление проектов. Только для суперюзеров."""
    charity_project = await check_project_exists(project_id, session)
    await check_invested_amount(project_id, session)
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project
