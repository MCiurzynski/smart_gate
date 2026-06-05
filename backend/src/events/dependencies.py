from typing import Any

from sqlmodel import select

from src.database import SessionDep
from src.events.models import AccessEvent
from src.events.schemas import AccessEventCreate
from src.plates.models import Plate


async def record_event(session: SessionDep, event_in: AccessEventCreate) -> Any:
    """
    Store a detection, marking it allowed when the code is on the whitelist.
    """
    clean_code = event_in.code.upper().replace(" ", "")
    plate = session.exec(select(Plate).where(Plate.code == clean_code)).first()

    event = AccessEvent(
        code=clean_code,
        allowed=plate is not None,
        label=plate.label if plate else None,
    )
    session.add(event)
    session.commit()
    session.refresh(event)
    return event
