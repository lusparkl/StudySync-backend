from __future__ import annotations

from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    profile_photo_link: Mapped[str] = mapped_column(nullable=False)

    workspaces: Mapped[list[Workspace]] = relationship(back_populates="owner")
    tasks: Mapped[list[Task]] = relationship(back_populates="owner")
    notes: Mapped[list[Note]] = relationship(back_populates="owner")
    shared_workspaces: Mapped[list[Workspace]] = relationship(back_populates="contributors")

class Workspace(Base):
    __tablename__ = "workspaces"

    workspace_id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    avatar_link: Mapped[str] = mapped_column(nullable=False)
    deadline: Mapped[datetime] = mapped_column(nullable=True)

    owner: Mapped[User] = relationship(back_populates="workspaces")
    tasks: Mapped[list[Task]] = relationship(back_populates="workspace")
    contributors: Mapped[list[User]] = relationship(back_populates="shared_workspaces")

class Task(Base):
    __tablename__ = "tasks"

    task_id: Mapped[int] = mapped_column(primary_key=True)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.workspace_id"), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(nullable=True)

    owner: Mapped[User] = relationship(back_populates="tasks", )
    workspace: Mapped[Workspace] = relationship(back_populates="tasks")
    notes: Mapped[list[Note]] = relationship(back_populates="task")

class Note(Base):
    __tablename__="notes"
    note_id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.task_id"), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(nullable=True)

    owner: Mapped[User] = relationship(back_populates="notes")
    task: Mapped[Task] = relationship(back_populates="notes")
