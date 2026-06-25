from fastapi import HTTPException
from app.repositories.users import UsersRepository
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas import UserCreate, UserEdit
from sqlalchemy.exc import IntegrityError
from app.auth.helpers import verify_password, create_access_token, hash_password
import re



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

    def create_user_for_service_login_user(self, data: UserCreate):
        try:
            user = self.repository.create(data)
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(status_code=409, detail="Email or username is already taken.")
        
        return create_access_token(user.user_id)

    def login_user(self, data: OAuth2PasswordRequestForm):
        user = self.repository.get_by_email_or_username(data.username)
        if user is None:
            raise HTTPException(status_code=400, detail="Username or password is wrong.")
        
        if user.hashed_password is None:
            raise HTTPException(status_code=400, detail="Username or password is wrong.")
        
        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Username or password is wrong.")

        token = create_access_token(user.user_id)
        return {"access_token": token, "token_type": "bearer"}
    
    def get_user_by_email(self, email):
        return self.repository.get_by_email_or_username(email)
    
    def get_token_for_service_login_user(self, user):
        return create_access_token(user.user_id)

    def login_or_create_oauth_user(self, email: str, username: str, provider: str, provider_id: str | int | None = None):
        existing_user = self.get_user_by_email(email)

        if existing_user:
            return self.get_token_for_service_login_user(existing_user)
        
        clean_username = self._make_oauth_username(username, provider, provider_id)
        return self.create_user_for_service_login_user(UserCreate(username=clean_username, email=email))
    
    def _make_oauth_username(self, username: str, provider: str, provider_id: str | int | None):
        fallback_id = str(provider_id) if provider_id is not None else "user"
        base_username = username or f"{provider}_{fallback_id}"
        base_username = re.sub(r"[^a-zA-Z0-9_-]+", "_", base_username).strip("_")
        base_username = base_username or f"{provider}_{fallback_id}"

        candidate = base_username
        if self.repository.get_by_email_or_username(candidate) is None:
            return candidate
        
        candidate = f"{base_username}_{provider}_{fallback_id}"
        if self.repository.get_by_email_or_username(candidate) is None:
            return candidate

        index = 2
        while self.repository.get_by_email_or_username(f"{candidate}_{index}") is not None:
            index += 1
        
        return f"{candidate}_{index}"
        

    def set_profile_photo_for_user(self, photo_url: str, user_id: int):
        self._get_user_or_404(user_id)
        return self.repository.set_user_photo_url(user_id, photo_url)

    def change_user_password(self, user_id: int, old_password: str, new_password: str):
        user = self._get_user_or_404(user_id)

        if user.hashed_password is None:
            raise HTTPException(status_code=400, detail="Password login is not enabled for this account.")
        
        if not verify_password(old_password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Wrong old password.")
        
        new_password_hash = hash_password(new_password)
        return self.repository.change_password_hash(user_id, new_password_hash)
    
