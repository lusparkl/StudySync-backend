from fastapi import HTTPException
from app.schemas import NoteCreate, NoteEdit
from app.repositories.notes import NotesRepository
from app.repositories.tasks import TasksRepository
from app.repositories.workspaces import WorkspacesRepository

class NoteService():
    def __init__(self, session):
        self.notes_repository = NotesRepository(session)
        self.tasks_repository = TasksRepository(session)
        self.workspace_repository = WorkspacesRepository(session)
    
    def _get_note_or_404(self, note_id: int):
        note = self.notes_repository.get_by_id(note_id)

        if note is None:
            raise HTTPException(status_code=404, detail="Note not found.")
        
        return note
    
    def _is_workspace_allowed(self, workspace_id: int, user_id: int):
        workspace = self.workspace_repository.get_by_id(workspace_id)

        if workspace is None:
            raise HTTPException(status_code=404, detail="Workspace not found.")
        
        if user_id != workspace.owner_id:
            raise HTTPException(status_code=403, detail="Not allowed.")
    
    def _get_task_or_404(self, task_id: int):
        task = self.tasks_repository.get_by_id(task_id)

        if task is None:
            raise HTTPException(status_code=404, detail="Task not found.")
        
        return task
    
    def get_note_for_user(self, note_id: int, workspace_id: int, task_id: int, user_id: int):
        self._is_workspace_allowed(workspace_id, user_id)
        self._get_task_or_404(task_id)
        note = self._get_note_or_404(note_id)

        return note
    
    def get_notes_for_user(self, workspace_id: int, task_id: int, user_id: int):
        self._is_workspace_allowed(workspace_id, user_id)
        self._get_task_or_404(task_id)
        return self.notes_repository.get_by_task(task_id)
    
    def edit_note_for_user(self, workspace_id: int, task_id: int, note_id: int, user_id: int, data: NoteEdit):
        self._is_workspace_allowed(workspace_id, user_id)
        self._get_task_or_404(task_id)
        note = self._get_note_or_404(note_id)


        return self.notes_repository.edit(data, note_id)
    
    def create_note_for_user(self, workspace_id: int, task_id: int, user_id: int, data: NoteCreate):
        self._is_workspace_allowed(workspace_id, user_id)
        self._get_task_or_404(task_id)

        return self.notes_repository.create(data, user_id, task_id)
    
    def delte_note_for_user(self, workspace_id: int, task_id: int, note_id: int, user_id: int):
        self._is_workspace_allowed(workspace_id, user_id)
        self._get_task_or_404(task_id)
        return self.notes_repository.delete(note_id)
