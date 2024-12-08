from datetime import datetime as dt
from app.models.base import CommonFields


def process_investments(
    new_entity: CommonFields,
    existing_entities: list[CommonFields]
) -> list[CommonFields]:
    """
    Распределяет средства между проектами и донейшенами.
    Обновляет статус объектов и распределяет средства.
    """
    if new_entity.fully_invested:
        return existing_entities

    for entity in existing_entities:
        available_amount = min(
            new_entity.full_amount - new_entity.invested_amount,
            entity.full_amount - entity.invested_amount
        )
        for obj in (entity, new_entity):
            obj.invested_amount += available_amount
            if obj.invested_amount == obj.full_amount:
                obj.fully_invested = True
                obj.close_date = dt.utcnow()

    return existing_entities
