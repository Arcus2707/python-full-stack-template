# Settings

Global configuration is managed by
[Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
in [`src/config.py`](../../src/config.py). All values are typed and validated at
startup, so a misconfigured deployment fails fast with a clear error instead of
breaking at runtime.

Domain-specific configuration lives in each package's `config.py` (for example
[`src/auth/config.py`](../../src/auth/config.py) and
[`src/aws/config.py`](../../src/aws/config.py)), each with its own env prefix.

## How it loads

Values are resolved in priority order:

1. Environment variables (global prefix `APP_`; domain prefixes such as
   `APP_AUTH_`, `APP_AWS_`)
2. A local `.env` file (see `.env.example`)
3. Defaults declared on the settings class

```python
from src.config import get_settings

settings = get_settings()  # cached singleton
print(settings.env, settings.port)
```

`get_settings()` is cached with `lru_cache`. In tests call
`get_settings.cache_clear()` to force a reload.

## Environment-based configuration

The `env` field is an `Environment` enum (`development`, `staging`,
`production`, `testing`). Switch environments purely through variables:

```bash
APP_ENV=production APP_DEBUG=false uv run app
```

Use `settings.is_production` for environment-specific behavior (e.g. template
caching, reload).

## Adding a setting

Add a typed field with a sensible default to `Settings` (global) or a domain
config class:

```python
class Settings(BaseSettings):
    feature_flag: bool = False
    max_items: int = Field(default=100, ge=1)
```

It is automatically populated from `APP_FEATURE_FLAG` / `APP_MAX_ITEMS`.

## Validation

Fields use standard Pydantic validation (`ge`, `le`, `Literal`, custom
validators). Invalid values raise `ValidationError` at construction, which
prevents booting with a broken configuration. Secrets use `SecretStr` so they
are never accidentally logged.
