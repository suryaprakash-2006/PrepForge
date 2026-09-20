"""
PrepForge — FastAPI Application Entry Point

Run locally from the backend/ directory with:
    uvicorn app.main:app --reload

The application uses the modern lifespan context manager (introduced in
FastAPI 0.93 / Starlette 0.27) instead of the deprecated @app.on_event
decorators. This is the recommended pattern for FastAPI in 2024+.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.connection import db_client

# ------------------------------------------------------------------
# Logging
# A simple stdout logger is sufficient for development.
# In production this would be replaced by structured logging.
# ------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# ------------------------------------------------------------------
# Lifespan — startup and shutdown
# ------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Manage application lifecycle events.

    Code before `yield` runs on startup.
    Code after `yield` runs on shutdown.

    This replaces the deprecated @app.on_event("startup") pattern.
    """
    # ---- STARTUP ----
    logger.info("PrepForge backend starting up …")
    logger.info("Environment : %s", settings.ENVIRONMENT)
    logger.info("API prefix  : %s", settings.API_PREFIX)

    try:
        await db_client.connect()
    except Exception as exc:  # noqa: BLE001
        # Log the error clearly but do NOT expose the connection
        # string (which may contain credentials) in the message.
        logger.error(
            "MongoDB connection FAILED during startup: %s — "
            "the application will start but the database is unavailable.",
            type(exc).__name__,
        )
        # We intentionally allow the application to start even if
        # MongoDB is down so that the /health endpoint can report the
        # degraded state rather than returning nothing at all.

    logger.info("PrepForge backend ready.")
    yield

    # ---- SHUTDOWN ----
    logger.info("PrepForge backend shutting down …")
    await db_client.close()
    logger.info("PrepForge backend stopped.")


# ------------------------------------------------------------------
# Application instance
# ------------------------------------------------------------------

app = FastAPI(
    title="PrepForge API",
    description=(
        "Backend API for PrepForge — 12-Week Internship Preparation Tracker. "
        "Phase 2: Infrastructure scaffold."
    ),
    version="0.2.0",
    # Only expose /docs and /redoc in non-production environments.
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
    lifespan=lifespan,
)


# ------------------------------------------------------------------
# CORS
#
# The frontend does not exist yet, but CORS middleware is added now
# so that when the frontend scaffold arrives (Phase 3) it works
# immediately without touching this file.
#
# Origins are loaded from the CORS_ORIGINS environment variable.
# Default is http://localhost:5173 (Vite dev server default).
#
# allow_credentials=True is intentionally left False here because
# we are not yet using cookies. It will be set when the auth
# strategy (cookie vs. header token) is finalised in Phase 4.
#
# Wildcard "*" is deliberately NOT used:
#   - It cannot be combined with allow_credentials=True.
#   - It allows any origin in production, which is insecure.
# ------------------------------------------------------------------

_cors_origins: list[str] = [
    origin.strip()
    for origin in settings.CORS_ORIGINS.split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


from app.api import api_router

# ------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------

app.include_router(api_router, prefix=settings.API_PREFIX)

@app.get(
    f"{settings.API_PREFIX}/health",
    summary="Health check",
    tags=["Infrastructure"],
)
async def health_check() -> dict:
    """
    Return the operational status of the application and its dependencies.

    Response fields:
      - status: always "ok" if the application itself is running.
      - environment: the deployment environment.
      - database: "connected" | "unavailable"

    HTTP status:
      - 200 if the application is alive (even if the DB is down).
        This lets a load balancer or orchestrator know the process
        is healthy. Database-level health is described in the body.

    Note: A more sophisticated health endpoint (returning 503 when
    the DB is down) can be added when the deployment strategy
    requires it. For local development, 200 is sufficient.
    """
    db_status = "connected" if db_client.is_connected else "unavailable"

    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT,
        "database": db_status,
    }
