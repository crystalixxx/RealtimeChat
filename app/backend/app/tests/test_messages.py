from app.tests.fixtures import client, session_fixture
from app.tests.test_chats import chat_create


def send_message(current_client, message_content) -> tuple:
    first_member_response, second_member_response, chat_creation_response = chat_create(
        current_client, "TestMessageCreateChat"
    )

    assert first_member_response.status_code == 200
    assert second_member_response.status_code == 200
    assert chat_creation_response.status_code == 200

    assert chat_creation_response.json()["name"] == "TestMessageCreateChat"

    response = current_client.post(
        f"/api/messages/{first_member_response.json()["id"]}/{chat_creation_response.json()['id']}",
        json={"content": message_content},
    )

    return (
        first_member_response,
        second_member_response,
        chat_creation_response,
        response,
    )


def test_message_create(client):
    (
        first_member_response,
        second_member_response,
        chat_creation_response,
        message_response,
    ) = send_message(client, "Hello World!")

    assert message_response.status_code == 200

    data = message_response.json()

    assert data["content"] == "Hello World!"
    assert data["chat_id"] == chat_creation_response.json()["id"]
    assert data["sender_id"] == chat_creation_response.json()["id"]


def test_message_delete(client):
    (
        first_member_response,
        second_member_response,
        chat_creation_response,
        message_response,
    ) = send_message(client, "Hello World!")

    assert message_response.status_code == 200

    data = message_response.json()

    assert data["content"] == "Hello World!"
    assert data["chat_id"] == chat_creation_response.json()["id"]
    assert data["sender_id"] == chat_creation_response.json()["id"]

    response = client.delete(f"/api/messages/{message_response.json()['id']}")

    assert response.status_code == 200
