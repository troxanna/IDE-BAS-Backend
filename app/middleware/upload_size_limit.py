from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.datastructures import UploadFile
from starlette.types import ASGIApp
import asyncio

class UploadSizeLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, max_bytes: int):
        super().__init__(app)
        self.max_bytes = max_bytes

    async def dispatch(self, request: Request, call_next):
        if request.method == "POST" and request.headers.get("content-type", "").startswith("multipart/form-data"):
            # Временное считывание тела запроса
            body = await request.body()
            if len(body) > self.max_bytes:
                raise HTTPException(status_code=413, detail=f"File too large. Max allowed size is {self.max_bytes / (1024 * 1024):.1f} MB")
            # Восстанавливаем тело, чтобы его мог прочитать endpoint
            async def receive():
                return {"type": "http.request", "body": body}
            request._receive = receive
        return await call_next(request)