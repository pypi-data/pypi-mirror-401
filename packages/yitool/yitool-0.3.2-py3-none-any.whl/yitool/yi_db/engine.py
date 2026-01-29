from sqlalchemy.ext.asyncio import create_async_engine
from yitool.yi_config import config as settings

# Map database URL prefixes to async driver suffixes
ASYNC_DRIVER_MAP = {
    "mysql": "asyncmy",
    "postgresql": "asyncpg",
    "sqlite": "aiosqlite",
}


def get_async_db_url(db_url: str) -> str:
    """Get async database URL by adding appropriate async driver suffix."""
    # Extract base database type (mysql, postgresql, sqlite)
    base_type = None
    for db_type in ASYNC_DRIVER_MAP.keys():
        if db_type in db_url:
            base_type = db_type
            break

    if base_type:
        # Get appropriate async driver suffix
        async_suffix = ASYNC_DRIVER_MAP[base_type]
        
        # Check if URL already has a driver
        if "+" in db_url.split("://")[0]:
            # URL already has a driver, return as is
            return db_url
        else:
            # Rebuild URL with async driver
            protocol = f"{base_type}+{async_suffix}"
            connection_string = db_url.split("://", 1)[1]
            return f"{protocol}://{connection_string}"

    return db_url


def create_engine_for_config(db_config) -> str:
    """Create async engine for given database configuration."""
    # Check if we're in a test environment or alembic environment
    import sys
    is_test = "pytest" in sys.modules
    is_alembic = "alembic" in sys.modules

    if is_test or is_alembic:
        # In test or alembic environment, use in-memory SQLite database
        db_url = "sqlite+aiosqlite:///:memory:"
        # SQLite doesn't support pool-related arguments
        return create_async_engine(
            db_url,
            connect_args={"check_same_thread": False},
            echo=True if settings.settings.app.environment == "development" else False,
        )

    # In normal environment, use the configured database URL
    db_url = get_async_db_url(db_config.url)

    # Check if the database is SQLite
    if "sqlite+" in db_url:
        # SQLite doesn't support pool-related arguments
        return create_async_engine(
            db_url,
            connect_args={"check_same_thread": False},
            echo=True if settings.settings.app.environment == "development" else False,
        )

    # For other databases (MySQL, PostgreSQL), use the pool-related arguments
    return create_async_engine(
        db_url,
        pool_size=db_config.pool_size,
        max_overflow=db_config.max_overflow,
        pool_timeout=db_config.pool_timeout,
        pool_recycle=db_config.pool_recycle,
        echo=True if settings.settings.app.environment == "development" else False,
    )


# Create async engines for different datasources
engine_master = create_engine_for_config(settings.settings.datasource.master)

# Create slave engine if configured
engine_slave = create_engine_for_config(settings.settings.datasource.slave) if settings.settings.datasource.slave else None

# Create tasks engine if configured, otherwise use master
engine_tasks = create_engine_for_config(settings.settings.datasource.tasks) if settings.settings.datasource.tasks else engine_master

# Default engine is master
engine = engine_master

__all__ = ["engine", "engine_master", "engine_slave", "engine_tasks"]
