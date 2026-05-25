from app.database import get_session
from sqlalchemy.orm import Session
from app.repositories.users import UsersRepository
from fastapi import Depends, APIRouter, HTTPException
from app.schemas import UserEdit, UserCreate, UserReadPublic, UserReadPrivate
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.helpers import verify_password, create_access_token

router = APIRouter(prefix="/users",tags=["users"])

@router.get("/me", response_model=UserReadPrivate)
def get_me(session: Session = Depends(get_session)):
    rep = UsersRepository(session)
    user_id = 1 # "We'll get it from jwt later"
    result = rep.get_by_id(user_id)

    if result is None:
        raise HTTPException(status_code=404, detail="User not found.")
    
    return result

@router.get("/{user_id}", response_model=UserReadPublic)
def get_user(user_id: int, session: Session = Depends(get_session)):
    rep = UsersRepository(session)
    result = rep.get_by_id(user_id)

    if result is None:
        raise HTTPException(status_code=404, detail="User not found.")
    
    return result

@router.post("/", response_model=UserReadPrivate)
def create_user(data: UserCreate, session: Session = Depends(get_session)):
    rep = UsersRepository(session)
    #We need to hash passwordd here
    result = rep.create(data)
    return result

@router.patch("/", response_model=UserReadPrivate)
def edit_user(data: UserEdit, session: Session = Depends(get_session)):
    rep = UsersRepository(session)
    user_id = 1
    result = rep.update(data, user_id)
    return result

@router.post("/login")
def login(data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    rep = UsersRepository(session)
    user = rep.get_by_email_or_username(data.username)

    if not user:
        raise HTTPException(status_code=400, detail="Incorect username or password")
    
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorect username or password")
    
    token = create_access_token(user.user_id)

    return {"access_token": token, "token_type": "bearer"}