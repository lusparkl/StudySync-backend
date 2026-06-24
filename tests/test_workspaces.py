from tests.conftest import client, auth_headers

def _create_workspace(client, auth_headers, title: str = "Test workspace", description: str = "This is test workspace"):
    return client.post("/workspaces", json={
        "title": title,
        "description": description
    },
    headers=auth_headers)

def _create_user_headers(client, username: str, email: str):
    responce = client.post("/users", json={
        "username": username,
        "email": email,
        "password": "test_password"
    })

    assert responce.status_code == 200

    return {
        "Authorization": f"Bearer {responce.json()['access_token']}"
    }

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

def test_workspace_invite_accepting(client, auth_headers):
    create_responce = _create_workspace(client, auth_headers)
    workspace_id = create_responce.json()["workspace_id"]
    second_user_headers = _create_user_headers(client, "second_user", "second@gmail.com")

    invite_responce = client.post(f"/workspaces/{workspace_id}/invites", headers=auth_headers)
    assert invite_responce.status_code == 200

    invite_link = invite_responce.json()["invite_link"]
    assert isinstance(invite_link, str)

    accept_responce = client.post(f"/invites/{invite_link}", headers=second_user_headers)
    assert accept_responce.status_code == 200

    accept_responce = client.post(f"/invites/{invite_link}", headers=second_user_headers)
    assert accept_responce.status_code == 200

    workspace_responce = client.get(f"/workspaces/{workspace_id}", headers=second_user_headers)
    assert workspace_responce.status_code == 200

    workspace = workspace_responce.json()
    assert workspace["workspace_id"] == workspace_id
    assert workspace["contributors"][0]["username"] == "second_user"
