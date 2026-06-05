"""Seed demo data: whitelist plates and a batch of detection events.

Runs against the live backend over HTTP, so events go through the real
whitelist-resolution logic. Intended for filling the "Wykrycia" history during
development / demos — it is NOT part of the test suite.

Note: events are timestamped server-side ("now"), so all seeded rows land on
today's date (the POST API has no way to backdate created_at).

Examples
--------
    # inside the running stack
    docker compose exec backend python scripts/seed_events.py --events 200

    # from the host (needs httpx)
    python scripts/seed_events.py --events 200 --api http://localhost:8000/api
"""

import argparse
import logging
import random
import string
import sys

import httpx

logger = logging.getLogger("seed")

LABELS: list[str | None] = [
    "Auto firmowe",
    "Dostawca",
    "Pracownik",
    "Gość VIP",
    "Serwis",
    None,
]


def random_plate() -> str:
    """Generate a plate matching the Polish format ^[A-Z]{2}[0-9]{5}$."""
    letters = "".join(random.choices(string.ascii_uppercase, k=2))
    digits = "".join(random.choices(string.digits, k=5))
    return f"{letters}{digits}"


def seed_whitelist(client: httpx.Client, count: int) -> list[str]:
    """Create `count` unique whitelist plates; skip the rare collision/error."""
    plates: list[str] = []
    attempts = 0
    while len(plates) < count and attempts < count * 5:
        attempts += 1
        code = random_plate()
        if code in plates:
            continue
        response = client.post(
            "/plates/", json={"code": code, "label": random.choice(LABELS)}
        )
        if response.status_code == httpx.codes.CREATED:
            plates.append(code)
    return plates


def seed_events(
    client: httpx.Client, count: int, whitelist: list[str], allowed_ratio: float
) -> int:
    """Post `count` detections, some drawn from the whitelist. Returns #allowed."""
    allowed = 0
    for _ in range(count):
        if whitelist and random.random() < allowed_ratio:
            code = random.choice(whitelist)
        else:
            code = random_plate()
        response = client.post("/events/", json={"code": code})
        response.raise_for_status()
        if response.json()["allowed"]:
            allowed += 1
    return allowed


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    # Quiet per-request httpx logs; keep only our summary lines.
    logging.getLogger("httpx").setLevel(logging.WARNING)

    parser = argparse.ArgumentParser(description="Seed whitelist plates and events.")
    parser.add_argument("--events", type=int, default=200, help="detections to add")
    parser.add_argument("--whitelist", type=int, default=15, help="whitelist plates")
    parser.add_argument(
        "--allowed-ratio",
        type=float,
        default=0.4,
        help="fraction of events drawn from the whitelist (0..1)",
    )
    parser.add_argument(
        "--api",
        default="http://localhost:8000/api",
        help="backend API base URL",
    )
    args = parser.parse_args()

    try:
        with httpx.Client(base_url=args.api.rstrip("/"), timeout=10.0) as client:
            whitelist = seed_whitelist(client, args.whitelist)
            logger.info("Dodano %d tablic do whitelisty", len(whitelist))

            allowed = seed_events(client, args.events, whitelist, args.allowed_ratio)
            logger.info(
                "Dodano %d zdarzeń (%d dozwolonych, %d odrzuconych)",
                args.events,
                allowed,
                args.events - allowed,
            )
    except httpx.HTTPError as exc:
        logger.error("Błąd połączenia z backendem (%s): %s", args.api, exc)
        return 1

    logger.info("Gotowe.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
