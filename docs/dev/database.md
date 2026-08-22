# Database

Persistence uses [SQLAlchemy 2.0](https://docs.sqlalchemy.org/) (async) with
[Alembic](https://alembic.sqlalchemy.org/) for migrations.

## Model organization

- [`src/models.py`](../../src/models.py) — the global declarative `Base` and a
  `TimestampMixin`
- Each domain declares its models in `<domain>/models.py` inheriting from
  `Base` (e.g. [`src/posts/models.py`](../../src/posts/models.py),
  [`src/auth/models.py`](../../src/auth/models.py))
- Alembic imports every domain model in
  [`alembic/env.py`](../../alembic/env.py) so a single metadata is shared and
  autogenerate sees all tables

Add a new model by creating it in a domain package:

```python
# src/posts/models.py
from src.models import Base, TimestampMixin

class Post(Base, TimestampMixin):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
```

Then import it in `alembic/env.py`:

```python
from src.posts.models import Post  # noqa: F401
```

## Sessions

The async engine and session factory live in
[`src/database.py`](../../src/database.py). In FastAPI, inject `DbSession`;
elsewhere use the `session_scope()` context manager:

```python
from src.database import DbSession, session_scope

async with session_scope() as session:
    session.add(obj)
```

## Migrations (via Make)

```bash
make migration m="add posts table"    # autogenerate a revision
make migrate                           # upgrade to head
make downgrade                         # step back one revision
```

Alembic is configured for async in [`alembic/env.py`](../../alembic/env.py) and
reads the database URL from application settings. Revisions are written to
`alembic/versions/` and auto-formatted with Ruff.

## Schema diagram

Generate an entity-relationship diagram with
[Paracelsus](https://github.com/tedivm/paracelsus):

```bash
make schema   # writes docs/dev/schema.mermaid
```

Embed the resulting Mermaid file in docs or your README to keep a live schema
diagram in version control.
