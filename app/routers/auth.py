from app.database import get_session
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, Request
from fastapi.responses import RedirectResponse
from app.services.user import UserService
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.helpers import oauth
from app.schemas import UserCreate




router = APIRouter(prefix="/login", tags=["auth"])

@router.post("/")
def login(data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    service = UserService(session)
    return service.login_user(data)

@router.get("/google")
async def login_google(request: Request):
    return await oauth.google.authorize_redirect(request, "http://127.0.0.1:8000/login/callback/google")

@router.get("/callback/google")
async def auth(request: Request, session: Session = Depends(get_session)):
    token = await oauth.google.authorize_access_token(request)

    user_info = token["userinfo"]
    service = UserService(session)

    existing_user = service.get_user_by_email(user_info["email"])
    
    if existing_user:
        token = service.get_token_for_service_login_user(existing_user)
    else:
        token = service.create_user_for_service_login_user(UserCreate(username=user_info["given_name"], email=user_info["email"]))

    return RedirectResponse(f"http://127.0.0.1:8000?access_token={token}")