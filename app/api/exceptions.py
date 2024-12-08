from fastapi import HTTPException, status


def handle_google_api_error(error: Exception):
    """
    Обрабатывает ошибки, возникающие при взаимодействии с Google API,
    и выбрасывает HTTPException.
    """
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f'Ошибка взаимодействия с Google API: {error}'
    )
