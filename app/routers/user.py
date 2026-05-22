from app.schemas import UserReadPublic, UserReadPrivate, UserEdit, UserCreate
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.utils import get_session
from app.repositories.users import UsersRepository

router = APIRouter(tags="users")

@router.get("/me", response_model=UserReadPrivate)
def get_me(session: Session = Depends(get_session)):
    rep = UsersRepository(session)
    user_id = 1 # "We'll get it from jwt later"
    result = rep.get_by_id(user_id)

    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return result

@router.get("/{user_id}", response_model=UserReadPublic)
def get_user(user_id: int, session: Session = Depends(get_session)):
    rep = UsersRepository(session)
    result = rep.get_by_id(user_id)

    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return result

@router.post("", response_model=UserReadPrivate)
def create_user(data: UserCreate, session: Session = Depends(get_session)):
    rep = UsersRepository(session)
    #We need to hash passwordd here
    result = rep.create(data)
    return result

@router.patch("", response_model=UserReadPrivate)
def edit_user(data: UserEdit, session: Session = Depends(get_session)):
    rep = UsersRepository(session)
    user_id = 1
    result = rep.update(data, user_id)
    return result