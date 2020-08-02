def test_healthcheck(flask_client):
    client = flask_client
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}
