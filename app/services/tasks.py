from fastapi import HTTPException
from app.repositories.tasks import TasksRepository
from app.repositories.workspaces import WorkspacesRepository
from app.schemas import TaskCreate, TaskEdit

class TaskService():
    def __init__(self, session):
        self.task_repository = TasksRepository(session)
        self.workspace_repository = WorkspacesRepository(session)

    
    def _get_task_or_404(self, task_id: int):
        task = self.task_repository.get_by_id(task_id)

        if task is None:
            raise HTTPException(status_code=404, detail="Task not found.")
        
        return task
    
    def _is_user_allowed(self, task, user_id: int):
        if user_id != task.workspace.owner_id:
            raise HTTPException(status_code=403, detail="Not allowed.")
    
    def _is_workspace_allowed(self, workspace_id: int, user_id: int):
        workspace = self.workspace_repository.get_by_id(workspace_id)

        if workspace is None:
            raise HTTPException(status_code=404, detail="Workspace not found.")
        
        if user_id != workspace.owner_id:
            raise HTTPException(status_code=403, detail="Not allowed.")
        
    def get_task_for_user(self, task_id: int, user_id: int):
        task = self._get_task_or_404(task_id)
        self._is_user_allowed(task, user_id)

        return task
    
    def get_tasks_for_user(self, workspace_id: int, user_id: int):
        self._is_workspace_allowed(workspace_id, user_id)
        return self.task_repository.get_by_workspace_id(workspace_id)
    
    def create_task_for_user(self, workspace_id: int, user_id: int, data: TaskCreate):
        self._is_workspace_allowed(workspace_id, user_id)
        return self.task_repository.create(data, user_id, workspace_id)
    
    def edit_task_for_user(self, workspace_id: int, user_id: int, task_id: int, data: TaskEdit):
        self._get_task_or_404(task_id)
        self._is_workspace_allowed(workspace_id, user_id)
        return self.task_repository.edit(data, task_id)
    
    def delete_task_for_user(self, workspace_id: int, user_id: int, task_id: int):
        self._get_task_or_404(task_id)
        self._is_workspace_allowed(workspace_id, user_id)
        return self.task_repository.delete(task_id)