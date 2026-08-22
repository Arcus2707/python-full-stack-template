# AGENTS.md

Guidance for AI coding agents (GitHub Copilot, Cursor, Aider, Devin, and others)
working in this repository. Follows the [agents.md](https://agents.md/) open standard.

## Project overview

A Python full-stack application template. The backend lives under `src` and is
built on FastAPI, SQLAlchemy (async), Celery, aiocache and Jinja2. Configuration
is managed with Pydantic Settings. Code is organized by **domain** (a
package per feature), following the
[fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices)
layout.

## Project structure

- `src/main.py` — FastAPI application factory (`create_app`) and lifespan
- `src/config.py` — global Pydantic `Settings` (`get_settings()`)
- `src/database.py` — async engine, `SessionFactory`, `get_db` / `DbSession`
- `src/models.py` — global declarative `Base` and `TimestampMixin`
- `src/exceptions.py` — global exception hierarchy (`DetailedHTTPException`, …)
- `src/pagination.py` — `PaginationParams`, `Page[M]`, `PaginationDep`
- `src/cache.py`, `src/worker.py`, `src/templates.py` — aiocache, Celery, Jinja2
- Domain packages (`src/auth`, `src/aws`, `src/posts`) each contain, as needed:
  `router.py`, `schemas.py`, `models.py`, `service.py`, `dependencies.py`,
  `config.py`, `constants.py`, `exceptions.py`, `utils.py` (and `client.py` for
  external services). Import paths are `src.<domain>.<module>`.
- `alembic/` — migration environment; `templates/` — Jinja2 HTML;
  `logging.ini` — logging config; `tests/<domain>/` — per-domain tests

## Environment & tooling

- **Python:** 3.13.15 (pinned in `.python-version`). Do not use features beyond
  the target version and do not lower the version.
- **Package manager:** [uv](https://docs.astral.sh/uv/). Never call `pip`
  directly. Add dependencies to `pyproject.toml` and run `uv sync`.
- **Task runner:** `make`. Common commands:
  - `make install` — create the venv and install dev dependencies
  - `make test` — run the test suite with coverage
  - `make lint` — Ruff, prettier, and mypy checks
  - `make format` — auto-format code and config files
  - `make run` — start the FastAPI dev server
  - `make migration m="msg"` / `make migrate` — Alembic migrations
  - `make publish` — build and publish to PyPI

## Coding conventions

- **Async first:** prefer `async`/`await` for I/O (DB, cache, HTTP). Use the
  async SQLAlchemy session from `src.database` and async cache from `src.cache`.
- **Typing:** full type annotations are required. `mypy` runs in strict mode.
  Use `from __future__ import annotations` and modern syntax (`str | None`,
  built-in generics, PEP 695 `class Page[M]`). Add types rather than
  `# type: ignore`.
- **Formatting & linting:** Ruff is the single source of truth (line length
  100). Run `make format` before committing.
- **Settings:** never read `os.environ` directly in application code. Add a
  typed field to `src.config.Settings` (or a domain `config.py`) and access it
  via `get_settings()`.
- **Pydantic v2:** use `model_config`, `model_dump()`, `ConfigDict`. Do not use
  deprecated v1 APIs.
- **FastAPI:** keep a domain's HTTP layer in `router.py`, business logic in
  `service.py`, and reusable dependencies in `dependencies.py`. Inject
  `DbSession` (from `src.database`) and `CacheDep` (from `src.cache`).

## Security practices

- Never commit secrets. Use `.env` (git-ignored); `.env.example` documents the
  variables. Gitleaks runs as a pre-commit hook.
- Jinja2 autoescaping is enabled — do not disable it or mark untrusted input as
  safe. Escape explicitly when building markup.
- Validate all external input at the boundary with Pydantic models.
- Ruff's bandit (`S`) rules are enabled; address findings rather than ignoring.

## Testing

- Framework: `pytest` with `pytest-asyncio` (auto mode) and `pytest-cov`.
- Tests live in `tests/`. Use the `client` and `db_session` fixtures from
  `tests/conftest.py`. Tests run against in-memory SQLite.
- Add or update tests for every behavioral change. Keep coverage from
  regressing. Run `make test` before finishing.

## Framework notes

- **SQLAlchemy/Alembic:** declare domain models in `src/<domain>/models.py`
  inheriting from `src.models.Base`, and import them in `alembic/env.py` so
  autogenerate discovers them. Generate migrations with `make migration m="..."`;
  never hand-edit applied revisions.
- **Celery:** register tasks in `src/worker.py` (or import them there). Keep
  tasks idempotent and JSON-serializable.
- **aiocache:** use the `CacheDep` dependency or `get_cache()`; prefer explicit
  TTLs from settings.

## Pull request expectations

- Run `make check` (lint + tests) and ensure it passes.
- Keep changes focused; do not introduce unrelated refactors.
- Versioning is automatic via setuptools-scm from git tags — do not edit
  version strings by hand.
