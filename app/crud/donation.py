from typing import Optional, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject, Donation, User
from app.schemas.donation import DonationCreate


class CRUDDonation(CRUDBase):

    async def get_by_user_id(self, user_id: int, session: AsyncSession):
        """Получить все пожертвования пользователя по его ID."""
        result = await session.execute(
            select(self.model).where(self.model.user_id == user_id)
        )
        return result.scalars().all()

    async def create(
        self,
        request_obj: DonationCreate,
        session: AsyncSession,
        user: Optional[User] = None
    ) -> Union[CharityProject, Donation]:
        """
        Создает объект модели с возможностью привязки пользователя.
        """
        db_obj = self.set_user(request_obj, self.model, user)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    @staticmethod
    def set_user(
        request_obj: dict,
        obj_model: Union[CharityProject, Donation],
        user: Optional[User],
    ) -> Union[CharityProject, Donation]:
        """
        Устанавливает текущего пользователя для объекта, если он передан.
        """
        if user:
            request_obj['user_id'] = user.id

        return obj_model(**request_obj)


donation_crud = CRUDDonation(Donation)
