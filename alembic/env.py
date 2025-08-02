import os
import sys
from logging.config import fileConfig

from sqlalchemy import create_engine
from alembic import context

# Подгружаем .env, если переменная не установлена
if not os.getenv("DB_URI_SYNC"):
    from dotenv import load_dotenv
    load_dotenv()

# Добавляем путь к приложению
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models import Base  # Импорт моделей
from app.core.config import DB_URI  # async URI, используется только для приложения

# Alembic config
config = context.config
fileConfig(config.config_file_name)

# Метаданные моделей для автогенерации миграций
target_metadata = Base.metadata

# Получаем sync URI из переменной окружения
SYNC_DB_URI = os.getenv("DB_URI_SYNC")


def run_migrations_offline():
    """Запуск офлайн-миграций (без подключения к БД)"""
    context.configure(
        url=SYNC_DB_URI,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Запуск онлайн-миграций через sync движок"""
    connectable = create_engine(SYNC_DB_URI, pool_pre_ping=True)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
