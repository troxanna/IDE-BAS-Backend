# session.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DB_URI  # переменная берётся из config.py

engine = create_async_engine(DB_URI, echo=True)

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