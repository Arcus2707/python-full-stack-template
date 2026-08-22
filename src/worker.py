"""Celery application, configuration and example tasks."""

from __future__ import annotations

from celery import Celery

from src.config import get_settings

settings = get_settings()

celery_app = Celery(
    "app",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,
    worker_max_tasks_per_child=1000,
    result_expires=3600,
)

celery_app.conf.beat_schedule = {
    "heartbeat-every-minute": {
        "task": "src.worker.heartbeat",
        "schedule": 60.0,
    },
}


@celery_app.task(name="src.worker.add")
def add(x: int, y: int) -> int:
    """Add two numbers. Serves as a minimal task example."""
    return x + y


@celery_app.task(name="src.worker.heartbeat")
def heartbeat() -> str:
    """Wired to Celery beat as a periodic task."""
    return "ok"
