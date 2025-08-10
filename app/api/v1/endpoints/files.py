from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Form, Query
from app.services.s3_service import upload_file_to_s3
from app.core.security import get_current_user
from app.core.config import MINIO_ENDPOINT, FRIENDLY_URL
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.repository.project import get_or_create_project, get_user_project_by_name
from app.db.repository.file import create_file, get_user_files_by_project_name
from typing import List, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("")
async def upload_md_file(
    file: UploadFile = File(...),
    project_name: str = Form(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    allowed_extensions = {".md", ".puml", ".png", ".svg"}
    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Allowed: Markdown (.md), PlantUML (.puml), PNG (.png), SVG (.svg)."
        )

    project = await get_or_create_project(db, project_name, current_user.id)
    project_name_value = project.name
    bucket_name = "files-uploads"
    try:
        await upload_file_to_s3(file.file, "files-uploads", file.filename, content_type=file.content_type)
        public_url = f"{FRIENDLY_URL}/{bucket_name}/{file.filename}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading to S3: {e}")

    
    new_file = await create_file(
        db,
        filename=file.filename,
        s3_key=file.filename,
        bucket=bucket_name,
        content_type=file.content_type,
        project_id=project.id,
        public_url=public_url,
    )

    return {
        "filename": new_file.filename,
        "project": project_name_value,
        "public_url": new_file.public_url,
        "message": "File and project saved successfully",
    }


@router.get("", response_model=List[str])
async def list_user_files(
    project_name: str = Query(...), 
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    project = await get_user_project_by_name(db, user_id=current_user.id, name=project_name)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project '{project_name}' not found")

    files = await get_user_files_by_project_name(db, user_id=current_user.id, project_name=project_name)
    public_urls = [f.public_url for f in files if f.public_url]
    logger.debug(f"Public URLs: {public_urls}")

    return public_urls
