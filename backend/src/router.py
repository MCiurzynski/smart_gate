from fastapi import APIRouter

from src.events.router import events_router
from src.plates.router import plates_router

router = APIRouter()
router.include_router(plates_router)
router.include_router(events_router)
