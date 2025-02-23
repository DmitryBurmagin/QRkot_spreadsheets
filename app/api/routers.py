from fastapi import APIRouter

from app.api.endpoints import (donation_router, google_router, projects_router,
                               user_router)

main_router = APIRouter()

main_router.include_router(user_router)
main_router.include_router(
    projects_router,
    prefix='/charity_project',
    tags=['Charity Project']
)
main_router.include_router(
    donation_router,
    prefix='/donation',
    tags=['Donations']
)
main_router.include_router(
    google_router,
    prefix='/google',
    tags=['Google']
)
