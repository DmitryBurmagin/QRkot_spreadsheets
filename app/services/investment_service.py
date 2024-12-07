from datetime import datetime as dt
from typing import List

from app.models.base import CommonFields


def process_investments(
    new_entity: CommonFields,
    existing_entities: List[CommonFields]
) -> List[CommonFields]:
    """
    Распределяет средства между проектами и донейшенами.
    Обновляет статус объектов и распределяет средства.
    """
    if new_entity.fully_invested:
        return []

    updated_entities = []

    for entity in existing_entities:
        if entity.fully_invested:
            continue

        available_amount = min(
            new_entity.full_amount - new_entity.invested_amount,
            entity.full_amount - entity.invested_amount
        )
        new_entity.invested_amount += available_amount
        entity.invested_amount += available_amount

        if entity.invested_amount == entity.full_amount:
            entity.fully_invested = True
            entity.close_date = dt.utcnow()
            updated_entities.append(entity)

        if new_entity.invested_amount == new_entity.full_amount:
            new_entity.fully_invested = True
            new_entity.close_date = dt.utcnow()
            break

    return updated_entities
