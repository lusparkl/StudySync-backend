from app.schemas import TaskCreate, TaskEdit, TaskRead
from app.utils import get_session
from app.repositories.tasks import TasksRepository
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

router = APIRouter(tags=["tasks"])

@router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: int, session: Session = Depends(get_session)):
    rep = TasksRepository(session)
    result = rep.get_by_id(task_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    
    return result

@router.post("/workspaces/{workspace_id}/tasks", response_model=TaskRead)
def create_task(workspace_id: int, data: TaskCreate, session: Session = Depends(get_session)):
    rep = TasksRepository(session)
    user_id = 1
    return rep.create(data, user_id, workspace_id)

@router.patch("/tasks/{task_id}", response_model=TaskRead)
def edit_task(task_id: int, data: TaskEdit, session: Session = Depends(get_session)):
    rep = TasksRepository(session)
    result = rep.update(data, task_id)

    if result is None:
        return HTTPException(status_code=404, detail="Task not found.")
    
    return result

@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, session: Session = Depends(get_session)):
    rep = TasksRepository(session)
    deleted = rep.delete(task_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found.")
    
    return None