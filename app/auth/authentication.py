from app.auth.helpers import decode_access_token, oauth2_scheme
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_session
from app.repositories.users import UsersRepository

def get_current_user_id(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> int:
    data = decode_access_token(token)
    rep = UsersRepository(session)

    if data is None or "sub" not in data:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_id = int(data["sub"])
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = rep.get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user_id
