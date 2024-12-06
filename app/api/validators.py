from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


async def get_project_or_404(project_id: int, session: AsyncSession
                             ) -> CharityProject:
    """Возвращает проект или выбрасывает 404 ошибку."""
    charity_project = await charity_project_crud.get(
        obj_id=project_id, session=session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Проект не найден!'
        )
    return charity_project


def validate_full_amount(charity_project: CharityProject, new_full_amount: int
                         ) -> None:
    """Проверяет, что новый full_amount не меньше вложенной суммы."""
    if new_full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Нельзя установить значение'
            'full_amount меньше уже вложенной суммы.'
        )


async def validate_unique_name(name: str, session: AsyncSession) -> None:
    """
    Проверяет уникальность имени проекта в базе данных.
    """
    query = select(CharityProject).where(CharityProject.name == name)
    result = await session.execute(query)
    if result.scalar() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )


async def validate_project_update(
    session: AsyncSession,
    project_id: int,
    new_full_amount: int = None,
    new_name: str = None
) -> CharityProject:
    charity_project = await get_project_or_404(project_id, session)

    if charity_project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )

    if new_name and new_name != charity_project.name:
        await validate_unique_name(new_name, session)

    if new_full_amount:
        validate_full_amount(charity_project, new_full_amount)

    return charity_project


async def validate_project_not_invested(project: CharityProject) -> None:
    """Проверяет, что проект не имеет вложенных средств."""
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
