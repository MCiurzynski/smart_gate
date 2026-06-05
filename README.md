<h1 align="center">
𓈈 Smart Gate App
</h1>

<div align="center">
🙋 <b>authors:</b> <a href="https://github.com/MCiurzynski">MCiurzynski</a> <a href="https://github.com/gwiazdan">gwiazdan</a> <a href="https://github.com/piatek5">piatek5</a><br/>
📆 <b>date:</b> 15-05-2026
</div>

## 🚀 Run the whole stack (Docker)

```bash
docker compose up --build
```

This starts Postgres, the FastAPI backend, and the frontend. Open
**http://localhost:5175** — the frontend is served by nginx, which proxies
`/api/*` to the backend container, so the browser stays same-origin (no CORS).

| Service  | URL                          |
|----------|------------------------------|
| Frontend | http://localhost:5175        |
| Backend  | http://localhost:8000/docs   |
| Postgres | localhost:5432               |

Stop with `docker compose down` (add `-v` to also drop the database volume).

## 🧑‍💻 Frontend development (hot reload)

To work on the UI with hot module reload, run the backend in Docker and the
frontend with Vite's dev server:

```bash
# Backend + database
docker compose up db backend

# Frontend dev server on http://localhost:5175
cd frontend
bun install
bun dev
```

In dev, Vite proxies `/api/*` to `http://localhost:8000` (override with
`VITE_API_PROXY_TARGET`, see `frontend/.env.example`).

The frontend follows a feature-based layout (inspired by
[fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices))
and the [2026-Boilerplate](https://github.com/bishopZ/2026-Boilerplate) conventions:

```
frontend/src/
├── config/            # typed env access
├── lib/               # api-client (typed fetch) + react-query client
├── features/plates/   # whitelist domain: api, hooks, types, components
├── features/events/   # detections/history domain (live-polling feed)
├── components/        # shared app shell (layout, error boundary)
├── pages/             # route-level, lazy-loaded screens
└── app-router.tsx     # React Router routes
```

## 🚗 Detections flow

The detector ([detector/](detector/)) recognises plates from a video/camera source
and reports each one to the backend:

```
detector  ──POST /api/events {code}──▶  backend resolves against the whitelist
          ◀──────────────────────────  stores AccessEvent (allowed / denied)
frontend  ──GET /api/events──────────▶  "Wykrycia" tab shows the live history
```

The **Wykrycia** tab has infinite scroll (loads more as you scroll) and filters by
plate number, label, status (allowed/denied) and date range. `GET /api/events/`
accepts `code`, `label`, `allowed`, `date_from`, `date_to`, `offset`, `limit`; the
returned `total` reflects the active filters (independent of the page).

### Seed demo data

To fill the whitelist and the **Wykrycia** history with realistic data (handy for
trying the infinite scroll and filters), run the seed script against the running
backend:

```bash
docker compose exec backend python scripts/seed_events.py --events 200
# options: --events N  --whitelist N  --allowed-ratio 0..1  --api <url>
```

It posts plates and detections over HTTP, so events go through the real
whitelist-resolution logic. (It is a dev/demo seed, **not** part of the test suite.
Seeded events are timestamped "now".)

The detector is **not** part of `docker compose` (it typically needs a GPU / camera).
Run it separately and point it at the backend via `BACKEND_URL` (default
`http://localhost:8000/api`, see `detector/.env.example`). With the backend
unreachable the detector logs a warning and keeps running.

<!-- ## 🚀 Quick Start -->
<!---->
<!-- ### Prerequisites -->
<!-- - Docker and Docker Compose installed -->
<!---->
<!-- ### Deployment -->
<!-- ```bash -->
<!-- git clone https://github.com/gwiazdan/odas-project.git -->
<!-- cd odas-project -->
<!---->
<!-- # Build containers -->
<!-- docker-compose build -->
<!---->
<!-- # Start the application -->
<!-- docker-compose up -->
<!---->
<!-- # Application is now available at https://localhost -->
<!-- ``` -->
