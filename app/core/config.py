# config.py
import os
from dotenv import load_dotenv

# Загружаем .env только если переменных ещё нет
if not os.getenv("MINIO_ENDPOINT"):
    load_dotenv()

# Получаем переменные
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_KEY_ID = os.getenv("MINIO_KEY_ID")
MINIO_APPLICATION_KEY = os.getenv("MINIO_APPLICATION_KEY")
DB_URI = os.getenv("DB_URI")