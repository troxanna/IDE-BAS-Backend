# file.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.file import File, Project
from typing import Optional
from sqlalchemy.future import select


async def create_file(
    db: AsyncSession,
    *,
    filename: str,
    s3_key: str,
    bucket: str,
    content_type: str,
    user_id: str,
    project_id: str
) -> File:
    new_file = File(
        filename=filename,
        s3_key=s3_key,
        bucket=bucket,
        content_type=content_type,
        user_id=user_id,
        project_id=project_id,
    )
    db.add(new_file)
    await db.commit()
    await db.refresh(new_file)
    return new_file


async def get_user_files_by_project_name(db: AsyncSession, user_id: str, project_name: Optional[str]):
    stmt = select(File).join(Project).where(File.user_id == user_id, File.is_public == True)

    if project_name:
        stmt = stmt.where(Project.name == project_name)

    result = await db.execute(stmt)
    return result.scalars().all()