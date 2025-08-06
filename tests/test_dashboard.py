import pytest

def test_dashboard_success(client, headers, family, asset_payload):
    # Cria alguns ativos
    asset1 = asset_payload.copy()
    asset1["asset_type"] = "renda_fixa"
    asset1["value"] = 10000.0
    asset2 = asset_payload.copy()
    asset2["asset_type"] = "renda_variavel"
    asset2["value"] = 20000.0
    client.post("/assets", json=asset1, headers=headers)
    client.post("/assets", json=asset2, headers=headers)
    response = client.get(f"/dashboard?family_id={family.id}", headers=headers)
    assert response.status_code == 200
    data = response.json
    assert "valor_total" in data
    assert "num_ativos" in data
    assert "distribuicao_classes" in data
    assert "top_ativos" in data
    assert "alertas_recentes" in data
    assert "score_risco" in data

def test_dashboard_unauthenticated(client, family):
    response = client.get(f"/dashboard?family_id={family.id}")
    assert response.status_code == 401

def test_dashboard_no_access(client, db, user, family):
    from app.models.family import Family
    outra_familia = Family(name="Outra Familia")
    db.session.add(outra_familia)
    db.session.commit()
    from flask_jwt_extended import create_access_token
    token = create_access_token(identity=str(user.id))
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/dashboard?family_id={outra_familia.id}", headers=headers)
    assert response.status_code == 403

def test_dashboard_family_not_found(client, headers):
    response = client.get("/dashboard?family_id=99999", headers=headers)
    assert response.status_code == 404 