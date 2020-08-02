from hamcrest import assert_that, has_entries


def test_messages_inserting_and_retrieving_two_messages(flask_client):
    client = flask_client
    user1 = {"name": "marco", "email": "aa@aa.aa", "phone": "1234556"}
    response = client.post("/users", json=user1)
    assert response.status_code == 201
    message1 = {
        "scheduled": "2040-08-02T16:12:12Z",
        "text": "message 1",
        "kind": "email",
        "user_id": 1,
    }
    message2 = {
        "scheduled": "2040-08-02T16:12:12Z",
        "text": "message 2",
        "kind": "email",
        "user_id": 1,
    }
    response = client.post("/messages", json=message1)
    assert response.status_code == 201
    assert_that(response.json, has_entries(message1))
    response = client.post("/messages", json=message2)
    assert response.status_code == 201
    assert_that(response.json, has_entries(message2))
    message1["status"] = "scheduled"
    message2["status"] = "scheduled"
    response = client.get("/messages")
    assert response.status_code == 200
    response_json = response.json

    assert_that(response_json[0], has_entries(message1))
    assert_that(response_json[1], has_entries(message2))


def test_users_create_user_with_empty_request(flask_client):
    client = flask_client
    response = client.post("/messages", json={})
    assert response.status_code == 400
    assert response.json == {
        "kind": ["Missing data for required field."],
        "scheduled": ["Missing data for required field."],
        "text": ["Missing data for required field."],
        "user_id": ["Missing data for required field."],
    }
