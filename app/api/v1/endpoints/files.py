from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Form, Query
from app.services.s3_service import upload_file_to_s3
from app.core.security import get_current_user
from app.models.user import User
from app.models.project import Project
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.repository.project import get_or_create_project, get_user_project_by_name
from app.db.repository.file import create_file
from typing import List, Optional
from app.db.repository.file import get_user_files_by_project_name

router = APIRouter()

@router.post("/")
async def upload_md_file(file: UploadFile = File(...),
                          project_name: str = Form(...), 
                          db: AsyncSession = Depends(get_db),
                          current_user: User = Depends(get_current_user)):
    if file.content_type != "text/markdown" and not file.filename.endswith(".md"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a Markdown (.md) file.")

    project = await get_or_create_project(db, project_name, current_user.id)
    # Задаем имя бакета
    bucket_name = "files-uploads"
    # Передача файла в S3
    try:
        await upload_file_to_s3(file.file, bucket_name, file.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading to S3: {e}")

    new_file = await create_file(
        db,
        filename=file.filename,
        s3_key=file.filename,
        bucket=bucket_name,
        content_type=file.content_type,
        project_id=project.id,
    )   

    return {
        "filename": new_file.filename,
        "project": project.name,
        "message": "File and project saved successfully"
    }



@router.get("/", response_model=List[str])
async def list_user_files(
    project_name: Optional[str] = Query(default=None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if project_name:
        project = await get_user_project_by_name(db, user_id=current_user.id, name=project_name)
        if not project:
            raise HTTPException(status_code=404, detail=f"Project '{project_name}' not found")

    files = await get_user_files_by_project_name(db, user_id=current_user.id, project_name=project_name)
    public_urls = [f.public_url for f in files if f.public_url]
    return public_urls