from fastapi import APIRouter, Depends, HTTPException
from app.schemas import WorkspaceRead, WorkspaceEdit, WorkspaceCreate
from sqlalchemy.orm import Session
from app.utils import get_session
from app.repositories.workspaces import WorkspacesRepository

router = APIRouter(prefix="/workspaces", tags=["workspace"])

@router.get("", response_model=list[WorkspaceRead]) # We'll need to get user id from jwt later
def get_workspaces_by_user(session: Session = Depends(get_session)):
    user_id = 1
    rep = WorkspacesRepository(session)
    return rep.get_by_user_id(user_id)

@router.patch("/{workspace_id}", response_model=WorkspaceRead)
def edit_workspace(workspace_id: int, data: WorkspaceEdit, session: Session = Depends(get_session)):
    rep = WorkspacesRepository(session)
    result = rep.edit(data, workspace_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    return result

@router.post("", response_model=WorkspaceRead) # We'll need to get user id from jwt later
def create_workspace(data: WorkspaceCreate, session: Session = Depends(get_session)):
    rep = WorkspacesRepository(session)
    user_id = 1
    result = rep.create(data, user_id)

    return result
