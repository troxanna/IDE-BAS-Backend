# router.py
from fastapi import APIRouter
from app.api.v1.endpoints import files
from app.api.v1.endpoints import core

api_router = APIRouter()
api_router.include_router(files.router, prefix="/files", tags=["files"])
api_router.include_router(core.router, tags=["health"])