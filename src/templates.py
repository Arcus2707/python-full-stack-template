"""Jinja2 templating configured for FastAPI server-side rendering.

Autoescaping is enabled for HTML to provide built-in XSS protection. In
development templates auto-reload; in production the bytecode cache is enabled
for faster rendering. Application-specific filters and globals are registered
here. Template files live in the repository-root ``templates/`` directory.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup, escape

from src.config import Settings, get_settings

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"


def _currency(value: float, symbol: str = "$") -> str:
    """Format a number as a currency string."""
    return f"{symbol}{value:,.2f}"


def _datetimeformat(value: datetime, fmt: str = "%Y-%m-%d %H:%M") -> str:
    """Format a datetime with a default, human-friendly pattern."""
    return value.strftime(fmt)


def _safe_highlight(text: str, term: str) -> Markup:
    """Wrap occurrences of ``term`` in ``<mark>`` while escaping user input.

    Demonstrates granular, opt-in escaping for security-sensitive rendering:
    both inputs are escaped before any markup is introduced.
    """
    safe_text = str(escape(text))
    safe_term = str(escape(term))
    if safe_term:
        safe_text = safe_text.replace(safe_term, f"<mark>{safe_term}</mark>")
    # Safe: both `text` and `term` are HTML-escaped above; only the trusted
    # <mark> wrapper is added, so no untrusted markup can be injected.
    return Markup(safe_text)  # noqa: S704


def create_templates(settings: Settings | None = None) -> Jinja2Templates:
    """Create a configured :class:`Jinja2Templates` instance."""
    settings = settings or get_settings()
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html", "xml", "j2"]),
        auto_reload=not settings.is_production,
        cache_size=400 if settings.is_production else 0,
    )
    env.filters["currency"] = _currency
    env.filters["datetimeformat"] = _datetimeformat
    env.filters["highlight"] = _safe_highlight
    env.globals["now"] = lambda: datetime.now(UTC)
    env.globals["app_name"] = settings.name
    return Jinja2Templates(env=env)


templates = create_templates()

__all__ = ["TEMPLATES_DIR", "create_templates", "templates"]
