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
├── features/plates/   # plates domain: api, hooks, types, components
├── components/        # shared app shell (layout, error boundary)
├── pages/             # route-level, lazy-loaded screens
└── app-router.tsx     # React Router routes
```

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
