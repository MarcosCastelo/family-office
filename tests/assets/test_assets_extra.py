import pytest
from app.models.asset import Asset

def test_create_asset_invalid_type(client, db, headers, asset_payload):
    payload = asset_payload.copy()
    payload["asset_type"] = "tipo_invalido"
    response = client.post("/assets", json=payload, headers=headers)
    assert response.status_code == 400

def test_create_asset_missing_fields(client, db, headers, asset_payload):
    payload = asset_payload.copy()
    del payload["name"]
    response = client.post("/assets", json=payload, headers=headers)
    assert response.status_code == 400

def test_create_asset_unauthenticated(client, db, asset_payload):
    response = client.post("/assets", json=asset_payload)
    assert response.status_code == 401

def test_create_asset_not_family_member(client, db, user, asset_payload, family):
    # Cria uma nova família à qual o usuário não pertence
    from app.models.family import Family
    outra_familia = Family(name="Outra Familia")
    db.session.add(outra_familia)
    db.session.commit()
    payload = asset_payload.copy()
    payload["family_id"] = outra_familia.id
    from flask_jwt_extended import create_access_token
    token = create_access_token(identity=str(user.id))
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/assets", json=payload, headers=headers)
    assert response.status_code == 403

def test_get_assets(client, db, headers, asset_payload):
    client.post("/assets", json=asset_payload, headers=headers)
    response = client.get(f"/assets?family_id={asset_payload['family_id']}", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_asset_not_found(client, db, headers):
    response = client.get("/assets/9999?family_id=1", headers=headers)
    assert response.status_code == 404

def test_update_asset(client, db, headers, asset_payload):
    resp = client.post("/assets", json=asset_payload, headers=headers)
    asset_id = resp.json["id"]
    update = {"name": "Novo Nome"}
    response = client.put(f"/assets/{asset_id}?family_id={asset_payload['family_id']}", json=update, headers=headers)
    assert response.status_code == 200
    assert response.json["name"] == "Novo Nome"

def test_delete_asset(client, db, headers, asset_payload):
    resp = client.post("/assets", json=asset_payload, headers=headers)
    asset_id = resp.json["id"]
    response = client.delete(f"/assets/{asset_id}?family_id={asset_payload['family_id']}", headers=headers)
    assert response.status_code == 204 

def test_create_asset_negative_value(client, db, headers, asset_payload):
    payload = asset_payload.copy()
    payload["value"] = -1000.0
    response = client.post("/assets", json=payload, headers=headers)
    assert response.status_code == 400
    payload["value"] = 0.0
    response = client.post("/assets", json=payload, headers=headers)
    assert response.status_code == 400

def test_create_asset_duplicate_name_ticker(client, db, headers, asset_payload):
    payload1 = asset_payload.copy()
    payload2 = asset_payload.copy()
    payload2["details"] = payload1["details"].copy()
    payload2["details"]["ticker"] = payload1["details"].get("ticker", "XPTO3")
    client.post("/assets", json=payload1, headers=headers)
    response = client.post("/assets", json=payload2, headers=headers)
    assert response.status_code == 400

def test_create_asset_missing_required_fields_by_class(client, db, headers, asset_payload):
    # Exemplo: renda_fixa exige indexador e vencimento
    payload = asset_payload.copy()
    payload["asset_type"] = "renda_fixa"
    payload["details"] = {"taxa": 6.5}  # faltando indexador e vencimento
    response = client.post("/assets", json=payload, headers=headers)
    assert response.status_code == 400
    # Exemplo: renda_variavel exige ticker
    payload = asset_payload.copy()
    payload["asset_type"] = "renda_variavel"
    payload["details"] = {"setor": "financeiro"}
    response = client.post("/assets", json=payload, headers=headers)
    assert response.status_code == 400

def test_edit_asset_no_access(client, db, user, asset_payload, family):
    # Cria ativo em outra família com usuário autorizado
    from app.models.family import Family
    from app.models.user import User
    outra_familia = Family(name="Outra Familia")
    db.session.add(outra_familia)
    db.session.commit()
    user_autorizado = User(email="autorizado2@example.com"); user_autorizado.set_password("123456"); user_autorizado.families.append(outra_familia); db.session.add(user_autorizado); db.session.commit()
    from flask_jwt_extended import create_access_token
    token_autorizado = create_access_token(identity=str(user_autorizado.id))
    headers_autorizado = {"Authorization": f"Bearer {token_autorizado}"}
    payload = asset_payload.copy(); payload["family_id"] = outra_familia.id
    resp = client.post("/assets", json=payload, headers=headers_autorizado)
    asset_id = resp.json["id"]
    # Tenta editar com usuário SEM acesso
    token_nao_autorizado = create_access_token(identity=str(user.id))
    headers_nao_autorizado = {"Authorization": f"Bearer {token_nao_autorizado}"}
    response = client.put(f"/assets/{asset_id}?family_id={outra_familia.id}", json={"name": "Novo Nome"}, headers=headers_nao_autorizado)
    assert response.status_code == 403

def test_delete_asset_no_access(client, db, user, asset_payload, family):
    # Cria ativo em outra família com usuário autorizado
    from app.models.family import Family
    from app.models.user import User
    outra_familia = Family(name="Outra Familia")
    db.session.add(outra_familia)
    db.session.commit()
    user_autorizado = User(email="autorizado3@example.com"); user_autorizado.set_password("123456"); user_autorizado.families.append(outra_familia); db.session.add(user_autorizado); db.session.commit()
    from flask_jwt_extended import create_access_token
    token_autorizado = create_access_token(identity=str(user_autorizado.id))
    headers_autorizado = {"Authorization": f"Bearer {token_autorizado}"}
    payload = asset_payload.copy(); payload["family_id"] = outra_familia.id
    resp = client.post("/assets", json=payload, headers=headers_autorizado)
    asset_id = resp.json["id"]
    # Tenta deletar com usuário SEM acesso
    token_nao_autorizado = create_access_token(identity=str(user.id))
    headers_nao_autorizado = {"Authorization": f"Bearer {token_nao_autorizado}"}
    response = client.delete(f"/assets/{asset_id}?family_id={outra_familia.id}", headers=headers_nao_autorizado)
    assert response.status_code == 403 