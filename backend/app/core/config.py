from typing import Annotated, Any, TypeGuard, cast

from pydantic import AnyUrl, BeforeValidator, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


def is_list_of_str(val: Any) -> TypeGuard[list[str]]:
    if not isinstance(val, list):
        return False
    items = cast(list[Any], val)
    return all(isinstance(i, str) for i in items)


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str):
        if v.startswith("["):
            return v
        return [i.strip() for i in v.split(",") if i.strip()]
    if is_list_of_str(v):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../../.env", env_ignore_empty=True, extra="ignore"
    )

    API_V1_STR: str = "/api/v1"
    FRONTEND_HOST: str = "http://localhost:5175"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    @computed_field
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]

    PROJECT_NAME: str = "smart-gate-backend"


settings = Settings()
