from app.models import User
from app.schemas import UserCreate, UserEdit
from sqlalchemy.orm import Session

class UsersRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, data: UserCreate) -> User:
        user = User(
            username=data.username,
            email=data.email,
            hashed_password="change me", 
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
    
    def get_by_id(self, user_id) -> User | None:
        return self.session.get(User, user_id)
