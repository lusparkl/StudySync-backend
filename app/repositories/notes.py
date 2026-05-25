from app.models import Note
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.schemas import NoteEdit, NoteCreate

class NotesRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, data: NoteCreate, user_id: int, task_id: int) -> Note:
        note = Note(
            title = data.title,
            text = data.text,
            owner_id = user_id,
            task_id = task_id
        )

        self.session.add(note)
        self.session.commit()
        self.session.refresh(note)

        return note
    
    def edit(self, data: NoteEdit, note_id: int) -> Note | None:
        note = self.session.get(Note, note_id)

        if note == None:
            return None
        
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(note, field, value)

        self.session.commit()
        self.session.refresh(note)

        return note
    
    def get_by_task(self, task_id: int) -> list[Note]:
        stm = select(Note).where(Note.task_id == task_id)
        return self.session.scalars(stm).all()
    
    def get_by_id(self, note_id: int) -> Note | None:
        return self.session.get(Note, note_id)
    
    def delete(self, note_id: int) -> bool:
        note = self.session.get(Note, note_id)

        if note is None:
            return False
        
        self.session.delete(note)
        self.session.commit()

        return True
