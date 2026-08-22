# Dependencies & Testing

## Dependency management with uv

Dependencies are declared in [`pyproject.toml`](../../pyproject.toml) and managed
with [uv](https://docs.astral.sh/uv/). uv creates the virtualenv, installs the
Python version pinned in `.python-version` (3.13.15), and resolves a lockfile
for reproducible builds.

```bash
make install        # uv sync --extra dev + install pre-commit hooks
make lock           # refresh uv.lock
```

Add a runtime dependency under `[project].dependencies` and a dev-only one under
`[project.optional-dependencies].dev`, then run `make install`. Do not use `pip`
directly.

### Versioning

Versions are derived automatically from git tags by
[setuptools-scm](https://setuptools-scm.readthedocs.io/) — there is no hardcoded
version string. Tagging `v1.2.3` produces version `1.2.3`; commits after a tag
get a development version. CI checks out full history (`fetch-depth: 0`) so the
version resolves correctly.

## Testing with pytest

Tests live in [`tests/`](../../tests) and run through the Makefile:

```bash
make test           # pytest with coverage
make test-cov       # HTML + XML coverage reports
make check          # lint + type-check + test
```

Configuration is in `[tool.pytest.ini_options]`:

- `pytest-asyncio` in `auto` mode — `async def` tests run without extra markers
- `pythonpath = ["."]` so `import src` works without installation
- coverage enabled by default via `--cov=src`

### Fixtures

[`tests/conftest.py`](../../tests/conftest.py) provides:

- `client` — an `httpx.AsyncClient` bound to the ASGI app, wired to the test
  database via a `get_db` dependency override
- `db_session` — an isolated session on a shared in-memory SQLite engine
- `engine` / `session_factory` — the underlying test engine and factory
- automatic reset of the settings and domain-config caches between tests

### Coverage

Coverage is configured in `[tool.coverage.*]` with branch coverage and
`concurrency = ["multiprocessing", "thread"]` for multiprocess and distributed
apps. Combine partial data with `coverage combine` (wired into `make test-cov`).
