from tests.conftest import client, auth_headers

def _create_workspace(client, auth_headers, title: str = "Test workspace", description: str = "This is test workspace"):
    return client.post("/workspaces", json={
        "title": title,
        "description": description
    },
    headers=auth_headers)

def test_workspace_creation(client, auth_headers):
    responce = client.post("/workspaces", json={
        "title": "Test workspace",
        "description": "This is test workspace"
    },
    headers=auth_headers)

    assert responce.status_code == 200

    data = responce.json()

    assert data["title"] == "Test workspace"
    assert data["description"] == "This is test workspace"
    assert isinstance(data["owner_id"], int) 
    assert isinstance(data["workspace_id"], int)

def test_getting_workspace_by_id(client, auth_headers):
    create_responce = _create_workspace(client, auth_headers)

    workspace_id = create_responce.json()["workspace_id"]

    responce = client.get(f"/workspaces/{workspace_id}", headers=auth_headers)

    assert responce.status_code == 200

    data = responce.json()

    assert data["title"] == "Test workspace"
    assert data["description"] == "This is test workspace"
    assert isinstance(data["owner_id"], int) 
    assert data["workspace_id"] == workspace_id

def test_getting_user_workspaces(client, auth_headers):
    _create_workspace(client, auth_headers)
    _create_workspace(client, auth_headers)
    _create_workspace(client, auth_headers)

    responce = client.get("/workspaces", headers=auth_headers)

    assert responce.status_code == 200
    
    data = responce.json()

    assert len(data) == 3

def test_updating_workspace(client, auth_headers):
    create_responce = _create_workspace(client, auth_headers)

    workspace_id = create_responce.json()["workspace_id"]

    edit_responce = client.patch(f"/workspaces/{workspace_id}", json={
        "title": "Changed workspace title.",
    },
    headers=auth_headers)

    assert edit_responce.status_code == 200

    responce = client.get(f"/workspaces/{workspace_id}", headers=auth_headers)
    workspace = responce.json()

    assert workspace["title"] == "Changed workspace title."

def test_deleting_workspace(client, auth_headers):
    create_responce = _create_workspace(client, auth_headers)
    workspace_id = create_responce.json()["workspace_id"]

    responce = client.delete(f"/workspaces/{workspace_id}", headers=auth_headers)
    assert responce.status_code == 204

    get_responce = client.get(f"/workspaces/{workspace_id}", headers=auth_headers)
    assert get_responce.status_code == 404