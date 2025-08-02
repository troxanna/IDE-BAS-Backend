import asyncio
import os
import sys
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

# Подгружаем .env, если локально
if not os.getenv("DB_URI"):
    from dotenv import load_dotenv
    load_dotenv()

# Добавляем путь к приложению
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models import Base  # Импорт базы моделей
from app.core.config import DB_URI  # Либо os.getenv("DB_URI")

# Alembic config
config = context.config
fileConfig(config.config_file_name)

# Для автогенерации
target_metadata = Base.metadata


def run_migrations_offline():
    """Запуск офлайн-миграций (без подключения к БД)"""
    url = DB_URI
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Запуск онлайн-миграций через async движок"""
    connectable = create_async_engine(DB_URI, pool_pre_ping=True)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
