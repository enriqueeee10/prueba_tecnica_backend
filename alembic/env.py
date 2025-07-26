import asyncio
import os
import sys
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Añadir el path al módulo principal para poder importar bien
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Importar settings y Base
from app.config.settings import settings
from app.shared.infrastructure.base import Base  # ✅ Usa el Base correcto

# Importa los modelos para que Alembic los detecte
from app.contexts.users.infrastructure.models.user_model import UserModel
from app.contexts.auth.infrastructure.models.session_model import SessionModel

# Configuración de Alembic
config = context.config
fileConfig(config.config_file_name)

# Sobrescribe la URL desde settings
DATABASE_URL = settings.DATABASE_URL
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Metadata de los modelos
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode (async)."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:

        def do_run_migrations(sync_connection):
            context.configure(
                connection=sync_connection,
                target_metadata=target_metadata,
                compare_type=True,
            )
            with context.begin_transaction():
                context.run_migrations()

        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
