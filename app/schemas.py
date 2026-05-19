from pydantic import BaseModel, ConfigDict
from __future__ import annotations
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    
class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    username: str
    email: str
    profile_photo_link: str | None = None
    workspaces: list[WorkspaceRead] = []

class UserEdit(BaseModel):
    username: str | None = None
    email: str | None = None

class WorkspaceCreate(BaseModel): #You'll get owner id from jwt
    title: str
    description: str | None = None
    deadline: datetime | None = None

class WorkspaceRead(WorkspaceCreate): 
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    owner_id: int
    avatar_link: str | None = None
    tasks: list[TaskRead] = []

class WorkspaceEdit(BaseModel):
    title: str | None = None
    description: str | None = None
    deadline: datetime | None = None

class TaskCreate(BaseModel): # You'll get owner id from jwt, and workspace id from the link params
    title: str
    text: str | None = None

class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    owner_id: int
    workspace_id: int
    title: str
    text: str | None

class TaskEdit(BaseModel):
    title: str | None = None
    text: str | None = None

