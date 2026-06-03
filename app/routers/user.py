from app.database import get_session
from sqlalchemy.orm import Session
from app.services.user import UserService
from fastapi import Depends, APIRouter, UploadFile, File
from app.schemas import UserEdit, UserEditPassword, UserCreate, UserReadPublic, UserReadPrivate
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

@router.patch("/me/password", response_model=UserReadPrivate)
def edit_user_password(data: UserEditPassword, session: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    service = UserService(session)
    return service.change_user_password(user_id, data.old_password, data.new_password)

@router.patch("/me/profile_picture", response_model=UserReadPrivate)
def set_profile_picture(file: UploadFile = File(...), session: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    service = UserService(session)
    photo_link = upload_profile_photo(file, user_id, service.get_user_for_user(user_id).profile_photo_link)
    return service.set_profile_photo_for_user(photo_link, user_id)

@router.delete("/me/profile_picture", response_model=UserReadPrivate)
def delete_profile_picture(session: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    service = UserService(session)
    return service.set_profile_photo_for_user("https://images.lusparkl.foo/default_avatar.webp", user_id)