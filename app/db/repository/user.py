from sqlalchemy.future import select
from app.models.user import User

async def get_or_create_user(db, user_info: dict) -> User:
    stmt = select(User).where(User.email == user_info["email"])
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user:
        return user

    user = User(email=user_info["email"], name=user_info.get("name"))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
