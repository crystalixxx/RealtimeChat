from app.tests.fixtures import client, session_fixture


def chat_create(current_client, chat_name) -> tuple:
    response_first_member = current_client.post(
        "/api/users/",
        json={
            "username": "test@gmail.com",
            "is_superadmin": False,
            "is_blocked": False,
            "password": "123456",
        },
    )

    # Создание второго пользователя
    response_second_member = current_client.post(
        "/api/users/",
        json={
            "username": "test2@gmail.com",
            "is_superadmin": False,
            "is_blocked": False,
            "password": "434y45",
        },
    )

    # Создание чата
    response_chat_creation = current_client.post(
        "/api/chats/2", json={"name": chat_name}
    )

    return response_first_member, response_second_member, response_chat_creation


def test_chat_creation(client):
    first_member_response, second_member_response, chat_creation_response = chat_create(
        client, "SuperChat"
    )

    assert first_member_response.status_code == 200
    assert second_member_response.status_code == 200
    assert chat_creation_response.status_code == 200

    assert chat_creation_response.json()["name"] == "SuperChat"

    # Проверка участников чата
    response = client.get("/api/chats/members/1")

    assert response.status_code == 200
    data = response.json()

    assert [user["id"] in (1, 2) for user in data]


def test_chat_delete(client):
    first_member_response, second_member_response, chat_creation_response = chat_create(
        client, "SecondTestChat"
    )

    assert first_member_response.status_code == 200
    assert second_member_response.status_code == 200
    assert chat_creation_response.status_code == 200

    assert chat_creation_response.json()["name"] == "SecondTestChat"

    response = client.delete("/api/chats/1")

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "SecondTestChat"


def test_chat_update(client):
    first_member_response, second_member_response, chat_creation_response = chat_create(
        client, "ThirdTestChat"
    )

    assert first_member_response.status_code == 200
    assert second_member_response.status_code == 200
    assert chat_creation_response.status_code == 200

    assert chat_creation_response.json()["name"] == "ThirdTestChat"

    response = client.patch("/api/chats/1", json={"name": "AnotherNaming"})

    assert response.status_code == 200
    assert response.json()["name"] == "AnotherNaming"
