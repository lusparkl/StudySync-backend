from app.database import get_session
from sqlalchemy.orm import Session
from app.services.user import UserService
from fastapi import Depends, APIRouter, UploadFile
from app.schemas import UserEdit, UserCreate, UserReadPublic, UserReadPrivate
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.authentication import get_current_user_id
from app.storage.profile_photos import upload_profile_photo

router = APIRouter(prefix="/users",tags=["users"])

@router.get("/me", response_model=UserReadPrivate)
def get_me(session: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    service = UserService(session)
    return service.get_user_for_user(user_id)

@router.get("/{user_id}", response_model=UserReadPublic)
def get_user(user_id: int, session: Session = Depends(get_session)):
    service = UserService(session)
    return service.get_user_for_user(user_id)

@router.post("/")
def create_user(data: UserCreate, session: Session = Depends(get_session)):
    service = UserService(session)
    return service.create_user_for_user(data)

@router.patch("/", response_model=UserReadPrivate)
def edit_user(data: UserEdit, session: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    service = UserService(session)
    return service.edit_user_for_user(user_id, data)

@router.post("/login")
def login(data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    service = UserService(session)
    return service.login_user(data)

@router.post("/profile_picture", response_model=UserReadPrivate)
def set_profile_picture(data: UploadFile, session: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    service = UserService(session)
    photo_link = upload_profile_photo(data)
    return service.set_profile_photo_for_user(photo_link, user_id)