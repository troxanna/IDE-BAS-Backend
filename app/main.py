from fastapi import FastAPI
from app.api.v1 import router as v1_router
from app.middleware.upload_size_limit import UploadSizeLimitMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.core.config import SESSION_SECRET_KEY
import logging
from .core.logging import setup_logging

setup_logging()  # вызываем ровно один раз при запуске

app = FastAPI(
    title="Markdown Upload API",
    version="1.0.0"
)

logger = logging.getLogger(__name__)
logger.info("App started")

app.add_middleware(UploadSizeLimitMiddleware, max_bytes=100 * 1024 * 1024)
app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET_KEY, 
)
app.include_router(v1_router.api_router, prefix="/api/v1")