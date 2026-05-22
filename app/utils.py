from app.database import SessionLocal
from collections.abc import Generator
from sqlalchemy.orm import Session

def get_session() -> Generator[Session, None, None]:
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()