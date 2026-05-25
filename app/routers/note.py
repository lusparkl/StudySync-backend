from app.schemas import NoteCreate, NoteEdit, NoteRead
from app.database import get_session
from app.services.notes import NoteService
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.authentication import get_current_user_id

router = APIRouter(prefix="/workspaces/{workspace_id}/tasks/{task_id}/notes", tags={"notes"})

@router.get("/{note_id}", response_model=NoteRead)
def get_note_by_id(workspace_id: int, task_id: int, note_id: int, session: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    service = NoteService(session)
    return service.get_note_for_user(note_id, workspace_id, task_id, user_id)

@router.get("", response_model=list[NoteRead])
def get_notes_by_task_id(workspace_id: int, task_id: int, session: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    service = NoteService(session)
    return service.get_notes_for_user(workspace_id, task_id, user_id)

@router.post("", response_model=NoteRead)
def create_note(workspace_id: int, task_id: int, data: NoteCreate, session: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    service = NoteService(session)
    return service.create_note_for_user(workspace_id, task_id, user_id, data)

@router.patch("/{note_id}", response_model=NoteRead)
def edit_note(workspace_id: int, task_id: int, note_id: int, data: NoteEdit, session: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    service = NoteService(session)
    return service.edit_note_for_user(workspace_id, task_id, note_id, user_id, data)

@router.delete("/{note_id}", status_code=204)
def delete_note(workspace_id: int, task_id: int, note_id: int, session: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    service = NoteService(session)
    return service.delte_note_for_user(workspace_id, task_id, note_id, user_id)