import asyncio

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.google import (create_spreadsheet, set_user_permissions,
                                 spreadsheet_update_values)

router = APIRouter()


@router.post(
    '/',
    response_model=list[dict[str, str]],
    dependencies=[Depends(current_superuser)],
)
async def create_projects_spreadsheet(
    session: AsyncSession = Depends(get_async_session),
    wrapp_services: Aiogoogle = Depends(get_service),
):
    """
    Создает новую электронную таблицу с информацией о завершенных проектах.
    """
    projects = await charity_project_crud.get_completed_project_by_rate(
        session
    )
    spreadsheet_id, spreadsheet_url = await create_spreadsheet(
        wrapp_services
    )
    try:
        await asyncio.gather(
            set_user_permissions(wrapp_services, spreadsheet_id),
            spreadsheet_update_values(spreadsheet_id, projects, wrapp_services)
        )
        return spreadsheet_url
    except Exception as e:
        return {'error': f'Произошла ошибка: {e}'}
