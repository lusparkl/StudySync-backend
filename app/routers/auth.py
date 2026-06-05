from app.database import get_session
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, Request
from fastapi.responses import RedirectResponse
from app.services.user import UserService
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.helpers import google_oauth, GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET
from app.schemas import UserCreate
import requests




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
    token = await google_oauth.google.authorize_access_token(request)

    user_info = token["userinfo"]
    service = UserService(session)

    existing_user = service.get_user_by_email(user_info["email"])
    
    if existing_user:
        token = service.get_token_for_service_login_user(existing_user)
    else:
        token = service.create_user_for_service_login_user(UserCreate(username=user_info["given_name"], email=user_info["email"]))

    return RedirectResponse(f"http://127.0.0.1:8000?access_token={token}")

@router.get("/github")
async def login_github(request: Request):
    return RedirectResponse(f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&scope=read:user%20user:email&redirect_url=http://127.0.0.1:8000/login/callback/github")

@router.get("/callback/github")
async def auth_github(code: str, session: Session = Depends(get_session)):
    url = "https://github.com/login/oauth/access_token"
    
    params = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code,
        "redirect_url": "http://127.0.0.1:8000/login/callback/github"
    }
    response = requests.get(url, params, headers={"Accept": "application/json"})

    token = response.json()["access_token"]

    url = "https://api.github.com/user"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    
    user_data = response.json()
    service = UserService(session)

    user_email = user_data["email"] if user_data["email"] else user_data["login"]
    existing_user = service.get_user_by_email(user_email)
    
    if existing_user:
        token = service.get_token_for_service_login_user(existing_user)
    else:
        token = service.create_user_for_service_login_user(UserCreate(user_data["login"], user_email))
    
    return RedirectResponse(f"http://127.0.0.1:8000?access_token={token}")