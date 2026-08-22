# Developer Guide

Documentation hub for the backend. Each guide covers one enabled feature and
how to work with it.

## Guides

- [Settings](settings.md) — Pydantic Settings configuration system
- [FastAPI](fastapi.md) — app structure, dependencies and static files
- [Database](database.md) — SQLAlchemy models, Alembic migrations, diagrams
- [Caching](caching.md) — aiocache integration and decorators
- [Tasks](tasks.md) — Celery workers and beat scheduling
- [Docker](docker.md) — images, local stack and registry publishing
- [Dependencies & Testing](dependencies-testing.md) — uv and pytest via Make

## Quick start

```bash
make install     # create venv (uv) and install dev deps + pre-commit
cp .env.example .env
make run         # start the FastAPI dev server on :8000
make test        # run the test suite
```

## Project layout

The backend follows the domain-driven
[fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices)
layout: `src` is the package and each feature is its own sub-package.

```text
src/
  auth/         auth domain (router, service, models, schemas, ...)
  aws/          example external-service client
  posts/        example API endpoint domain
  config.py     global Pydantic Settings
  database.py   async engine, session factory, get_db dependency
  models.py     global declarative Base + TimestampMixin
  exceptions.py global exception hierarchy
  pagination.py PaginationParams / Page[M] helpers
  cache.py      aiocache configuration
  worker.py     Celery app and tasks
  templates.py  Jinja2 environment
  main.py       application factory
alembic/        Alembic environment and revisions
templates/      Jinja2 HTML templates
tests/          pytest suite (auth/, aws/, posts/)
logging.ini     logging configuration
```

Each domain package contains the files it needs from this set: `router.py`,
`schemas.py` (Pydantic models), `models.py` (DB models), `service.py` (business
logic), `dependencies.py`, `config.py` (local config), `constants.py`,
`exceptions.py`, `utils.py`, and `client.py` for external services.
