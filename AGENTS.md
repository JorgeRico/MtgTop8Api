# AGENTS.md — MtgTop8Api

## Repository purpose
Public FastAPI + Supabase (PostgreSQL) API serving Magic: The Gathering tournament/league stats for the MTG Stats website. Python backend, deployed on Vercel.

## Tech stack
- Language: Python 3.11 (Dockerfile base: `python:3.11-slim`)
- Framework: FastAPI
- Database: Supabase / PostgreSQL (supabase-py client)
- Caching: cachetools TTLCache
- Server: uvicorn
- Config: python-dotenv (.env)
- Validation: Pydantic v2 (BaseModel + Field constraints)

## Project layout (api/)
```
app.py              # FastAPI app, CORS, routers, root + /health
cache.py            # Shared TTLCache + async-compatible cached decorator
codes/codes.py      # HTTP status + option string constants
errors/errors.py    # 404 exception handler
routers/*.py        # API route modules (tournaments, decks, leagues, players)
schemas/*.py        # Pydantic models with Field constraints
queries/supabase/*.py  # Supabase data access classes
db/supabase/db.py   # Singleton Supabase client wrapper
db/mysql/db.py      # Legacy MySQL wrapper (not active)
requirements.txt    # fastapi, uvicorn, supabase, cachetools, python-dotenv
Dockerfile / docker-compose.yml / vercel.json
```

## Coding rules & conventions

### 1. API versioning
All routers are mounted under `/api/v1/<resource>`. Do not mount new routes at the top-level `/api/` without updating all four routers consistently. Add a root `/` endpoint exposing `name`/`version`/`docs`/`health`.

### 2. Pydantic schemas
Every response shape must be a Pydantic `BaseModel` in `schemas/` using `Field` constraints:
- `id` fields: `Field(gt=0)`
- strings: `Field(min_length=1)`
- counts: `Field(ge=0)`
- years: `Field(ge=1900, le=2100)`
- booleans stored as int: `Field(ge=0, le=1)`

### 3. Database access
- `Db` is a **singleton** (`db/supabase/db.py`) — instantiate once, reuse the Supabase client. Do not create `Db()` per query.
- `load_dotenv()` runs once at module import, not per request.
- All query methods are `async` and return `response.data` (never the raw Supabase response object).
- Guard empty results before indexing `result.data[0]`; return `None` or `[]` so routers can raise 404.

### 4. Caching
- Use the shared `cache` instance from `cache.py` (TTLCache, maxsize=1000, ttl=300s).
- Use the `cached(cache)` decorator (async-compatible wrapper), **not** `cachetools.cached` directly on async functions.
- One cache is shared across all routers; do not create per-router `TTLCache` instances.

### 5. Routers
- One router file per resource: `router_tournaments.py`, `router_decks.py`, `router_leagues.py`, `router_players.py`.
- Prefix each router with `/api/v1/<resource>`.
- Use `Path(gt=0)` for ID path parameters.
- Use unique function names per route (do not reuse `getLeagueData` across multiple routes).
- Raise `HTTPException(status_code=HTTP_404, detail=...)` for missing items; never reference undefined variables in guards.

### 6. CORS
- Origins come from `ALLOWED_ORIGINS` env var (comma-separated), default `https://mtg-stats.vercel.app,http://localhost:3000`.
- Never use `allow_origins=["*"]` in production.
- Limit methods to `["GET", "POST", "PUT", "DELETE", "OPTIONS"]` and headers to `["Content-Type", "Authorization", "Accept"]`.

### 7. Docker / deployment
- Base image: `python:3.11-slim` (not EOL `3.10-slim-buster`).
- CMD: `uvicorn app:app --host=0.0.0.0` — **no** `--reload` in production.
- `.dockerignore` excludes `__pycache__/`, `*.pyc`, `.env`, `.git/`, docs, Docker/compose/vercel files.

### 8. Environment
Required env vars: `SUPABASE_URL`, `SUPABASE_KEY`, `ALLOWED_ORIGINS` (optional).
`.env` is gitignored — never commit real Supabase keys.

### 9. Testing / quality
- No test suite exists yet (`test` script is a stub). Add tests under `tests/` when modifying behavior.
- Run the API locally: `uvicorn app:app` (or `docker-compose up -d`).

## Pull request rules
- Create a new branch per improvement/fix.
- Open a PR against `main`; do not merge — wait for review.
- Keep PRs small and single-purpose.