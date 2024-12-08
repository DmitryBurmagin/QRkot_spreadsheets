from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import CharityProject
from app.models.user import User
from app.schemas.donation import (DonationCreate, DonationCreateResponse,
                                  DonationSuperUserResponse)
from app.services.investment_service import process_investments

router = APIRouter()


@router.post(
    '/',
    response_model=DonationCreateResponse,
    response_model_exclude_none=True,
)
async def create_donation(
    new_donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
) -> DonationCreateResponse:
    """
    Создает новое пожертвование от текущего пользователя.
    """
    donation_data = new_donation.dict()
    donation_data['user_id'] = current_user.id
    donation = await donation_crud.create(donation_data, session)
    active_projects = await session.execute(
        select(CharityProject).where(CharityProject.fully_invested.is_(False))
    )
    projects = active_projects.scalars().all()
    updated_entities = process_investments([donation], projects)
    session.add_all(updated_entities)
    await session.commit()
    await session.refresh(donation)
    return donation


@router.get(
    '/',
    response_model=List[DonationSuperUserResponse],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
) -> List[DonationSuperUserResponse]:
    """
    Возвращает список всех пожертвований.
    Доступно только для суперпользователей.
    """
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=List[DonationCreateResponse],
    response_model_exclude_none=True,
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
) -> List[DonationCreateResponse]:
    """
    Возвращает список пожертвований текущего пользователя.
    """
    return await donation_crud.get_by_user_id(current_user.id, session)
