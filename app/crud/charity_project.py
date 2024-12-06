from datetime import datetime
from typing import Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.base import CRUDBase
from app.models import CharityProject, Donation


class CRUDCharityProject(CRUDBase):

    async def update(
        self,
        db_obj: Union[CharityProject, Donation],
        obj_in,
        session: AsyncSession,
    ) -> Union[CharityProject, Donation]:

        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data and update_data[field] is not None:
                setattr(db_obj, field, update_data[field])

        db_obj = self.set_close(db_obj)

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    @staticmethod
    def set_close(obj: Union[CharityProject, Donation]
                  ) -> Union[CharityProject, Donation]:
        if obj.full_amount == obj.invested_amount:
            obj.fully_invested = True
            obj.close_date = datetime.utcnow()
        return obj

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
            .order_by('rate')
        )
        projects = result.fetchall()

        return [
            {
                'name': project.name,
                'rate': str(project.rate),
                'description': project.description
            }
            for project in projects
        ]


charity_project_crud = CRUDCharityProject(CharityProject)
