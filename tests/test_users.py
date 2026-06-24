from tests.conftest import client, auth_headers
from app.storage import profile_photos

def test_profile_photo_url_building_does_not_duplicate_slash(monkeypatch):
    monkeypatch.setattr(profile_photos, "PUBLIC_ENDPOINT", "https://images.example.com/")

    url = profile_photos.build_profile_photo_url("avatar.webp")

    assert url == "https://images.example.com/avatar.webp"

def test_getting_me(client, auth_headers):
    resonse = client.get("/users/me", headers=auth_headers)
    assert resonse.status_code == 200
    data = resonse.json()

    assert data["username"] == "test_user"
    assert data["email"] == "test@gmail.com"


def test_default_profile_photo(client, auth_headers):
    response = client.get("/users/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["profile_photo_link"] == "https://images.lusparkl.foo/default_avatar.webp"

def test_setting_profile_photo(client, auth_headers):
    with open("tests/assets/test_photo_1.jpg", "rb") as image:
        response = client.patch("/users/me/profile_picture", files={
            "file": ("test_photo_1.jpg", image, "image/jpeg")
            },
            headers=auth_headers
        )
    
    assert response.status_code == 200

    data = response.json()
    assert data["profile_photo_link"] is not None
    assert data["profile_photo_link"] != "https://images.lusparkl.foo/default_avatar.webp"

def test_deleting_profile_photo(client, auth_headers):
    with open("tests/assets/test_photo_1.jpg", "rb") as image:
        client.patch("/users/me/profile_picture", files={
            "file": ("test_photo_1.jpg", image, "image/jpeg")
            },
            headers=auth_headers
        )

    response = client.delete("/users/me/profile_picture", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    assert data["profile_photo_link"] == "https://images.lusparkl.foo/default_avatar.webp"

def test_changing_user_password(client, auth_headers):
    response = client.patch("/users/me/password", json={
        "old_password": "test_password",
        "new_password": "new_test_password"
    }, headers=auth_headers)

    assert response.status_code == 200

    # Try to login with old password
    login_response_old = client.post("/users/login", data={
        "username": "test_user",
        "password": "test_password"
    })
    assert login_response_old.status_code == 400

    # Try to login with new password
    login_response_new = client.post("/users/login", data={
        "username": "test_user",
        "password": "new_test_password"
    })
    assert login_response_new.status_code == 200
