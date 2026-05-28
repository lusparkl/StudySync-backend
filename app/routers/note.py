from app.schemas import NoteCreate, NoteEdit, NoteRead
from app.database import get_session
from app.services.notes import NoteService
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.authentication import get_current_user_id

router = APIRouter(tags={"notes"})

@router.get("/notes/{note_id}", response_model=NoteRead)
def get_note_by_id(note_id: int, session: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    service = NoteService(session)
    return service.get_note_for_user(note_id, user_id)

@router.get("/tasks/{task_id}/notes", response_model=list[NoteRead])
def get_notes_by_task_id(task_id: int, session: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    service = NoteService(session)
    return service.get_notes_for_user(task_id, user_id)

@router.post("/tasks/{task_id}/notes", response_model=NoteRead)
def create_note(task_id: int, data: NoteCreate, session: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    service = NoteService(session)
    return service.create_note_for_user(task_id, user_id, data)

@router.patch("/notes/{note_id}", response_model=NoteRead)
def edit_note(note_id: int, data: NoteEdit, session: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    service = NoteService(session)
    return service.edit_note_for_user(note_id, user_id, data)

@router.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, session: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    service = NoteService(session)
    return service.delte_note_for_user(note_id, user_id)