from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.s3_service import upload_file_to_s3
import os

router = APIRouter()

@router.post("/upload-md/")
async def upload_md_file(file: UploadFile = File(...)):
    if file.content_type != "text/markdown" and not file.filename.endswith(".md"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a Markdown (.md) file.")
    # Задаем имя бакета
    bucket_name = "markdown-files-uploads"
    # Передача файла в S3
    try:
        await upload_file_to_s3(file.file, bucket_name, file.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading to S3: {e}")
    return {"filename": file.filename, "message": "File uploaded successfully"}
