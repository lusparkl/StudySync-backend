from tests.conftest import client, auth_headers

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
    create_responce = client.post("/workspaces", json={
        "title": "Test workspace",
        "description": "This is test workspace"
    },
    headers=auth_headers)

    workspace_id = create_responce.json()["workspace_id"]

    responce = client.get(f"/workspaces/{workspace_id}", headers=auth_headers)

    assert responce.status_code == 200

    data = responce.json()

    assert data["title"] == "Test workspace"
    assert data["description"] == "This is test workspace"
    assert isinstance(data["owner_id"], int) 
    assert data["workspace_id"] == workspace_id

def test_getting_user_workspaces(client, auth_headers):
    client.post("/workspaces", json={"title": "Workspace - 1", "Description": "First workspace"}, headers=auth_headers)
    client.post("/workspaces", json={"title": "Workspace - 2", "Description": "Second workspace"}, headers=auth_headers)
    client.post("/workspaces", json={"title": "Workspace - 3", "Description": "Third workspace"}, headers=auth_headers)

    responce = client.get("/workspaces", headers=auth_headers)

    assert responce.status_code == 200
    
    data = responce.json()

    assert len(data) == 3
