from fastapi import FastAPI, Response
from app.routers.user import router as user_router
from app.routers.workspace import router as workspace_router
from app.routers.task import router as task_router
from app.routers.note import router as note_router
from app.database import Base, engine
from app import models #Need to create all tables

app = FastAPI()
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(workspace_router)
app.include_router(task_router)
app.include_router(note_router)

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)