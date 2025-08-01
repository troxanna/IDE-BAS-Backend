import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from fastapi import HTTPException
import asyncio


# Настройки для подключения к MinIO (или AWS S3)
s3_client = boto3.client(
    's3',
    endpoint_url='http://minio:9000',  # ⚠️ URL MinIO-сервера
    aws_access_key_id='minio',
    aws_secret_access_key='minio123',
    region_name='us-east-1'            # можно любой
)

async def upload_file_to_s3(file_obj, bucket_name, object_name):
    try:
        # оборачиваем синхронную функцию в async-совместимую
        await asyncio.to_thread(s3_client.upload_fileobj, file_obj, bucket_name, object_name)
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="MinIO credentials not found")
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload to S3: {e.response['Error']['Message']}")