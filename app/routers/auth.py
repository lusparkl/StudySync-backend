from app.database import get_session
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from app.services.user import UserService
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.helpers import BACKEND_URL, FRONTEND_URL, google_oauth, GITHUB_CLIENT_ID
from app.auth.github import get_github_user_info
from urllib.parse import urlencode




router = APIRouter(prefix="/login", tags=["auth"])

def frontend_oauth_redirect(token: str | None = None, error: str | None = None, provider: str | None = None):
    params = {}

    if token:
        params["access_token"] = token
    if error:
        params["error"] = error
    if provider:
        params["provider"] = provider

    return RedirectResponse(f"{FRONTEND_URL}/oauth/callback?{urlencode(params)}")

@router.post("/")
def login(data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    service = UserService(session)
    return service.login_user(data)

@router.get("/google")
async def login_google(request: Request):
    return await google_oauth.google.authorize_redirect(request, f"{BACKEND_URL}/login/callback/google")

@router.get("/callback/google")
async def auth_google(request: Request, session: Session = Depends(get_session)):
    try:
        oauth_token = await google_oauth.google.authorize_access_token(request)
    except Exception:
        return frontend_oauth_redirect(error="Google authentication failed", provider="google")

    user_info = oauth_token.get("userinfo")
    if not user_info:
        return frontend_oauth_redirect(error="Failed to get user info from Google", provider="google")

    service = UserService(session)
    email = user_info["email"]
    username = user_info.get("given_name") or user_info.get("name") or email.split("@")[0]
    token = service.login_or_create_oauth_user(
        email=email,
        username=username,
        provider="google",
        provider_id=user_info.get("sub"),
    )

    return frontend_oauth_redirect(token=token, provider="google")

@router.get("/github")
async def login_github(request: Request):
    params = urlencode({
        "client_id": GITHUB_CLIENT_ID,
        "scope": "read:user user:email",
        "redirect_uri": f"{BACKEND_URL}/login/callback/github",
    })
    return RedirectResponse(f"https://github.com/login/oauth/authorize?{params}")

@router.get("/callback/github")
def auth_github(code: str, session: Session = Depends(get_session)):
    user_data = get_github_user_info(code)
    service = UserService(session)

    user_email = user_data.get("email") or f"github_{user_data['id']}@users.noreply.github.com"
    token = service.login_or_create_oauth_user(
        email=user_email,
        username=user_data.get("login", "github_user"),
        provider="github",
        provider_id=user_data.get("id"),
    )
    
    return frontend_oauth_redirect(token=token, provider="github")
