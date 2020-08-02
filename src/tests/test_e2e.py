def test_healthcheck(flask_client):
    client = flask_client
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_users_inserting_and_retrieving_two_users(flask_client):
    client = flask_client
    user1 = {"name": "marco", "email": "aa@aa.aa", "phone": "1234556"}
    user2 = {"name": "don corleone", "email": "ab@aa.aa", "phone": "1234551"}
    response = client.post("/users", json=user1)
    user1["id"] = 1
    assert response.status_code == 201
    assert response.json == user1
    response = client.post("/users", json=user2)
    user2["id"] = 2
    assert response.status_code == 201
    assert response.json == user2

    response = client.get("/users")
    assert response.status_code == 200
    assert response.json == [user1, user2]


def test_users_create_user_with_empty_request(flask_client):
    client = flask_client
    response = client.post("/users", json={})
    assert response.status_code == 400
    assert response.json == {"name": ["Missing data for required field."]}


def test_users_create_with_more_fields_than_necessary(flask_client):
    client = flask_client
    user1 = {
        "name": "marco",
        "email": "aa@aa.aa",
        "phone": "1231556",
        "address": "some st, 123",
    }
    response = client.post("/users", json=user1)
    assert response.status_code == 201
    assert response.json == {
        "email": "aa@aa.aa",
        "id": 1,
        "name": "marco",
        "phone": "1231556",
    }
