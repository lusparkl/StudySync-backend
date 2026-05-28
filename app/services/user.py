from fastapi import HTTPException
from app.repositories.users import UsersRepository
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas import UserCreate, UserEdit
from sqlalchemy.exc import IntegrityError
from app.auth.helpers import verify_password, create_access_token

class UserService:
    def __init__(self, session):
        self.repository = UsersRepository(session)
        self.session = session

    def _get_user_or_404(self, user_id: int):
        user = self.repository.get_by_id(user_id)

        if user is None:
            raise HTTPException(status_code=404, detail="User not found.")
        
        return user
    
    def _is_user_allowed(self, user, user_id: int):
        if user.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not allowed.")
        
    def get_user_for_user(self, user_id: int):
        return self._get_user_or_404(user_id)
    
    def edit_user_for_user(self, user_id: int, data: UserEdit):
        user = self._get_user_or_404(user_id)
        self._is_user_allowed(user, user_id)

        try:
            return self.repository.edit(data, user_id)
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(status_code=409, detail="Email or username is already taken.") 

    def create_user_for_user(self, data: UserCreate):
        try:
            user = self.repository.create(data)
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(status_code=409, detail="Email or username is already taken.")
        
        token = create_access_token(user.user_id)
        return {"access_token": token, "token_type": "bearer"}

    
    def login_user(self, data: OAuth2PasswordRequestForm):
        user = self.repository.get_by_email_or_username(data.username)
        if user is None:
            raise HTTPException(status_code=400, detail="Username or password is wrong.")
        
        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Username or password is wrong.")

        token = create_access_token(user.user_id)
        return {"access_token": token, "token_type": "bearer"}

    def set_profile_photo_for_user(self, photo_url: str, user_id: int):
        user = self._get_user_or_404(user_id)
        return self.repository.set_user_photo_url(user_id, photo_url)
