# security.py
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.models.user import User  # подкорректируй путь, если нужно
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import JWT_SECRET, TEST_AUTH_TOKEN, TEST_USER_ID
from app.db.repository.user import get_user_by_id

JWT_ALGORITHM = "HS256"

def create_jwt_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(days=7)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # не используется напрямую

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Разрешаем использование статичного токена для тестирования
    if TEST_AUTH_TOKEN and token == TEST_AUTH_TOKEN:
        if not TEST_USER_ID:
            raise credentials_exception
        user = await get_user_by_id(db, TEST_USER_ID)
        if user is None:
            raise credentials_exception
        return user

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user_by_id(db, user_id)
    if user is None:
        raise credentials_exception
    return user
