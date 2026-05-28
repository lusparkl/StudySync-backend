from app.database import get_session
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from app.services.workspaces import WorkspacesService
from app.schemas import WorkspaceEdit, WorkspaceRead, WorkspaceCreate
from app.auth.authentication import get_current_user_id

router = APIRouter(tags=["workspaces"])

@router.get("/workspaces", response_model=list[WorkspaceRead]) # We'll need to get user id from jwt later
def get_workspaces_by_user(session: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    service = WorkspacesService(session)
    return service.get_workspaces_for_user(user_id)

@router.get("/workspaces/{workspace_id}", response_model=WorkspaceRead)
def get_by_id(workspace_id: int, session: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    service = WorkspacesService(session)
    return service.get_workspace_for_user(workspace_id, user_id)

@router.patch("/workspaces/{workspace_id}", response_model=WorkspaceRead)
def edit_workspace(workspace_id: int, data: WorkspaceEdit, session: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    service = WorkspacesService(session)
    return service.edit_workspace_for_user(workspace_id, user_id, data)

@router.post("/workspaces", response_model=WorkspaceRead) # We'll need to get user id from jwt later
def create_workspace(data: WorkspaceCreate, session: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    service = WorkspacesService(session)
    return service.create_workspace_for_user(user_id, data)

@router.post("/workspaces/{workspace_id}/invites")
def create_invite_link(workspace_id: int, session: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    service = WorkspacesService(session)
    return service.create_invite_link_for_user(user_id, workspace_id)

@router.post("/invites/{invite_token}")
def accept_invite_to_workspace(invite_token: str, session: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    service = WorkspacesService(session)
    return service.accept_invite_link_for_user(user_id, invite_token)

@router.delete("/workspaces/{workspace_id}")
def delete_workspace(workspace_id: int, session: Session = Depends(get_session), user_id: int = Depends(get_current_user_id)):
    service = WorkspacesService(session)
    return service.delete_workspace_for_user(workspace_id, user_id)