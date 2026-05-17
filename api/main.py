from fastapi import Body, FastAPI, HTTPException

import api.mock as mock

app = FastAPI()


def find_workspace(workspace_id: int):
    for workspace in mock.workspaces:
        if workspace["id"] == workspace_id:
            return workspace
    return None


def find_task(task_id: int):
    for task in mock.tasks:
        if task["id"] == task_id:
            return task
    return None


def find_note(note_id: int):
    for note in mock.notes:
        if note["id"] == note_id:
            return note
    return None


def add_activity(workspace_id: int, activity_type: str, text: str):
    new_id = 1
    if mock.activity:
        new_id = mock.activity[-1]["id"] + 1

    mock.activity.append(
        {
            "id": new_id,
            "workspace_id": workspace_id,
            "type": activity_type,
            "text": text,
        }
    )


def get_progress_data(workspace_id: int):
    workspace_tasks = []

    for task in mock.tasks:
        if task["workspace_id"] == workspace_id:
            workspace_tasks.append(task)

    total_tasks = len(workspace_tasks)
    done_tasks = 0

    for task in workspace_tasks:
        if task["status"] == "done":
            done_tasks += 1

    if total_tasks == 0:
        progress = 0
    else:
        progress = int((done_tasks / total_tasks) * 100)

    return {
        "workspace_id": workspace_id,
        "total_tasks": total_tasks,
        "done_tasks": done_tasks,
        "left_tasks": total_tasks - done_tasks,
        "progress": progress,
    }


@app.get("/me")
def get_me():
    return mock.me


@app.get("/workspaces")
def get_workspaces():
    return {"workspaces": mock.workspaces}


@app.get("/workspaces/{workspace_id}")
def get_workspace(workspace_id: int):
    workspace = find_workspace(workspace_id)

    if workspace is None:
        raise HTTPException(status_code=404, detail="Workspace not found")

    result = workspace.copy()
    result["progress"] = get_progress_data(workspace_id)["progress"]
    return result


@app.get("/workspaces/{workspace_id}/tasks")
def get_workspace_tasks(workspace_id: int):
    workspace = find_workspace(workspace_id)

    if workspace is None:
        raise HTTPException(status_code=404, detail="Workspace not found")

    workspace_tasks = []

    for task in mock.tasks:
        if task["workspace_id"] == workspace_id:
            workspace_tasks.append(task)

    return {"tasks": workspace_tasks}


@app.patch("/tasks/{task_id}")
def patch_task(task_id: int, data: dict = Body(...)):
    task = find_task(task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    for key in data:
        task[key] = data[key]

    add_activity(task["workspace_id"], "task", f"Updated task: {task['title']}")

    return {"task": task}


@app.get("/workspaces/{workspace_id}/notes")
def get_workspace_notes(workspace_id: int):
    workspace = find_workspace(workspace_id)

    if workspace is None:
        raise HTTPException(status_code=404, detail="Workspace not found")

    workspace_notes = []

    for note in mock.notes:
        if note["workspace_id"] == workspace_id:
            workspace_notes.append(note)

    return {"notes": workspace_notes}


@app.post("/notes")
def post_note(data: dict = Body(...)):
    workspace = find_workspace(data["workspace_id"])

    if workspace is None:
        raise HTTPException(status_code=404, detail="Workspace not found")

    new_id = 1
    if mock.notes:
        new_id = mock.notes[-1]["id"] + 1

    new_note = {
        "id": new_id,
        "workspace_id": data["workspace_id"],
        "title": data["title"],
        "content": data["content"],
    }

    mock.notes.append(new_note)
    add_activity(new_note["workspace_id"], "note", f"Created note: {new_note['title']}")

    return {"note": new_note}


@app.patch("/notes/{note_id}")
def patch_note(note_id: int, data: dict = Body(...)):
    note = find_note(note_id)

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    for key in data:
        note[key] = data[key]

    add_activity(note["workspace_id"], "note", f"Updated note: {note['title']}")

    return {"note": note}


@app.get("/workspaces/{workspace_id}/activity")
def get_workspace_activity(workspace_id: int):
    workspace = find_workspace(workspace_id)

    if workspace is None:
        raise HTTPException(status_code=404, detail="Workspace not found")

    workspace_activity = []

    for item in mock.activity:
        if item["workspace_id"] == workspace_id:
            workspace_activity.append(item)

    return {"activity": workspace_activity}


@app.get("/workspaces/{workspace_id}/progress")
def get_workspace_progress(workspace_id: int):
    workspace = find_workspace(workspace_id)

    if workspace is None:
        raise HTTPException(status_code=404, detail="Workspace not found")

    return get_progress_data(workspace_id)
