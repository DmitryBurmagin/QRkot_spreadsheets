
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    @staticmethod
    async def get_completed_project_by_rate(session: AsyncSession):
        result = await session.execute(
            select(
                CharityProject.name,
                (CharityProject.close_date -
                 CharityProject.create_date).label('rate'),
                CharityProject.description
            )
            .filter(CharityProject.fully_invested.is_(True))
        )
        projects = result.fetchall()
        return projects


charity_project_crud = CRUDCharityProject(CharityProject)
