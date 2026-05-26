from sqlalchemy import select, or_
from app.models import Workspace, User
from sqlalchemy.orm import Session
from app.schemas import WorkspaceEdit, WorkspaceCreate

class WorkspacesRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: WorkspaceCreate, user_id: int) -> Workspace:
        workspace = Workspace(
            title=data.title,
            description=data.description,
            deadline=data.deadline,
            owner_id = user_id,
        )

        self.session.add(workspace)
        self.session.commit()
        self.session.refresh(workspace)

        return workspace
    
    def edit(self, data: WorkspaceEdit, workspace_id) -> Workspace | None:
        workspace = self.session.get(Workspace, workspace_id)

        if workspace == None:
            return None
        
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(workspace, field, value)
        
        self.session.commit()
        self.session.refresh(workspace)

        return workspace
    
    def get_by_user_id(self, user_id) -> list[Workspace]:
        stm = select(Workspace).where(or_(Workspace.owner_id == user_id, Workspace.contributors.any(User.user_id == user_id)))
        return list(self.session.scalars(stm).all())
    
    def get_by_id(self, workspace_id) -> Workspace | None:
        return self.session.get(Workspace, workspace_id)
    
    def delete(self, workspace_id: int) -> bool:
        workspace = self.session.get(Workspace, workspace_id)

        if workspace is None:
            return False
        
        self.session.delete(workspace)
        self.session.commit()

        return True