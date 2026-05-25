from app.schemas import NoteCreate, NoteEdit, NoteRead
from app.utils import get_session
from app.repositories.notes import NotesRepository
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(tags={"notes"})

@router.get("/notes/{note_id}", response_model=NoteRead)
def get_note_by_id(note_id: int, session: Session = Depends(get_session)):
    rep = NotesRepository(session)
    result = rep.get_by_id(note_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Note not found.")
    
    return result

@router.post("/tasks/{task_id}/notes", response_model=NoteRead)
def create_note(task_id: int, data: NoteCreate, session: Session = Depends(get_session)):
    rep = NotesRepository(session)
    user_id = 1
    return rep.create(data, user_id, task_id)

@router.patch("/notes/{note_id}", response_model=NoteRead)
def edit_note(note_id: int, data: NoteEdit, session: Session = Depends(get_session)):
    rep = NotesRepository(session)
    result = rep.edit(data, note_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Note not found.")
    
    return result

@router.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, session: Session = Depends(get_session)):
    rep = NotesRepository(session)
    deleted = rep.delete(note_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Note not found.")
    
    return None