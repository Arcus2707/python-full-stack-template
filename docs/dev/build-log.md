# Backend Build-Out Log

This document records how the `python-full-stack-template` backend was built,
in two phases: (1) the initial scaffold and (2) the restructure into a
domain-driven layout. It lists the steps taken, the errors hit along the way,
and how each was resolved.

## Phase 1 — Initial backend scaffold

**Goal:** stand up a full-featured FastAPI backend under `src/app` with uv,
Ruff, mypy, pytest, Pydantic Settings, SQLAlchemy + Alembic, Celery, aiocache,
Jinja2, Docker, GitHub Actions CI/CD, and documentation.

### Steps

1. Created root tooling: `.python-version` (3.13.15), `pyproject.toml`
   (setuptools + setuptools-scm build backend, Ruff/mypy/pytest/coverage
   config), `Makefile`, `.pre-commit-config.yaml`, `.prettierrc`,
   `.prettierignore`, `.dockerignore`, `.env.example`.
2. Built the `src/app` package: `settings.py` (Pydantic Settings),
   `logging.py`, `db/` (base, session, models), `cache/` (aiocache),
   `tasks/` (Celery app + example tasks), `templates/` (Jinja2 environment +
   HTML templates), `api/` (deps + routers for health/items), `web/`
   (server-rendered route), `main.py` (app factory).
3. Added Alembic (`migrations/env.py`, `script.py.mako`) wired to the async
   engine and application settings.
4. Added `tests/` with `conftest.py` fixtures (`client`, `db_session`) and
   tests for health and settings.
5. Added Docker: multi-stage production `Dockerfile`, `Dockerfile.dev`,
   `docker-compose.yml` + `docker-compose.dev.yml`.
6. Added CI/CD: `.github/workflows/ci.yml`, `publish.yml`, `docker.yml`, and
   `.github/dependabot.yml`.
7. Wrote the developer guide hub in `docs/dev/` (settings, FastAPI, database,
   caching, tasks, docker, dependencies & testing) and a project `README.md`.
8. Verified everything with `uv sync`, `ruff check`/`format`, `mypy`,
   `pytest`, `prettier`, and `uv build`.

### Errors encountered and fixes

| #   | Error                                                                                                     | Cause                                                                                                                                            | Fix                                                                                                                                                                                              |
| --- | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | Ruff `S704`: unsafe use of `markupsafe.Markup`                                                            | The `highlight` Jinja2 filter wrapped escaped text in `Markup()`, which Ruff flags as a potential XSS sink by default                            | Confirmed both inputs were already HTML-escaped before wrapping, then added a targeted `# noqa: S704` with a one-line comment explaining why it's safe                                           |
| 2   | Ruff `RUF100`: unused `noqa` directives in `tests/conftest.py`                                            | `# noqa: E402` was added defensively next to imports that Ruff didn't actually flag for E402                                                     | Ran `ruff check --fix` to strip the unused directives                                                                                                                                            |
| 3   | mypy `untyped-decorator` on Celery `@celery_app.task`                                                     | Celery's task decorator has no type stubs, so mypy treated decorated functions as untyped under `strict = true`                                  | Added a `[[tool.mypy.overrides]]` entry disabling `disallow_untyped_decorators` for the tasks module only                                                                                        |
| 4   | mypy `call-overload` on `Jinja2Templates(directory=..., autoescape=..., auto_reload=..., cache_size=...)` | FastAPI's `Jinja2Templates` overloads don't accept those Jinja2-specific kwargs directly                                                         | Built a `jinja2.Environment` explicitly (with `FileSystemLoader`, `select_autoescape`, `auto_reload`, `cache_size`) and passed it via `Jinja2Templates(env=env)`, which matches a typed overload |
| 5   | Misleading `exit code 1` from `uv sync` / `uv build` / `pytest` in PowerShell                             | uv writes normal build/progress banners to stderr, which PowerShell's `NativeCommandError` reporting surfaces as a non-zero exit even on success | Learned to check `$LASTEXITCODE` explicitly rather than trusting the wrapper's reported exit code                                                                                                |

All checks passed after fixes: Ruff, Ruff format, mypy (strict, 20 files),
pytest (4 passed), prettier, and `uv build` (version `0.1.0` derived from a
git tag via setuptools-scm).

