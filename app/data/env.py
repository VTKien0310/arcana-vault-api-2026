import logging
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import URL
from alembic import context

from app.core import settings
from .models import model_common_metadata

config = context.config

if not config.get_main_option("sqlalchemy.url"):
    db_url = URL.create(
        drivername="postgresql",
        username=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
    )
    config.set_main_option("sqlalchemy.url", str(db_url))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)
else:
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

target_metadata = model_common_metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
