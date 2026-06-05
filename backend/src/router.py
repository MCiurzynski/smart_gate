from fastapi import APIRouter

from src.plates.router import plates_router

router = APIRouter()
router.include_router(plates_router)
