# session.py
import ssl
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DB_URI  # переменная берётся из config.py

# Создаём SSL-контекст
ssl_context = ssl.create_default_context()

# Подключаем движок с SSL
engine = create_async_engine(
    DB_URI,
    echo=True,
    connect_args={"ssl": ssl_context}  # 👈 важно
)

# Создаём асинхронную сессию
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
)

# Dependency для FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
