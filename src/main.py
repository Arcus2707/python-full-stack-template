"""FastAPI application factory and entrypoint."""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from logging.config import fileConfig
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from src import __version__
from src.auth.router import router as auth_router
from src.cache import configure_cache
from src.config import Settings, get_settings
from src.posts.router import router as posts_router
from src.templates import templates

logger = logging.getLogger("src.main")

LOGGING_CONFIG = Path(__file__).parent.parent / "logging.ini"


def configure_logging(settings: Settings) -> None:
    """Load logging configuration from ``logging.ini`` and apply the level."""
    if LOGGING_CONFIG.exists():
        fileConfig(LOGGING_CONFIG, disable_existing_loggers=False)
    logging.getLogger().setLevel(settings.log_level)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Configure resources on startup and clean up on shutdown."""
    settings = get_settings()
    configure_logging(settings)
    configure_cache(settings)
    logger.info("starting %s in %s mode", settings.name, settings.env.value)
    yield
    logger.info("shutting down")


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build and configure the FastAPI application."""
    settings = settings or get_settings()
    app = FastAPI(
        title=settings.name,
        version=__version__,
        debug=settings.debug,
        lifespan=lifespan,
    )
    app.include_router(auth_router)
    app.include_router(posts_router)

    @app.get("/health", tags=["health"])
    async def health() -> dict[str, str]:
        current = get_settings()
        return {
            "status": "ok",
            "environment": current.env.value,
            "version": __version__,
        }

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    async def index(request: Request) -> HTMLResponse:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"message": "Welcome to your full-stack template."},
        )

    return app


app = create_app()


def run() -> None:
    """Run the application with uvicorn (console-script entrypoint)."""
    settings = get_settings()
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=not settings.is_production,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    run()
