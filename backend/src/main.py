from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.config import settings
from src.database import engine, init_db
from src.logger import logger
from src.router import router


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    logger.info("Inicjalizacja systemu Smart Gate...")
    init_db()

    logger.info("System gotowy do pracy.")

    yield

    logger.info("Zamykanie połączeń i czyszczenie zasobów...")

    engine.dispose()
    logger.info("System zamknięty poprawnie.")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESC,
    version="0.1.0",
    lifespan=app_lifespan,
    openapi_url=f"{settings.API_STR}/openapi.json",
)


if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(router, prefix=settings.API_STR)
