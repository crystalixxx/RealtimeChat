from app.tests.fixtures import client, session_fixture


def test_user_creation(client):
    response = client.post(
        "/api/users/",
        json={
            "username": "Maxim",
            "is_superuser": False,
            "is_blocked": False,
            "password": "123456",
        },
    )
    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "Maxim"
    assert not data["is_superadmin"]
    assert not data["is_blocked"]
    assert data["hashed_password"] != "123456"  # храним захешированный пароль


def test_user_delete(client):
    responses = client.delete("/api/users/2")

    assert responses.status_code == 404

    responses = client.delete("/api/users/1")

    assert responses.status_code == 409


def test_user_update(client):
    responses = client.post(
        "/api/users/",
        json={
            "username": "Maxim",
            "is_superuser": False,
            "is_blocked": False,
            "password": "12345363432",
        },
    )
    response = client.get("/api/users/user/1")

    assert response.status_code == 200

    old_data = response.json()

    response = client.patch(
        "/api/users/1",
        json={
            "username": "Maxim123",
            "is_superuser": False,
            "is_blocked": False,
            "password": "6755432322",
        },
    )

    assert response.status_code == 200

    new_data = response.json()

    assert new_data["username"] == "Maxim123"
    assert not new_data["is_superadmin"]
    assert not new_data["is_blocked"]
    assert new_data["hashed_password"] != old_data["hashed_password"]
