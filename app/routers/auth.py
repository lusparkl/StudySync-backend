from app.database import get_session
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from app.services.user import UserService
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.helpers import google_oauth, GITHUB_CLIENT_ID
from app.auth.github import get_github_user_info
from app.schemas import UserCreate




router = APIRouter(prefix="/login", tags=["auth"])

@router.post("/")
def login(data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    service = UserService(session)
    return service.login_user(data)

@router.get("/google")
async def login_google(request: Request):
    return await google_oauth.google.authorize_redirect(request, "http://127.0.0.1:8000/login/callback/google")

@router.get("/callback/google")
async def auth_google(request: Request, session: Session = Depends(get_session)):
    try:
        token = await google_oauth.google.authorize_access_token(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Google authentication failed")

    user_info = token.get("userinfo")
    if not user_info:
        raise HTTPException(status_code=400, detail="Failed to get user info from Google")

    service = UserService(session)

    existing_user = service.get_user_by_email(user_info["email"])
    
    if existing_user:
        token = service.get_token_for_service_login_user(existing_user)
    else:
        token = service.create_user_for_service_login_user(UserCreate(username=user_info["given_name"], email=user_info["email"]))

    return RedirectResponse(f"http://127.0.0.1:8000?access_token={token}")

@router.get("/github")
async def login_github(request: Request):
    return RedirectResponse(f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&scope=read:user%20user:email&redirect_uri=http://127.0.0.1:8000/login/callback/github")

@router.get("/callback/github")
def auth_github(code: str, session: Session = Depends(get_session)):
    user_data = get_github_user_info(code)
    service = UserService(session)

    user_email = user_data.get("email") or user_data.get("login")
    existing_user = service.get_user_by_email(user_email)
    
    if existing_user:
        token = service.get_token_for_service_login_user(existing_user)
    else:
        token = service.create_user_for_service_login_user(UserCreate(username=user_data.get("login", "github_user"), email=user_email))
    
    return RedirectResponse(f"http://127.0.0.1:8000?access_token={token}")