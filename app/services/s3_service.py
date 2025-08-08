import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from botocore.config import Config
from fastapi import HTTPException
import asyncio
from app.core.config import MINIO_ENDPOINT, MINIO_KEY_ID, MINIO_APPLICATION_KEY


# Настройки для подключения к MinIO (или AWS S3)
s3_client = boto3.client(
    's3',
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_KEY_ID.strip(),
    aws_secret_access_key=MINIO_APPLICATION_KEY.strip(),
    region_name='us-east-005',
    config=Config(signature_version="s3v4", s3={"addressing_style": "virtual"}),
)

async def upload_file_to_s3(file_obj, bucket_name: str, object_name: str, content_type: str | None = None):
    print(MINIO_ENDPOINT)
    print(MINIO_KEY_ID)
    print(MINIO_APPLICATION_KEY)

    print("KEY_ID:", MINIO_KEY_ID[:4], "...", MINIO_APPLICATION_KEY[-4:])
    file_obj.seek(0)  # важно!
    extra = {}
    if content_type:
     extra["ContentType"] = content_type
    def _do_upload():
        s3_client.upload_fileobj(file_obj, bucket_name, object_name, ExtraArgs=extra)
    # boto3 — блокирующий, выносим в поток
    return await asyncio.to_thread(_do_upload)