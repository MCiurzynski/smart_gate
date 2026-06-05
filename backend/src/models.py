from sqlmodel import SQLModel  # noqa: F401

# Import every table model so Alembic's autogenerate sees them on the metadata.
from src.auth.models import User  # noqa: F401
from src.events.models import AccessEvent  # noqa: F401
from src.plates.models import Plate  # noqa: F401
