from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (get_project_or_404,
                                validate_project_not_invested,
                                validate_project_update, validate_unique_name)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud, donation_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectResponse,
                                         CharityProjectUpdate)
from app.services.investment_service import process_investments

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectResponse:
    """Создает новый благотворительный проект."""
    await validate_unique_name(project.name, session)
    new_project = await charity_project_crud.create(project, session)
    incomplete_projects = await charity_project_crud.fetch_uninvested(session)
    incomplete_donations = await donation_crud.fetch_uninvested(session)
    updated_projects = process_investments(
        incomplete_donations, incomplete_projects
    )
    session.add_all(updated_projects + incomplete_donations)
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.get(
    '/',
    response_model=List[CharityProjectResponse],
    response_model_exclude_none=True
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session),
) -> List[CharityProjectResponse]:
    """Возвращает список всех благотворительных проектов."""
    return await charity_project_crud.get_multi(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectResponse:
    """Частично обновляет благотворительный проект."""
    charity_project = await validate_project_update(
        session=session,
        project_id=project_id,
        new_full_amount=obj_in.full_amount,
        new_name=obj_in.name
    )

    return await charity_project_crud.update(
        db_obj=charity_project,
        obj_in=obj_in,
        session=session
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectResponse:
    """Удаляет благотворительный проект."""
    project = await get_project_or_404(
        project_id, session)
    validate_project_not_invested(project)
    return await charity_project_crud.remove(project, session)
