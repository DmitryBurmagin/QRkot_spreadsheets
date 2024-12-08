from datetime import datetime as dt
from app.models.base import CommonFields


def process_investments(
    new_entities: CommonFields,
    existing_entities: list[CommonFields]
) -> list[CommonFields]:
    """
    Распределяет средства между проектами и донейшенами.
    Обновляет статус объектов и распределяет средства.
    """
    updated_entities = []

    available_amount = min(
        new_entities.full_amount - new_entities.invested_amount,
        existing_entities.full_amount - existing_entities.invested_amount
    )

    for obj in (existing_entities, new_entities):
        obj.invested_amount += available_amount

        if obj.invested_amount == obj.full_amount:
            obj.fully_invested = True
            obj.close_date = dt.utcnow()

        if obj not in updated_entities:
            updated_entities.append(obj)

    return updated_entities
