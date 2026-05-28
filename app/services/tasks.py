from fastapi import HTTPException, Response, status
from app.repositories.tasks import TasksRepository
from app.repositories.workspaces import WorkspacesRepository
from app.schemas import TaskCreate, TaskEdit

class TaskService:
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
    
    def _is_workspace_allowed(self, user_id: int, task=None, workspace_id = None):
        if task:
            workspace = task.workspace
        else:
            workspace = self.workspace_repository.get_by_id(workspace_id)

        if workspace is None:
            raise HTTPException(status_code=404, detail="Workspace not found.")
        
        for contributor in workspace.contributors:
            if contributor.user_id == user_id:
                return
        
        if user_id != workspace.owner_id:
            raise HTTPException(status_code=403, detail="Not allowed.")
        
    def get_task_for_user(self, task_id: int, user_id: int):
        task = self._get_task_or_404(task_id)
        self._is_workspace_allowed(user_id, task=task)

        return task
    
    def get_tasks_for_user(self, workspace_id: int, user_id: int):
        self._is_workspace_allowed(user_id, workspace_id)
        return self.task_repository.get_by_workspace_id(workspace_id)
    
    def create_task_for_user(self, workspace_id: int, user_id: int, data: TaskCreate):
        self._is_workspace_allowed(user_id, workspace_id=workspace_id)
        return self.task_repository.create(data, user_id, workspace_id)
    
    def edit_task_for_user(self, user_id: int, task_id: int, data: TaskEdit):
        task = self._get_task_or_404(task_id)
        self._is_workspace_allowed(user_id, task=task)
        return self.task_repository.edit(data, task_id)
    
    def delete_task_for_user(self, user_id: int, task_id: int):
        task = self._get_task_or_404(task_id)
        self._is_workspace_allowed(user_id, task)
        if self.task_repository.delete(task_id):
            return Response(status_code=status.HTTP_204_NO_CONTENT)