from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/health")
async def health():
    return JSONResponse(status_code=200, content={"status": "ok"})