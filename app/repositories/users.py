from app.models import User
from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from app.schemas import UserEdit, UserCreate
from app.auth.helpers import hash_password

class UsersRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, data: UserCreate) -> User:
        user = User(
            username=data.username,
            email=data.email,
            hashed_password=hash_password(data.password), 
            profile_photo_link="change me too" # Set default photo
        )

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user
    
    def update(self, data: UserEdit, user_id: int) -> User | None:
        user = self.session.get(User, user_id)

        if user == None:
            return None
        
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(user, field, value)

        self.session.commit()
        self.session.refresh(user)

        return user
    
    def get_by_id(self, user_id: int) -> User | None:
        return self.session.get(User, user_id)


    def get_by_email_or_username(self, login: str) -> User | None:
        stm = select(User).where(or_(User.email == login, User.username == login))
        return self.session.scalar(stm)