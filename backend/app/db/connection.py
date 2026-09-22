"""
PrepForge — MongoDB Connection

Manages the lifecycle of the Motor async MongoDB client.

Responsibilities:
  - Create the client on application startup.
  - Verify connectivity with a lightweight ping.
  - Expose the database instance to the rest of the app.
  - Close the client cleanly on application shutdown.

Usage:
  from app.db.connection import db_client

  # Inside an endpoint or dependency:
  db = db_client.database
  users = db["users"]
"""

import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings

logger = logging.getLogger(__name__)


class _DatabaseClient:
    """
    Thin wrapper that holds the Motor client and exposes the
    target database as an attribute.

    Instantiated once at module import time; the client itself
    is created lazily during application startup so that
    configuration is fully loaded before any network call.
    """

    def __init__(self) -> None:
        self._client: AsyncIOMotorClient | None = None
        self._database: AsyncIOMotorDatabase | None = None

    # ----------------------------------------------------------
    # Lifecycle — called from the FastAPI lifespan handler
    # ----------------------------------------------------------

    async def connect(self) -> None:
        """
        Create the Motor client and verify MongoDB is reachable.

        serverSelectionTimeoutMS=5000 limits the ping to 5 seconds.
        If MongoDB is not reachable within that window, a
        ServerSelectionTimeoutError is raised rather than hanging.
        """
        logger.info("Connecting to MongoDB at %s …", settings.MONGODB_URL)

        self._client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            serverSelectionTimeoutMS=5000,
        )
        self._database = self._client[settings.DATABASE_NAME]

        # Ping the admin database to verify the connection is live
        # before the application starts accepting requests.
        await self._client.admin.command("ping")
        
        # Setup indexes
        await self._database["users"].create_index("email", unique=True)
        await self._database["weeks"].create_index([("user_id", 1), ("week_number", 1)], unique=True)
        await self._database["tasks"].create_index([("user_id", 1), ("week_id", 1)])
        await self._database["tasks"].create_index([("user_id", 1), ("completed", 1)])
        await self._database["task_progress"].create_index([("user_id", 1), ("task_id", 1)], unique=True)
        await self._database["weaknesses"].create_index([("user_id", 1), ("status", 1)])
        await self._database["weaknesses"].create_index([("user_id", 1), ("priority", 1)])
        await self._database["weaknesses"].create_index([("user_id", 1), ("retry_date", 1)])
        await self._database["weekly_reviews"].create_index([("user_id", 1), ("week_number", 1)], unique=True)
        
        logger.info(
            "MongoDB connected — database: '%s'", settings.DATABASE_NAME
        )

    async def close(self) -> None:
        """Close the Motor client on application shutdown."""
        if self._client is not None:
            self._client.close()
            self._client = None
            self._database = None
            logger.info("MongoDB connection closed.")

    # ----------------------------------------------------------
    # Accessor
    # ----------------------------------------------------------

    @property
    def database(self) -> AsyncIOMotorDatabase:
        """
        Return the active database instance.

        Raises RuntimeError if accessed before connect() has been
        called — prevents silent failures from unconfigured state.
        """
        if self._database is None:
            raise RuntimeError(
                "Database is not connected. "
                "Ensure connect() was called during application startup."
            )
        return self._database

    @property
    def is_connected(self) -> bool:
        """True if the client has been initialised and connected."""
        return self._client is not None


# Single module-level instance shared across the application.
db_client = _DatabaseClient()