## Phase 2 — Restructure to a domain-driven layout

**Goal:** reorganize the backend from a single `src/app` package into the
`fastapi-best-practices` domain-driven layout, with `src` as the package root,
per-domain packages (`auth`, `aws`, `posts`), global modules at the top level,
and `alembic/`, `templates/`, and `logging.ini` at the repo root.

### Steps

1. Mapped every old module to its new location (see mapping below) and wrote
   the plan to session memory before making changes.
2. Created global modules directly under `src/`: `config.py` (was
   `app/settings.py`), `database.py` (was `app/db/session.py`, now also
   exposes `get_db`/`DbSession`), `models.py` (was `app/db/base.py`),
   `exceptions.py` and `pagination.py` (new shared primitives), `cache.py`,
   `worker.py` (Celery, was `app/tasks/celery_app.py`), `templates.py`,
   `main.py`.
3. Built the **auth** domain: `router.py`, `schemas.py`, `models.py` (`User`),
   `dependencies.py`, `config.py`, `constants.py`, `exceptions.py`,
   `service.py`, `utils.py` — password hashing via stdlib `scrypt` and JWTs via
   the new `pyjwt` dependency.
4. Built the **aws** domain as an external-service example: `client.py`,
   `schemas.py`, `config.py`, `constants.py`, `exceptions.py`, `utils.py` — a
   dependency-free stub client demonstrating the pattern.
5. Built the **posts** domain as an API endpoint example: `router.py`,
   `schemas.py`, `models.py` (`Post`), `dependencies.py`, `constants.py`,
   `exceptions.py`, `service.py`, `utils.py`, using the new `pagination`
   helpers.
6. Renamed `migrations/` to `alembic/`, updated `alembic.ini`
   (`script_location = alembic`), and updated `alembic/env.py` to import
   `Base` from `src.models` plus every domain's models.
7. Moved templates to a root-level `templates/` directory and logging config
   to a root-level `logging.ini`, loaded via `logging.config.fileConfig` in
   `src/main.py`.
8. Rewrote `tests/conftest.py` fixtures around a shared in-memory SQLite
   engine (`StaticPool`) and a `get_db` dependency override, and added
   per-domain test packages: `tests/auth`, `tests/aws`, `tests/posts`, plus
   `tests/test_main.py` for the app/settings-level checks. Deleted the old
   `tests/test_health.py` and `tests/test_settings.py`.
9. Updated all tooling and config for the new layout: `pyproject.toml`
   (package discovery, `pyjwt` dependency, Ruff/mypy/pytest/coverage paths),
   `Makefile` (app target, Celery, schema generation commands), both
   Dockerfiles and both Compose files (copy/mount paths, `logging.ini`,
   `alembic`, `templates`), `AGENTS.md`, `README.md`, and every guide in
   `docs/dev/`.
10. Re-ran the full verification loop (`uv sync`, Ruff, mypy, pytest,
    prettier, `uv build`, plus manual import/route smoke tests) until clean.

### Mapping reference

| Old (`src/app`)           | New (`src`)                                                                                 |
| ------------------------- | ------------------------------------------------------------------------------------------- |
| `app.settings`            | `src.config`                                                                                |
| `app.db.session`          | `src.database`                                                                              |
| `app.db.base`             | `src.models`                                                                                |
| `app.db.models.item.Item` | `src.posts.models.Post`                                                                     |
| `app.cache`               | `src.cache`                                                                                 |
| `app.tasks.celery_app`    | `src.worker`                                                                                |
| `app.templates`           | `src.templates` (+ root `templates/index.html`)                                             |
| `app.main`                | `src.main`                                                                                  |
| `app.api.deps`            | split into `src.database.DbSession`, `src.cache.CacheDep`, and per-domain `dependencies.py` |
| `app/logging.py`          | root `logging.ini`                                                                          |
| `migrations/`             | `alembic/`                                                                                  |

### Errors encountered and fixes

