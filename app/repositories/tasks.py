from app.models import Task
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.schemas import TaskEdit, TaskCreate


class TasksRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: TaskCreate, owner_id: int, workspace_id: int):
        task = Task(
            title = data.title,
            text=data.text,
            owner_id=owner_id,
            workspace_id=workspace_id
        )

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        return task
    
    def edit(self, data: TaskEdit, task_id: int) -> Task | None:
        task = self.session.get(Task, task_id)

        if task is None:
            return None
        
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(task, field, value)
        
        self.session.commit()
        self.session.refresh(task)

        return task
    
    def get_by_workspace_id(self, workspace_id: int) -> list[Task]:
        stm = select(Task).where(Task.workspace_id == workspace_id)
        return self.session.scalars(stm).all()
    
    def get_by_id(self, task_id: int) -> Task | None:
        return self.session.get(Task, task_id)
    
    def delete(self, task_id: int) -> bool:
        task = self.session.get(Task, task_id)

        if task is None:
            return False
        
        self.session.delete(task)
        self.session.commit()

        return True