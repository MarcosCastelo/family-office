import pytest

def test_get_asset_risk_success(client, headers, asset_payload):
    # Cria ativo
    resp = client.post("/assets", json=asset_payload, headers=headers)
    asset_id = resp.json["id"]
    family_id = asset_payload["family_id"]
    # Consulta risco
    response = client.get(f"/assets/{asset_id}/risk?family_id={family_id}", headers=headers)
    assert response.status_code == 200
    data = response.json
    assert data["id"] == asset_id
    assert "risco_mercado" in data
    assert "classificacao_final" in data


def test_get_asset_risk_not_found(client, headers):
    response = client.get("/assets/99999/risk?family_id=1", headers=headers)
    assert response.status_code == 404


def test_get_asset_risk_unauthenticated(client, asset_payload):
    # Cria ativo
    resp = client.post("/assets", json=asset_payload)
    asset_id = resp.json["id"] if resp.status_code == 201 else 1
    family_id = asset_payload["family_id"]
    response = client.get(f"/assets/{asset_id}/risk?family_id={family_id}")
    assert response.status_code == 401


def test_get_asset_risk_no_access(client, db, user, asset_payload, family):
    # Cria ativo em outra família com usuário autorizado
    from app.models.family import Family
    from app.models.user import User
    outra_familia = Family(name="Outra Familia")
    db.session.add(outra_familia)
    db.session.commit()
    # Cria usuário autorizado
    user_autorizado = User(email="autorizado@example.com")
    user_autorizado.set_password("123456")
    user_autorizado.families.append(outra_familia)
    db.session.add(user_autorizado)
    db.session.commit()
    from flask_jwt_extended import create_access_token
    token_autorizado = create_access_token(identity=str(user_autorizado.id))
    headers_autorizado = {"Authorization": f"Bearer {token_autorizado}"}
    payload = asset_payload.copy()
    payload["family_id"] = outra_familia.id
    resp = client.post("/assets", json=payload, headers=headers_autorizado)
    asset_id = resp.json["id"]
    # Agora tenta acessar com usuário SEM acesso
    token_nao_autorizado = create_access_token(identity=str(user.id))
    headers_nao_autorizado = {"Authorization": f"Bearer {token_nao_autorizado}"}
    response = client.get(f"/assets/{asset_id}/risk?family_id={outra_familia.id}", headers=headers_nao_autorizado)
    assert response.status_code == 403 

def test_asset_risk_classification_low(client, headers, asset_payload):
    # Ativo conservador (baixo risco)
    payload = asset_payload.copy()
    payload["asset_type"] = "renda_fixa"
    payload["details"] = {"indexador": "IPCA", "vencimento": "2030-01-01", "taxa": 6.5}
    payload["value"] = 10000.0
    resp = client.post("/assets", json=payload, headers=headers)
    asset_id = resp.json["id"]
    family_id = payload["family_id"]
    response = client.get(f"/assets/{asset_id}/risk?family_id={family_id}", headers=headers)
    data = response.json
    assert data["classificacao_final"] == "baixo"

def test_asset_risk_classification_high(client, headers, asset_payload):
    # Ativo arriscado (ex: renda_variavel, valor alto, sem governança)
    payload = asset_payload.copy()
    payload["asset_type"] = "renda_variavel"
    payload["details"] = {"ticker": "XPTO3", "setor": "cripto", "governanca": 10}
    payload["value"] = 1000000.0
    resp = client.post("/assets", json=payload, headers=headers)
    asset_id = resp.json["id"]
    family_id = payload["family_id"]
    response = client.get(f"/assets/{asset_id}/risk?family_id={family_id}", headers=headers)
    data = response.json
    assert data["classificacao_final"] in ["alto", "crítico"] 