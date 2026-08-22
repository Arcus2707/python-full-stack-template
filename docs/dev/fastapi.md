# FastAPI

The application is built with [FastAPI](https://fastapi.tiangolo.com/). The app
is created by a factory in [`src/main.py`](../../src/main.py) so it can be
instantiated with custom settings in tests.

## Structure

Code is organized by domain (`src/auth`, `src/posts`, ...). Each domain keeps
its HTTP layer in `router.py`, business logic in `service.py`, and reusable
dependencies in `dependencies.py`. Routers are included in `create_app()`:

```python
app.include_router(auth_router)
app.include_router(posts_router)
```

## Dependency system

Use the typed dependency aliases instead of wiring things manually:

```python
from src.database import DbSession       # request-scoped AsyncSession
from src.cache import CacheDep           # shared aiocache instance
from src.pagination import PaginationDep # validated limit/offset
from src.auth.dependencies import CurrentUser  # authenticated user

@router.get("/example")
async def example(db: DbSession, user: CurrentUser) -> dict[str, str]:
    ...
```

- `DbSession` — a request-scoped async SQLAlchemy session (commits on success,
  rolls back on error), defined in [`src/database.py`](../../src/database.py)
- `CacheDep` — the shared aiocache instance
- Domain dependencies (e.g. `ValidPost`, `CurrentUser`) resolve and validate
  path resources or the current user

## Server-side rendering

The root `/` route renders Jinja2 templates for hybrid API + HTML apps. The
environment is configured in [`src/templates.py`](../../src/templates.py):
autoescaping is on for XSS protection, templates auto-reload in development and
are cached in production. Custom filters (`currency`, `datetimeformat`,
`highlight`) and globals (`now`, `app_name`) are pre-registered. Template files
live in the repository-root [`templates/`](../../templates) directory.

## Static files

To serve static assets, mount `StaticFiles` in `create_app()`:

```python
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")
```

## Running

```bash
make run                       # uvicorn with reload
uv run app                     # console-script entrypoint (src.main:run)
```

Interactive API docs are available at `/docs` and `/redoc`.
