# file.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.file import File
from app.models.project import Project
from typing import Optional, List
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


async def create_file(
    db: AsyncSession,
    *,
    filename: str,
    s3_key: str,
    bucket: str,
    content_type: str,
    project_id: str,
    public_url: Optional[str] = None
) -> File:
    new_file = File(
        filename=filename,
        s3_key=s3_key,
        bucket=bucket,
        content_type=content_type,
        project_id=project_id,
        public_url=public_url,
    )
    db.add(new_file)
    await db.commit()
    await db.refresh(new_file)
    return new_file


async def get_user_files_by_project_name(
    db: AsyncSession,
    user_id: str,                 # проверь, не int ли у тебя на самом деле
    project_name: Optional[str],  # теперь опционально
) -> List[File]:
    stmt = (
        select(File)
        .join(File.project)                       # join по ORM-отношению
        .where(Project.user_id == user_id)        # только проекты текущего пользователя
        # .where(File.is_public.is_(True))        # раскомментируй, если нужны только публичные
        .options(selectinload(File.project))      # подгружаем проект, чтобы не было N+1
        .order_by(File.created_at.desc())
    )

    if project_name:                               # фильтр по имени проекта — только если задан
        stmt = stmt.where(Project.name == project_name)

    result = await db.execute(stmt)
    return result.scalars().all()