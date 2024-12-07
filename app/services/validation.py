from typing import List


def validate_table_size(value: int) -> None:
    """Проверяет, что значение находится в пределах допустимых размеров."""
    from app.services.validation import MAX_SIZE, MIN_SIZE
    if not MIN_SIZE <= value <= MAX_SIZE:
        raise ValueError(
            f'Размер должен быть между {MIN_SIZE} '
            f'и {MAX_SIZE}. Получено: {value}.'
        )


def validate_table_header(header: List[str]) -> None:
    """Проверяет заголовки таблиц."""
    for column in header:
        if not column.strip():
            raise ValueError('Заголовок таблицы не может быть пустым.')
