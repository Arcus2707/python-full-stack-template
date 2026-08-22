# Task Processing

Background and scheduled work is handled by [Celery](https://docs.celeryq.dev/),
configured in [`src/worker.py`](../../src/worker.py).

## Celery

The broker and result backend default to Redis (`APP_CELERY_BROKER_URL`,
`APP_CELERY_RESULT_BACKEND`). Tasks are JSON-serialized.

### Defining tasks

Add tasks to [`src/worker.py`](../../src/worker.py) (or a domain module imported
there):

```python
@celery_app.task(name="src.worker.add")
def add(x: int, y: int) -> int:
    return x + y
```

Enqueue from application code:

```python
from src.worker import add
result = add.delay(2, 3)
```

### Worker configuration

```bash
make worker   # celery -A src.worker worker --loglevel=info
```

Key options set in `celery_app.conf`: `task_track_started`, a 300s
`task_time_limit`, `worker_max_tasks_per_child=1000` (guards against memory
leaks) and `result_expires=3600`.

### Beat (scheduled tasks)

Periodic tasks are declared in `celery_app.conf.beat_schedule`. Run the
scheduler with:

```bash
make beat     # celery -A src.worker beat --loglevel=info
```

### Docker

The `worker` and `beat` services in
[`docker/docker-compose.yml`](../../docker/docker-compose.yml) run alongside
`web`, sharing the same image and Redis broker. Start everything with
`make docker-up`.

## QuasiQueue (optional)

For lightweight, file-driven queues you can add
[QuasiQueue](https://github.com/tedivm/quasiqueue). Point it at a configuration
file (e.g. `quasiqueue.toml`) and run its container image next to the `worker`
service in Compose. It is not enabled by default in this template.
