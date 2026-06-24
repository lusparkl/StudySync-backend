from fastapi import HTTPException, Response, status
from app.repositories.workspaces import WorkspacesRepository
from app.schemas import WorkspaceCreate, WorkspaceEdit
from app.auth.invites import create_invite_token, encode_invite_token

class WorkspacesService:
    def __init__(self, session):
        self.workspace_repository = WorkspacesRepository(session)
    
    def _get_workspace_or_404(self, workspace_id: int):
        workspace = self.workspace_repository.get_by_id(workspace_id)

        if workspace is None:
            raise HTTPException(status_code=404, detail="Workspace not found.")
        
        return workspace
    
    def _check_is_user_allowed(self, workspace, user_id: int):
        for contributor in workspace.contributors:
            if contributor.user_id == user_id:
                return
        
        if user_id != workspace.owner_id:
            raise HTTPException(status_code=403, detail="Forbidden.")
        
    def get_workspace_for_user(self, workspace_id: int, user_id: int):
        workspace = self._get_workspace_or_404(workspace_id)
        self._check_is_user_allowed(workspace, user_id)

        return workspace
    
    def get_workspaces_for_user(self, user_id: int):
        return self.workspace_repository.get_by_user_id(user_id)

    def create_workspace_for_user(self, user_id: int, data: WorkspaceCreate):
        return self.workspace_repository.create(data, user_id)

    def edit_workspace_for_user(self, workspace_id: int, user_id: int, data: WorkspaceEdit):
        workspace = self._get_workspace_or_404(workspace_id)
        self._check_is_user_allowed(workspace, user_id)

        return self.workspace_repository.edit(data, workspace_id)
    
    def delete_workspace_for_user(self, workspace_id: int, user_id: int):
        workspace = self._get_workspace_or_404(workspace_id)
        self._check_is_user_allowed(workspace, user_id)

        if self.workspace_repository.delete(workspace_id):
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
    def create_invite_link_for_user(self, user_id: int, workspace_id: int):
        workspace = self._get_workspace_or_404(workspace_id)

        if workspace.owner_id != user_id:
            raise HTTPException(status_code=403, detail="Forbidden.")
        
        token = create_invite_token(workspace_id)

        return {"invite_link": token}
    
    def accept_invite_link_for_user(self, user_id: int, invite_token: str):
        try:
            data = encode_invite_token(invite_token)
            workspace_id = data["workspace_id"]
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid invite token.")
        
        workspace = self._get_workspace_or_404(workspace_id)
        self.workspace_repository.add_contributor(workspace.workspace_id, user_id)

        return {"message": "Invite accepted."}
