def _create_user_headers(client):
    response = client.post("/users", json={
        "username": "release_contributor",
        "email": "release_contributor@example.com",
        "password": "test_password"
    })

    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_invalid_access_token_returns_401(client):
    response = client.get(
        "/users/me",
        headers={"Authorization": "Bearer not-a-valid-token"}
    )

    assert response.status_code == 401


def test_contributor_cannot_delete_workspace(client, auth_headers):
    workspace_response = client.post(
        "/workspaces",
        json={"title": "Owner workspace"},
        headers=auth_headers
    )
    workspace_id = workspace_response.json()["workspace_id"]
    contributor_headers = _create_user_headers(client)
    invite_response = client.post(
        f"/workspaces/{workspace_id}/invites",
        headers=auth_headers
    )

    client.post(
        f"/invites/{invite_response.json()['invite_link']}",
        headers=contributor_headers
    )
    delete_response = client.delete(
        f"/workspaces/{workspace_id}",
        headers=contributor_headers
    )

    assert delete_response.status_code == 403
    assert client.get(
        f"/workspaces/{workspace_id}",
        headers=auth_headers
    ).status_code == 200
