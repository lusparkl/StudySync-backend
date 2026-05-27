from tests.test_tasks import _create_workspace, _create_task
from tests.conftest import client, auth_headers

def _create_note(client, auth_headers, workspace_id: int, task_id: int):
    return client.post(f"/workspaces/{workspace_id}/tasks/{task_id}/notes", json={"title": "Test note", "text": "Test note text"}, headers=auth_headers).json()

def test_note_creation(client, auth_headers):
    workspace_id = _create_workspace(client, auth_headers).json()["workspace_id"]
    task_id = _create_task(client, auth_headers, workspace_id).json()["task_id"]
    response = client.post(f"/workspaces/{workspace_id}/tasks/{task_id}/notes", json={"title": "Test note", "text": "Test note text"}, headers=auth_headers)

    assert response.status_code == 200
    data = response.json()

    assert data["title"] == "Test note"
    assert data["text"] == "Test note text"
    assert isinstance(data["note_id"], int)

def test_note_retrieval(client, auth_headers):
    workspace_id = _create_workspace(client, auth_headers).json()["workspace_id"]
    task_id = _create_task(client, auth_headers, workspace_id).json()["task_id"]
    note_id = _create_note(client, auth_headers, workspace_id, task_id)["note_id"]

    response = client.get(f"/workspaces/{workspace_id}/tasks/{task_id}/notes/{note_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()

    assert data["title"] == "Test note"
    assert data["text"] == "Test note text"
    assert data["note_id"] == note_id

def test_note_editing(client, auth_headers):
    workspace_id = _create_workspace(client, auth_headers).json()["workspace_id"]
    task_id = _create_task(client, auth_headers, workspace_id).json()["task_id"]
    note_id = _create_note(client, auth_headers, workspace_id, task_id)["note_id"]

    response = client.patch(f"/workspaces/{workspace_id}/tasks/{task_id}/notes/{note_id}", json={"title": "Edited note title"}, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()

    assert data["title"] == "Edited note title"

def test_note_deletion(client, auth_headers):
    workspace_id = _create_workspace(client, auth_headers).json()["workspace_id"]
    task_id = _create_task(client, auth_headers, workspace_id).json()["task_id"]
    note_id = _create_note(client, auth_headers, workspace_id, task_id)["note_id"]

    response = client.delete(f"/workspaces/{workspace_id}/tasks/{task_id}/notes/{note_id}", headers=auth_headers)
    assert response.status_code == 204

    get_response = client.get(f"/workspaces/{workspace_id}/tasks/{task_id}/notes/{note_id}", headers=auth_headers)
    assert get_response.status_code == 404