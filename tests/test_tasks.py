from tests.test_workspaces import _create_workspace
from tests.conftest import client, auth_headers

def _create_task(client, auth_headers, workspace_id: int):
    return client.post(f"/workspaces/{workspace_id}/tasks", json={
        "title": "Test task",
        "text": "Test task text"
    },
    headers=auth_headers)

def test_task_creation(client, auth_headers):
    workspace_id = _create_workspace(client, auth_headers).json()["workspace_id"]
    response = _create_task(client, auth_headers, workspace_id)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test task"
    assert data["text"] == "Test task text"
    assert isinstance(data["task_id"], int)

def test_task_retrieval(client, auth_headers):
    workspace_id = _create_workspace(client, auth_headers).json()["workspace_id"]
    task_id = _create_task(client, auth_headers, workspace_id).json()["task_id"]

    response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test task"
    assert data["text"] == "Test task text"
    assert isinstance(data["task_id"], int)

def test_getting_workspace_tasks(client, auth_headers):
    workspace_id = _create_workspace(client, auth_headers).json()["workspace_id"]
    _create_task(client, auth_headers, workspace_id)
    _create_task(client, auth_headers, workspace_id)

    response = client.get(f"/workspaces/{workspace_id}/tasks", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Test task"

def test_task_editing(client, auth_headers):
    workspace_id = _create_workspace(client, auth_headers).json()["workspace_id"]
    task_id = _create_task(client, auth_headers, workspace_id).json()["task_id"]

    response = client.patch(f"/tasks/{task_id}",json={
        "title": "Changed task title"
    }, headers=auth_headers)
    
    assert response.status_code == 200
    assert response.json()["title"] == "Changed task title"

def test_task_deletion(client, auth_headers):
    workspace_id = _create_workspace(client, auth_headers).json()["workspace_id"]
    task_id = _create_task(client, auth_headers, workspace_id).json()["task_id"]

    response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 204

    get_responce = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert get_responce.status_code == 404
