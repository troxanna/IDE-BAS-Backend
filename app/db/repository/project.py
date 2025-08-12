from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.models.project import Project
from app.models.project_access import ProjectAccess


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


async def grant_project_access(
    db: AsyncSession, *, project_id: str, user_id: str
) -> ProjectAccess:
    result = await db.execute(
        select(ProjectAccess).where(
            ProjectAccess.project_id == project_id, ProjectAccess.user_id == user_id
        )
    )
    access = result.scalars().first()
    if not access:
        access = ProjectAccess(project_id=project_id, user_id=user_id)
        db.add(access)
        await db.flush()
    return access


async def get_user_project_by_name(
    db: AsyncSession, user_id: str, name: str
) -> Optional[Project]:
    stmt = (
        select(Project)
        .outerjoin(ProjectAccess, ProjectAccess.project_id == Project.id)
        .where(
            Project.name == name,
            or_(Project.user_id == user_id, ProjectAccess.user_id == user_id),
        )
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
