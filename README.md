# Review site

Log, rate, and review the games you play. See [review-site-plan.md](review-site-plan.md) for the plan.

## Layout

- `api/`: FastAPI backend (Python 3.13, managed by uv)
- `web/`: Next.js front end (TypeScript, Tailwind)
- `docker-compose.yml`: Postgres (with pgvector) and Redis for local development

## Running locally

Start Docker Desktop first. Then, from the project root:

```
docker compose up -d --wait
```

API (port 8001, because another local project uses 8000):

```
cd api
cp .env.example .env
uv run alembic upgrade head
uv run uvicorn app.main:app --reload --port 8001
```

Web (port 3000):

```
cd web
cp .env.example .env.local
npm install
npm run dev
```

Open http://localhost:3000. The home page shows whether the API can reach Postgres and Redis.

## Checks

```
cd api && uv run ruff check . && uv run ruff format --check . && uv run pytest
cd web && npm run lint && npm run typecheck
```

## Stopping

```
docker compose stop      # keep data
docker compose down -v   # delete all local data
```
