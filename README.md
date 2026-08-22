# Python Full-Stack Template

A batteries-included template for building production-ready Python full-stack
applications. The backend lives under [`src`](src) and is built on
FastAPI, SQLAlchemy (async), Celery, aiocache and Jinja2, with a modern tooling
stack (uv, Ruff, mypy, pytest, pre-commit). Code is organized by **domain**
following the
[fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices)
layout.

- **Python:** 3.13.15 (pinned in [`.python-version`](.python-version))
- **Packaging:** [`pyproject.toml`](pyproject.toml) with setuptools-scm
  git-tag versioning
- **Task runner:** [`Makefile`](Makefile)

## Quick start

```bash
make install          # create venv (uv), install dev deps, install pre-commit
cp .env.example .env
make run              # FastAPI dev server on http://localhost:8000
make test             # run the test suite with coverage
make check            # lint + type-check + test
```

Prefer containers?

```bash
make docker-up        # web + worker + beat + postgres + redis (hot reload)
```

## Features

- **FastAPI** application factory with a typed dependency system and
  server-side rendering via **Jinja2** (autoescaping/XSS protection, custom
  filters, dev auto-reload, prod caching)
- **SQLAlchemy 2.0** async models with **Alembic** migrations (`make migration`)
  and Paracelsus schema diagrams (`make schema`)
- **Celery** workers and beat scheduling; **aiocache** Redis caching
- **Pydantic Settings** for type-safe, environment-based, validated config
- **uv** for fast, reproducible dependency management and virtualenvs
- **Ruff** (lint + format), **mypy** (strict), **pytest** + coverage,
  **pre-commit** hooks, and **prettier** for YAML/JSON/Markdown
- **Docker**: multi-stage prod image (non-root, healthcheck, multi-arch) and a
  dev image with hot reload; Compose orchestration for the full stack
- **CI/CD** with GitHub Actions: quality gate, PyPI trusted publishing on tags,
  multi-arch image publishing to GHCR/Docker Hub, and Dependabot updates
- **AI-ready**: an [`AGENTS.md`](AGENTS.md) following the
  [agents.md](https://agents.md/) standard

## Documentation

See the developer guide hub in [`docs/dev/`](docs/dev/index.md):

- [Settings](docs/dev/settings.md)
- [FastAPI](docs/dev/fastapi.md)
- [Database](docs/dev/database.md)
- [Caching](docs/dev/caching.md)
- [Tasks](docs/dev/tasks.md)
- [Docker](docs/dev/docker.md)
- [Dependencies & Testing](docs/dev/dependencies-testing.md)

## License

See [LICENSE](LICENSE).
