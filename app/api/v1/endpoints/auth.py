from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.core.oauth import oauth
from app.db.session import get_db
from app.db.repository.user import get_or_create_user
from app.core.security import create_jwt_token
from app.core.config import GOOGLE_REDIRECT_URI

router = APIRouter()

@router.get("/login")
async def login(request: Request):
    redirect_uri = GOOGLE_REDIRECT_URI
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth/callback")
async def auth_callback(request: Request, db=Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    if not token:
        raise HTTPException(status_code=400, detail="Failed to retrieve access token")

    user_info = token.get("userinfo")
    if not user_info:
        raise HTTPException(status_code=400, detail="User info not found in token")

    user = await get_or_create_user(db, user_info)
    jwt_token = create_jwt_token(user.id)

    # Когда будет фронт:
    # redirect_url = f"FRONTEND_REDIRECT_URI/auth/callback?token={jwt_token}"
    # return RedirectResponse(url=redirect_url)

    return JSONResponse(content={"access_token": jwt_token})
