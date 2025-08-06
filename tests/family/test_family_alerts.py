import pytest
from app.models.alert import Alert
from app.config.extensions import db
from datetime import datetime

def criar_alerta(family_id, asset_id=None, tipo="concentracao", mensagem="Concentração acima do limite", severidade="warning"):
    alerta = Alert(
        family_id=family_id,
        asset_id=asset_id,
        tipo=tipo,
        mensagem=mensagem,
        severidade=severidade,
        criado_em=datetime.utcnow()
    )
    db.session.add(alerta)
    db.session.commit()
    return alerta

def test_list_family_alerts_success(client, headers, family):
    criar_alerta(family.id)
    criar_alerta(family.id, tipo="liquidez", mensagem="Liquidez baixa", severidade="danger")
    response = client.get(f"/families/{family.id}/alerts", headers=headers)
    assert response.status_code == 200
    data = response.json
    assert isinstance(data, list)
    assert len(data) >= 2
    assert any(a["tipo"] == "concentracao" for a in data)
    assert any(a["tipo"] == "liquidez" for a in data)

def test_list_family_alerts_unauthenticated(client, family):
    response = client.get(f"/families/{family.id}/alerts")
    assert response.status_code == 401

def test_list_family_alerts_no_access(client, db, user, family):
    from app.models.family import Family
    outra_familia = Family(name="Outra Familia")
    db.session.add(outra_familia)
    db.session.commit()
    from flask_jwt_extended import create_access_token
    token = create_access_token(identity=str(user.id))
    headers = {"Authorization": f"Bearer {token}"}
    criar_alerta(outra_familia.id)
    response = client.get(f"/families/{outra_familia.id}/alerts", headers=headers)
    assert response.status_code == 403

def test_list_family_alerts_not_found(client, headers):
    response = client.get("/families/99999/alerts", headers=headers)
    assert response.status_code == 404 

def test_alerta_nao_duplicado(client, headers, family, asset_payload):
    # Cria dois ativos para garantir geração de alerta
    import uuid
    asset1 = asset_payload.copy(); asset1["value"] = 70000.0; asset1["name"] = "Alerta Não Duplicado 1 " + str(uuid.uuid4())
    asset2 = asset_payload.copy(); asset2["value"] = 20000.0; asset2["name"] = "Alerta Não Duplicado 2 " + str(uuid.uuid4())
    resp1 = client.post("/assets", json=asset1, headers=headers)
    resp2 = client.post("/assets", json=asset2, headers=headers)
    assert resp1.status_code == 201
    assert resp2.status_code == 201
    client.post(f"/families/{family.id}/alerts/trigger", headers=headers)
    # Gera novamente
    client.post(f"/families/{family.id}/alerts/trigger", headers=headers)
    response = client.get(f"/families/{family.id}/alerts", headers=headers)
    data = response.json
    assert sum(1 for a in data if a["tipo"] == "concentracao") == 1

def test_alerta_removido_se_condicao_some(client, headers, family, asset_payload, db):
    # Cria ativo que gera alerta de concentração
    payload = asset_payload.copy(); payload["value"] = 90000.0; payload["name"] = "Alerta Remove"
    resp = client.post("/assets", json=payload, headers=headers)
    asset_id = resp.json["id"]
    client.post(f"/families/{family.id}/alerts/trigger", headers=headers)
    # Reduz valor do ativo para remover alerta
    client.put(f"/assets/{asset_id}?family_id={family.id}", json={"value": 10000.0}, headers=headers)
    client.post(f"/families/{family.id}/alerts/trigger", headers=headers)
    db.session.commit()  # commit explícito para garantir sincronização
    response = client.get(f"/families/{family.id}/alerts", headers=headers)
    data = response.json
    assert all(a["tipo"] != "concentracao" for a in data)

def test_alerta_permissao(client, db, user, family, asset_payload):
    # Cria alerta com usuário autorizado
    from flask_jwt_extended import create_access_token
    token = create_access_token(identity=str(user.id))
    headers = {"Authorization": f"Bearer {token}"}
    payload = asset_payload.copy(); payload["value"] = 90000.0; payload["name"] = "Alerta Permissão"
    client.post("/assets", json=payload, headers=headers)
    client.post(f"/families/{family.id}/alerts/trigger", headers=headers)
    # Cria nova família sem vínculo
    from app.models.family import Family
    outra_familia = Family(name="Outra Familia Alertas"); db.session.add(outra_familia); db.session.commit()
    response = client.get(f"/families/{outra_familia.id}/alerts", headers=headers)
    assert response.status_code == 403 