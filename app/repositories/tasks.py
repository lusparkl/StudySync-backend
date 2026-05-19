from app.models import Task
from sqlalchemy import select
from sqlalchemy.orm import Session

class TasksRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self):
        pass
    
    def get_by_workspace_id(self, workspace_id: int) -> list:
        stm = select(Task).where(Task.workspace_id == workspace_id)
        return self.session.scalars(stm).all()
    
    def get_by_id(self, id: int) -> Task | None:
        stm = select(Task).where(Task.id == id)
        return self.session.scalars(stm).first()
    
    