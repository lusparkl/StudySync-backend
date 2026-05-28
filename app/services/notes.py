from fastapi import HTTPException
from app.schemas import NoteCreate, NoteEdit
from app.repositories.notes import NotesRepository
from app.repositories.tasks import TasksRepository
from app.repositories.workspaces import WorkspacesRepository

class NoteService:
    def __init__(self, session):
        self.notes_repository = NotesRepository(session)
        self.tasks_repository = TasksRepository(session)
        self.workspace_repository = WorkspacesRepository(session)
    
    def _get_note_or_404(self, note_id: int):
        note = self.notes_repository.get_by_id(note_id)

        if note is None:
            raise HTTPException(status_code=404, detail="Note not found.")
        
        return note
    
    def _is_workspace_allowed(self, user_id: int, note = None, task = None):
        if note:
            task = note.task

        if task is None:
            raise HTTPException(status_code=404, detail="Task not found.")
        
        workspace = task.workspace
        if workspace is None:
            raise HTTPException(status_code=404, detail="Workspace not found.")
        
        for contributor in workspace.contributors:
            if contributor.user_id == user_id:
                return
        
        if user_id != workspace.owner_id:
            raise HTTPException(status_code=403, detail="Not allowed.")


    
    def get_note_for_user(self, note_id: int, user_id: int):
        note = self._get_note_or_404(note_id)
        self._is_workspace_allowed(user_id, note=note)

        return note
    
    def get_notes_for_user(self, task_id: int, user_id: int):
        task = self.tasks_repository.get_by_id(task_id)
        self._is_workspace_allowed(user_id, task=task)

        return task.notes
    
    def edit_note_for_user(self, note_id: int, user_id: int, data: NoteEdit):
        note = self._get_note_or_404(note_id)
        self._is_workspace_allowed(user_id, note)

        return self.notes_repository.edit(data, note_id)
    
    def create_note_for_user(self, task_id: int, user_id: int, data: NoteCreate):
        task = self.tasks_repository.get_by_id(task_id)
        self._is_workspace_allowed(user_id, task=task)

        return self.notes_repository.create(data, user_id, task_id)
    
    def delte_note_for_user(self, note_id: int, user_id: int):
        note = self._get_note_or_404(note_id)
        self._is_workspace_allowed(user_id, note)
        
        return self.notes_repository.delete(note_id)
