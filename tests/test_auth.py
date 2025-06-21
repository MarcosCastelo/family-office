"""Testes relacionados a autoriação e criação de usuário"""

def test_register_user(client):
    """Receive client check if user are created"""
    response = client.post("/auth/register", json={
        "email": "user1@example.com",
        "password": "senha123"
    })
    assert response.status_code == 201
    assert b"Usuario criado" in response.data

def test_login_user(client):
    """Receive client check if correct user/passwd is logged"""
    client.post("/auth/register", json={
        "email": "user2@example.com",
        "password": "senha123"
    })
    response = client.post("/auth/login", json={
        "email": "user2@example.com",
        "password": "senha123"
    })

    assert response.status_code == 200
    json = response.get_json()
    assert "access_token" in json
