from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.project import Project
from typing import Optional

async def get_or_create_project(db: AsyncSession, name: str, user_id: str) -> Project:
    result = await db.execute(
        select(Project).where(Project.name == name, Project.user_id == user_id)
    )
    project = result.scalars().first()

    if not project:
        project = Project(name=name, user_id=user_id)
        db.add(project)
        await db.flush()  # нужно до коммита, чтобы получить project.id

    return project


async def get_user_project_by_name(db: AsyncSession, user_id: str, name: str) -> Optional[Project]:
    stmt = select(Project).where(Project.user_id == user_id, Project.name == name)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()