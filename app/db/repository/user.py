from sqlalchemy.future import select
from typing import Optional
from app.models.user import User

async def get_or_create_user(db, user_info: dict) -> User:
    google_id = user_info.get("sub")  # Обычно 'sub' — это Google ID

    stmt = select(User).where(User.google_id == google_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user:
        return user

    user = User(
        google_id=google_id,
        email=user_info.get("email"),
        name=user_info.get("name"),
        avatar_url=user_info.get("picture")  # если есть
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_user_by_id(db, user_id: int) -> Optional[User]:
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()