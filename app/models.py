from sqlalchemy import ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column
from __future__ import annotations
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    profile_photo_link: Mapped[str] = mapped_column(nullable=False)

    workspaces: Mapped[list[Workspace]] = relationship(back_populates="owner")
    tasks: Mapped[list[Task]] = relationship(back_populates="owner")

class Workspace(Base):
    __tablename__ = "workspaces"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column()
    avatar_link: Mapped[str] = mapped_column(nullable=False)
    deadline: Mapped[datetime] = mapped_column()

    owner: Mapped[User] = relationship(back_populates="workspaces")
    tasks: Mapped[list[Task]] = relationship(back_populates="workspace")

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column()

    owner: Mapped[User] = relationship(back_populates="tasks")
    workspace: Mapped[Workspace] = relationship(back_populates="tasks")