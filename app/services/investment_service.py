from datetime import datetime as dt
from app.models.base import CommonFields


def process_investments(
    new_entities: list[CommonFields],
    existing_entities: list[CommonFields]
) -> list[CommonFields]:
    """
    Распределяет средства между проектами и донейшенами.
    Обновляет статус объектов и распределяет средства.
    """
    updated_entities = []

    for new_entity in new_entities:
        for entity in existing_entities:
            available_amount = min(
                new_entity.full_amount - new_entity.invested_amount,
                entity.full_amount - entity.invested_amount
            )
            new_entity.invested_amount += available_amount
            entity.invested_amount += available_amount

            for obj in (entity, new_entity):
                if obj.invested_amount == obj.full_amount:
                    obj.fully_invested = True
                    obj.close_date = dt.utcnow()
                    if obj not in updated_entities:
                        updated_entities.append(obj)

    return updated_entities
