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
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
JWT_SECRET = os.getenv("JWT_SECRET")
SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY")
FRIENDLY_URL = os.getenv("FRIENDLY_URL")

# Тестовый токен и пользователь для упрощённой авторизации
TEST_AUTH_TOKEN = os.getenv("TEST_AUTH_TOKEN")
TEST_USER_ID = os.getenv("TEST_USER_ID")