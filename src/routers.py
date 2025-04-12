from fastapi import APIRouter

from src.tron.tron_controllers import router as tron_router


def get_apps_router():
    router = APIRouter()
    router.include_router(tron_router)
    return router
