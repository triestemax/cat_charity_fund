from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    """Проверка уникальности названия проекта."""
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    """Проверка существования проекта."""
    charity_project = await charity_project_crud.get(project_id, session)
    if not charity_project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return charity_project


async def check_project_open(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Проверка того, что проект еще открыт."""
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project.close_date:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!',
        )
    return charity_project


async def check_investing_funds(
        project_id: int,
        obj_in_full_amount,
        session: AsyncSession,
) -> CharityProject:
    """Проверка новой требуемой суммы."""
    charity_project = await charity_project_crud.get(project_id, session)
    if obj_in_full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Требуемая сумма проекта не может быть меньше вложенной!',
        )
    return charity_project


async def check_invested_amount(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Проверка того, что в проект уже поступили некоторые средства."""
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!',
        )
    return charity_project
