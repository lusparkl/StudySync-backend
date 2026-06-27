import os
import uvicorn
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.routers.user import router as user_router
from app.routers.workspace import router as workspace_router
from app.routers.task import router as task_router
from app.routers.note import router as note_router
from app.routers.auth import router as auth_router
from app.database import Base, engine
from app.auth.helpers import FRONTEND_URL, SECRET_KEY
from app import models #Need to create all tables

app = FastAPI(
    title="StudySync API",
    description="Platform to make your studies both enjoyable and effective"
)

allowed_origins = {
    FRONTEND_URL,
    "http://localhost:5173",
    "http://127.0.0.1:5173",
}
allowed_origins.update(
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(allowed_origins),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(workspace_router)
app.include_router(task_router)
app.include_router(note_router)
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to StudySync API!"}

@app.get("/health", tags=["system"])
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)

