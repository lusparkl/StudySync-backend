from app.schemas import TaskCreate, TaskEdit, TaskRead
from app.database import get_session
from app.services.tasks import TaskService
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.authentication import get_current_user_id

router = APIRouter(tags=["tasks"])

@router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: int, session: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    service = TaskService(session)
    return service.get_task_for_user(task_id, user_id)

@router.get("/workspaces/{workspace_id}/tasks", response_model=list[TaskRead])
def get_tasks_by_workspace_id(workspace_id: int, session: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    service = TaskService(session)
    return service.get_tasks_for_user(workspace_id, user_id)

@router.post("/workspaces/{workspace_id}/tasks", response_model=TaskRead)
def create_task(workspace_id: int, data: TaskCreate, session: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    service = TaskService(session)
    return service.create_task_for_user(workspace_id, user_id, data)

@router.patch("/tasks/{task_id}", response_model=TaskRead)
def edit_task(task_id: int, data: TaskEdit, session: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    service = TaskService(session)
    return service.edit_task_for_user(user_id, task_id, data)

@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, session: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    service = TaskService(session)
    service.delete_task_for_user(user_id, task_id)