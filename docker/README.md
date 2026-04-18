# Docker

`docker-compose.yml` at the repository root defines the local development stack:

- `postgres` for application persistence
- `redis` for broker/cache support
- `backend` for the FastAPI API, including Alembic migration startup
- `celery_worker` for CSV import background work
- `frontend` for the Next.js dashboard

Run from the repository root:

```powershell
docker compose up --build
```

The default ports are:

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`
