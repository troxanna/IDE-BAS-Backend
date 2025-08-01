import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from fastapi import HTTPException
import asyncio
from app.core.config import MINIO_ENDPOINT, MINIO_KEY_ID, MINIO_APPLICATION_KEY


# Настройки для подключения к MinIO (или AWS S3)
s3_client = boto3.client(
    's3',
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_KEY_ID,
    aws_secret_access_key=MINIO_APPLICATION_KEY,
    region_name='us-east-1' 
)

async def upload_file_to_s3(file_obj, bucket_name, object_name):
    try:
        # оборачиваем синхронную функцию в async-совместимую
        await asyncio.to_thread(s3_client.upload_fileobj, file_obj, bucket_name, object_name)
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="MinIO credentials not found")
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload to S3: {e.response['Error']['Message']}")