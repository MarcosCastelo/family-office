import pytest

def test_register_existing_user(client, db):
    client.post("/auth/register", json={"email": "user3@example.com", "password": "senha123"})
    response = client.post("/auth/register", json={"email": "user3@example.com", "password": "senha123"})
    assert response.status_code in [400, 500]

@pytest.mark.parametrize("payload", [
    {"email": "", "password": "senha123"},
    {"email": "user4@example.com", "password": ""},
    {"email": "user4@example.com"},  # sem password
    {"password": "senha123"},  # sem email
    {},  # payload vazio
])
def test_register_invalid_payload(client, payload):
    response = client.post("/auth/register", json=payload)
    assert response.status_code in [400, 422, 500]

def test_login_wrong_password(client, db):
    client.post("/auth/register", json={"email": "user5@example.com", "password": "senha123"})
    response = client.post("/auth/login", json={"email": "user5@example.com", "password": "errada"})
    assert response.status_code == 401

def test_login_nonexistent_user(client):
    response = client.post("/auth/login", json={"email": "naoexiste@example.com", "password": "senha123"})
    assert response.status_code == 401

def test_login_missing_fields(client):
    response = client.post("/auth/login", json={"email": "user6@example.com"})
    assert response.status_code in [400, 422, 500] 