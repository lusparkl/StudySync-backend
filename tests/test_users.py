from tests.conftest import client, auth_headers

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