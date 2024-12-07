from datetime import datetime as dt

from app.models import CharityProject, Donation


def process_investments(
    donations: list[Donation],
    projects: list[CharityProject]
) -> list[CharityProject]:
    """
    Распределяет средства между проектами и донейшенами.
    Обновляет статус объектов и распределяет средства.
    """
    for donation in donations:
        if donation.fully_invested:
            continue

        for project in projects:
            if project.fully_invested:
                continue

            available_amount = min(
                donation.full_amount - donation.invested_amount,
                project.full_amount - project.invested_amount
            )

            donation.invested_amount += available_amount
            if donation.invested_amount == donation.full_amount:
                donation.fully_invested = True
                donation.close_date = dt.utcnow()

            project.invested_amount += available_amount
            if project.invested_amount == project.full_amount:
                project.fully_invested = True
                project.close_date = dt.utcnow()

            if donation.fully_invested:
                break

    return projects
