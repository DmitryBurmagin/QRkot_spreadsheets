from datetime import datetime as dt

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def fetch_uninvested(session: AsyncSession, model):
    """Извлекает неинвестированные записи модели."""
    query = select(model).where(
        model.fully_invested.is_(False)).order_by(model.create_date)
    result = await session.execute(query)
    return result.scalars().all()


def calculate_investment(donation: Donation, project: CharityProject) -> int:
    """
    Рассчитывает доступную сумму для инвестиции на основе остатка средств.
    """
    return min(
        donation.full_amount - donation.invested_amount,
        project.full_amount - project.invested_amount
    )


def update_investment_status(obj, available_amount: int) -> None:
    """Обновляет статус инвестиции объекта."""
    obj.invested_amount += available_amount

    if obj.invested_amount == obj.full_amount:
        obj.fully_invested = True
        obj.close_date = dt.utcnow()


async def invest_funds(donation: Donation, project: CharityProject) -> None:
    """Инвестирует средства из донейшена в проект."""
    available_amount = calculate_investment(donation, project)

    update_investment_status(donation, available_amount)
    update_investment_status(project, available_amount)


async def process_investments(session: AsyncSession) -> None:
    """
    Распределяет неинвестированные средства между проектами и донейшенами.
    """
    projects = await fetch_uninvested(session, CharityProject)
    donations = await fetch_uninvested(session, Donation)

    for donation in donations:
        if donation.fully_invested:
            continue

        for project in projects:
            if project.fully_invested:
                continue

            await invest_funds(donation, project)

            if donation.fully_invested:
                break

    await session.commit()

    for obj in donations + projects:
        await session.refresh(obj)
