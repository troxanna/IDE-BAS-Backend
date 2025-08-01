from fastapi import FastAPI
from app.api.v1 import router as v1_router
from app.middleware import upload_size_limit as UploadSizeLimitMiddleware

app = FastAPI(
    title="Markdown Upload API",
    version="1.0.0"
)

app.add_middleware(UploadSizeLimitMiddleware, max_bytes=100 * 1024 * 1024)

app.include_router(v1_router.api_router, prefix="/api/v1")