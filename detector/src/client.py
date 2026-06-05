import logging

import httpx

from src.config import Config

logger = logging.getLogger(__name__)


def report_detections(plates: set[str]) -> None:
    """
    Send each detected plate to the backend events endpoint.

    Best-effort: a backend hiccup must never crash the detection loop, so all
    network errors are logged and swallowed.
    """
    if not plates:
        return

    url = f"{Config.BACKEND_URL.rstrip('/')}/events/"
    for code in plates:
        try:
            response = httpx.post(url, json={"code": code}, timeout=5.0)
            response.raise_for_status()
            logger.info("Zgłoszono tablicę %s do backendu", code)
        except httpx.HTTPError as exc:
            logger.warning("Nie udało się zgłosić tablicy %s: %s", code, exc)
