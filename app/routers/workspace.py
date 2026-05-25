from app.utils import get_session
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException
from app.repositories.workspaces import WorkspacesRepository
from app.schemas import WorkspaceEdit, WorkspaceRead, WorkspaceCreate
from app.auth.authentication import get_current_user_id

router = APIRouter(prefix="/workspaces", tags=["workspaces"])

@router.get("", response_model=list[WorkspaceRead]) # We'll need to get user id from jwt later
def get_workspaces_by_user(session: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    rep = WorkspacesRepository(session)
    return rep.get_by_user_id(user_id)

@router.patch("/{workspace_id}", response_model=WorkspaceRead)
def edit_workspace(workspace_id: int, data: WorkspaceEdit, session: Session = Depends(get_session)):
    rep = WorkspacesRepository(session)
    result = rep.edit(data, workspace_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Workspace not found.")
    
    return result

@router.post("", response_model=WorkspaceRead) # We'll need to get user id from jwt later
def create_workspace(data: WorkspaceCreate, session: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    rep = WorkspacesRepository(session)
    result = rep.create(data, user_id)

    return result

@router.delete("/{workspace_id}")
def delete_workspace(workspace_id: int, session: Session = Depends(get_session)):
    rep = WorkspacesRepository(session)
    deleted = rep.delete(workspace_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Workspace not found.")