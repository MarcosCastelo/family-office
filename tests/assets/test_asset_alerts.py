import pytest
from app.models.alert import Alert
from app.config.extensions import db

def contar_alertas(family_id, tipo):
    return Alert.query.filter_by(family_id=family_id, tipo=tipo).count()

def test_alerta_concentracao_gerado(client, headers, family, asset_payload):
    """Test that concentration alert is generated when asset > 30% of portfolio"""
    # Cria 2 ativos, um deles com valor > 30% da carteira, ambos com nomes únicos
    import uuid
    asset1 = asset_payload.copy()
    asset1["value"] = 70000.0
    asset1["name"] = "Ativo Conc " + str(uuid.uuid4())
    
    asset2 = asset_payload.copy()
    asset2["value"] = 20000.0
    asset2["name"] = "Ativo Conc " + str(uuid.uuid4())
    
    resp1 = client.post("/assets", json=asset1, headers=headers)
    resp2 = client.post("/assets", json=asset2, headers=headers)
    
    assert resp1.status_code == 201
    assert resp2.status_code == 201
    
    # Espera alerta de concentração
    client.post(f"/families/{family.id}/alerts/trigger", headers=headers)
    
    from app.models.alert import Alert
    from app.config.extensions import db
    db.session.commit()
    
    response = client.get(f"/families/{family.id}/alerts", headers=headers)
    assert response.status_code == 200
    
    data = response.get_json()  # Use get_json() instead of .json
    assert sum(1 for a in data if a["tipo"] == "concentracao") == 1

def test_alerta_nao_duplicado(client, headers, family, asset_payload):
    """Test that alerts are not duplicated when triggered multiple times"""
    # Cria dois ativos para garantir geração de alerta
    import uuid
    asset1 = asset_payload.copy()
    asset1["value"] = 90000.0
    asset1["name"] = "Alerta Não Duplicado 1 " + str(uuid.uuid4())
    
    asset2 = asset_payload.copy()
    asset2["value"] = 10000.0
    asset2["name"] = "Alerta Não Duplicado 2 " + str(uuid.uuid4())
    
    resp1 = client.post("/assets", json=asset1, headers=headers)
    resp2 = client.post("/assets", json=asset2, headers=headers)
    
    assert resp1.status_code == 201
    assert resp2.status_code == 201
    
    # Gera alertas
    client.post(f"/families/{family.id}/alerts/trigger", headers=headers)
    
    # Gera novamente
    client.post(f"/families/{family.id}/alerts/trigger", headers=headers)
    
    response = client.get(f"/families/{family.id}/alerts", headers=headers)
    assert response.status_code == 200
    
    data = response.get_json()  # Use get_json() instead of .json
    assert sum(1 for a in data if a["tipo"] == "concentracao") == 1

def test_alerta_liquidez_gerado(client, headers, family):
    """Test that liquidity alert is generated for low liquidity assets"""
    import io
    csv = (
        "name,asset_type,value,acquisition_date,details,family_id\n"
        f"Ativo1,renda_fixa,60000.0,2024-01-01,{{\"liquidez\": \"baixa\"}},{family.id}\n"
        f"Ativo2,renda_fixa,50000.0,2024-01-01,{{\"liquidez\": \"baixa\"}},{family.id}\n"
    )
    data = {'file': (io.BytesIO(csv.encode()), 'ativos.csv')}
    
    response = client.post('/assets/upload', content_type='multipart/form-data', headers=headers, data=data)
    assert response.status_code == 201
    
    # Força geração de alertas
    client.post(f"/families/{family.id}/alerts/trigger", headers=headers)
    
    # Consulta alertas via API
    response = client.get(f"/families/{family.id}/alerts", headers=headers)
    assert response.status_code == 200
    
    data = response.get_json()  # Use get_json() instead of .json
    assert any(a["tipo"] == "liquidez" for a in data) 