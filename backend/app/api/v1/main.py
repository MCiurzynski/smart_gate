from fastapi import APIRouter

from app.api.v1.routes import history, login, plates

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(history.router)
api_router.include_router(plates.router)