| #   | Error                                                                                                       | Cause                                                                                                                                                                             | Fix                                                                                                                                                               |
| --- | ----------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Ruff `RUF100`: unused `noqa: E402` directives in the rewritten `tests/conftest.py`                          | Copy-pasted `noqa` comments from the old conftest no longer matched what Ruff flagged after reordering imports                                                                    | `ruff check --fix` removed the stale directives automatically                                                                                                     |
| 2   | Ruff `S105`: "possible hardcoded password" on `INVALID_TOKEN` message string and `token_type = "bearer"`    | Bandit's heuristic flags any identifier containing `token`/`password`-like names assigned to a string literal, even for non-secret values                                         | Added targeted `# noqa: S105` with a one-line justification (error message / OAuth2 token-type label, not a secret)                                               |
| 3   | Ruff `UP046`: `Page(BaseModel, Generic[M])` should use PEP 695 type parameters                              | Ruff's pyupgrade rules flag legacy `typing.Generic` subclassing under a `target-version = "py313"` config                                                                         | Rewrote as `class Page[M](BaseModel)` and dropped the now-unused `TypeVar` import                                                                                 |
| 4   | mypy `untyped-decorator` on the relocated `@celery_app.task` in `src/worker.py`                             | Same root cause as Phase 1, but the override needed to be re-targeted after the module moved from `app.tasks.*` to `src.worker`                                                   | Updated the `[[tool.mypy.overrides]]` `module` list to `["src.worker"]`                                                                                           |
| 5   | Stale `paracelsus.*` mypy override reported as "unused section(s)"                                          | The override was added defensively but paracelsus is only invoked via the Makefile (`make schema`), never imported directly, so mypy never needed the override                    | Removed the unused override entry                                                                                                                                 |
| 6   | JWT `InsecureKeyLengthWarning` during auth tests                                                            | The test `.env`-equivalent secret (`APP_AUTH_SECRET_KEY`) was a short placeholder string, below HMAC-SHA256's recommended 32-byte minimum                                         | Lengthened the test secret keys in `tests/conftest.py` to 32+ characters                                                                                          |
| 7   | `AttributeError: '_IncludedRouter' object has no attribute 'path'` during a manual route-listing smoke test | Starlette 1.6 wraps `include_router()` mounts as `_IncludedRouter` objects (no `.path` attribute) until routes are resolved at request time; this is expected behavior, not a bug | Verified route registration instead via the passing integration tests (`tests/auth`, `tests/posts`) rather than introspecting `app.routes` directly               |
| 8   | Docs, `AGENTS.md`, and Docker/Compose files referenced old `app.*` module paths and `migrations/`           | Bulk restructure of source code wasn't automatically reflected in prose documentation or path-based config                                                                        | Searched (`grep`) for lingering `app.`/`src/app`/`migrations/` references across `docs/`, `README.md`, `AGENTS.md`, and Docker files, and updated each occurrence |
| 9   | Prettier flagged reformatted/newly-edited docs after content updates                                        | Manual markdown edits didn't match Prettier's formatting rules (line wrapping, list spacing)                                                                                      | Ran `prettier --write` over `**/*.{yml,yaml,json,md}` and re-verified with `--check`                                                                              |

All checks passed after fixes: Ruff, Ruff format, mypy (strict, 36 files),
pytest (17 passed, 85% coverage), prettier, and `uv build` (version resolved
via setuptools-scm from the existing git tag plus commit metadata).

## Lessons learned

- **uv's stderr banners can look like failures in PowerShell.** Always check
  `$LASTEXITCODE` (or run the command directly) instead of trusting a
  wrapper's `NativeCommandError` noise.
- **Bandit-style rules (`S1xx`) flag by name, not by value.** Fields or
  constants named `token`, `password`, `secret`, etc. get flagged even when
  they hold non-sensitive labels or messages — suppress with a narrow,
  justified `# noqa` rather than disabling the rule globally.
- **Keep mypy overrides scoped to the actual importing module.** When code
  moves (e.g. `app.tasks.celery_app` → `src.worker`), override `module` lists
  must move with it, and unused overrides should be pruned to avoid mypy
  "unused section" notices.
- **Test secrets need to satisfy the same validation as production values.**
  Short placeholder secrets can trigger library-level warnings (e.g. PyJWT's
  key-length warning); use realistic-length dummy values in tests.
- **A restructure isn't done until docs and infra config are updated too.**
  Grep broadly across `docs/`, `AGENTS.md`, `Makefile`, and Docker/Compose
  files for old module/path references after any package rename.
