from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr

from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.db.repository.project import get_user_project_by_name, grant_project_access
from app.db.repository.user import get_user_by_email


router = APIRouter()


@router.post("/{project_name}/share")
async def share_project(
    project_name: str,
    user_email: EmailStr,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = await get_user_project_by_name(
        db, user_id=current_user.id, name=project_name
    )
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found")

    target_user = await get_user_by_email(db, user_email)
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    await grant_project_access(
        db, project_id=str(project.id), user_id=str(target_user.id)
    )
    await db.commit()

    return {"message": "access granted"}

