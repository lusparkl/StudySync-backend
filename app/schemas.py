from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, ConfigDict

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    
class UserReadPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    user_id: int
    username: str
    profile_photo_link: str | None = None

class UserReadPrivate(UserReadPublic):
    email: str
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
    
    workspace_id: int
    owner_id: int
    avatar_link: str | None = None
    tasks: list[TaskRead] = []
    contributors: list[UserReadPublic] = []

class WorkspaceEdit(BaseModel):
    title: str | None = None
    description: str | None = None
    deadline: datetime | None = None

class TaskCreate(BaseModel): # You'll get owner id from jwt, and workspace id from the link params
    title: str
    text: str | None = None

class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    task_id: int
    owner_id: int
    workspace_id: int
    title: str
    text: str | None

class TaskEdit(BaseModel):
    title: str | None = None
    text: str | None = None

class NoteCreate(BaseModel): #owner id - jwt, task id - link
    title: str
    text: str | None = None

class NoteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    note_id: int
    owner_id: int
    task_id: int
    title: str
    text: str | None 

class NoteEdit(BaseModel):
    title: str | None = None
    text: str  | None = None

class Token(BaseModel):
    access_token: str
    token_type: str

    