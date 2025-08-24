import pytest

def test_get_family_risk_summary_success(client, headers, family):
    """Test successful risk summary retrieval"""
    response = client.get(f"/families/{family.id}/risk/summary", headers=headers)
    assert response.status_code == 200
    
    data = response.get_json()  # Use get_json() instead of .json
    assert data["family_id"] == family.id
    assert "score_global" in data
    assert "classificacao_final" in data

def test_get_family_risk_summary_unauthenticated(client, family):
    """Test risk summary without authentication"""
    response = client.get(f"/families/{family.id}/risk/summary")
    assert response.status_code == 401

def test_get_family_risk_summary_no_access(client, db, user, family):
    """Test risk summary for family without access"""
    # Cria nova família sem vínculo com o usuário
    from app.models.family import Family
    outra_familia = Family(name="Outra Familia")
    db.session.add(outra_familia)
    db.session.commit()
    
    from flask_jwt_extended import create_access_token
    token = create_access_token(identity=str(user.id))
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get(f"/families/{outra_familia.id}/risk/summary", headers=headers)
    assert response.status_code == 403

def test_get_family_risk_summary_not_found(client, headers):
    """Test risk summary for non-existent family"""
    response = client.get("/families/99999/risk/summary", headers=headers)
    assert response.status_code == 404 

def test_family_risk_score_concentrated(client, headers, family, asset_payload):
    """Test risk score calculation for concentrated portfolio"""
    # Cria ativos concentrados em um só
    payload1 = asset_payload.copy()
    payload1["value"] = 90000.0
    
    payload2 = asset_payload.copy()
    payload2["value"] = 10000.0
    
    # Criar ativos
    resp1 = client.post("/assets", json=payload1, headers=headers)
    resp2 = client.post("/assets", json=payload2, headers=headers)
    
    assert resp1.status_code == 201
    assert resp2.status_code == 201
    
    # Criar transações para dar valor aos ativos
    asset1_id = resp1.get_json()["id"]  # Use get_json() instead of .json
    asset2_id = resp2.get_json()["id"]  # Use get_json() instead of .json
    
    # Transação para o primeiro ativo (90k)
    transaction1 = {
        "asset_id": asset1_id,
        "transaction_type": "buy",
        "quantity": 9000.0,  # 90000 / 10
        "unit_price": 10.0,
        "transaction_date": "2024-01-01"
    }
    
    # Transação para o segundo ativo (10k)
    transaction2 = {
        "asset_id": asset2_id,
        "transaction_type": "buy",
        "quantity": 1000.0,  # 10000 / 10
        "unit_price": 10.0,
        "transaction_date": "2024-01-01"
    }
    
    client.post("/transactions", json=transaction1, headers=headers)
    client.post("/transactions", json=transaction2, headers=headers)
    
    response = client.get(f"/families/{family.id}/risk/summary", headers=headers)
    assert response.status_code == 200
    
    data = response.get_json()  # Use get_json() instead of .json
    assert data["concentracao"] >= 30
    assert data["score_global"] >= 30

def test_family_risk_score_liquidity(client, db, user, asset_payload):
    """Test risk score calculation for low liquidity portfolio"""
    import uuid
    
    # Cria família nova para o teste
    from app.models.family import Family
    from flask_jwt_extended import create_access_token
    
    family = Family(name="Família Liquidez Teste " + str(uuid.uuid4()), cash_balance=100000.0)
    db.session.add(family)
    db.session.commit()
    
    user.families.append(family)
    db.session.commit()
    
    token = create_access_token(identity=str(user.id))
    headers = {"Authorization": f"Bearer {token}"}
    
    # Cria ativos ilíquidos com nomes únicos
    name1 = "Ativo Ilíquido " + str(uuid.uuid4())
    name2 = "Ativo Ilíquido " + str(uuid.uuid4())
    details = {"liquidez": "baixa", "indexador": "IPCA", "vencimento": "2030-01-01"}
    
    payload1 = asset_payload.copy()
    payload1["value"] = 60000.0
    payload1["details"] = details
    payload1["name"] = name1
    payload1["family_id"] = family.id
    
    payload2 = asset_payload.copy()
    payload2["value"] = 50000.0
    payload2["details"] = details
    payload2["name"] = name2
    payload2["family_id"] = family.id
    
    resp1 = client.post("/assets", json=payload1, headers=headers)
    resp2 = client.post("/assets", json=payload2, headers=headers)
    
    assert resp1.status_code == 201, f"POST 1 falhou: {resp1.status_code}, {resp1.data}"
    assert resp2.status_code == 201, f"POST 2 falhou: {resp2.status_code}, {resp2.data}"
    
    # Criar transações para dar valor aos ativos
    asset1_id = resp1.get_json()["id"]  # Use get_json() instead of .json
    asset2_id = resp2.get_json()["id"]  # Use get_json() instead of .json
    
    # Transação para o primeiro ativo (60k)
    transaction1 = {
        "asset_id": asset1_id,
        "transaction_type": "buy",
        "quantity": 6000.0,  # 60000 / 10
        "unit_price": 10.0,
        "transaction_date": "2024-01-01"
    }
    
    # Transação para o segundo ativo (50k)
    transaction2 = {
        "asset_id": asset2_id,
        "transaction_type": "buy",
        "quantity": 5000.0,  # 50000 / 10
        "unit_price": 10.0,
        "transaction_date": "2024-01-01"
    }
    
    client.post("/transactions", json=transaction1, headers=headers)
    client.post("/transactions", json=transaction2, headers=headers)
    
    response = client.get(f"/families/{family.id}/risk/summary", headers=headers)
    assert response.status_code == 200
    
    data = response.get_json()  # Use get_json() instead of .json
    # O controller retorna 'liquidez_aggregada', não 'liquidez'
    assert data["liquidez_aggregada"] >= 20
    assert data["score_global"] >= 20

def test_family_risk_score_volatility(client, headers, family, asset_payload):
    """Test risk score calculation for high volatility portfolio"""
    # Cria ativos com alta volatilidade
    payload1 = asset_payload.copy()
    payload1["asset_type"] = "renda_variavel"
    payload1["value"] = 50000.0
    
    payload2 = asset_payload.copy()
    payload2["asset_type"] = "criptomoeda"
    payload2["value"] = 30000.0
    
    # Criar ativos
    resp1 = client.post("/assets", json=payload1, headers=headers)
    resp2 = client.post("/assets", json=payload2, headers=headers)
    
    assert resp1.status_code == 201
    assert resp2.status_code == 201
    
    # Criar transações para dar valor aos ativos
    asset1_id = resp1.get_json()["id"]  # Use get_json() instead of .json
    asset2_id = resp2.get_json()["id"]  # Use get_json() instead of .json
    
    # Transação para o primeiro ativo (50k)
    transaction1 = {
        "asset_id": asset1_id,
        "transaction_type": "buy",
        "quantity": 5000.0,  # 50000 / 10
        "unit_price": 10.0,
        "transaction_date": "2024-01-01"
    }
    
    # Transação para o segundo ativo (30k)
    transaction2 = {
        "asset_id": asset2_id,
        "transaction_type": "buy",
        "quantity": 3000.0,  # 30000 / 10
        "unit_price": 10.0,
        "transaction_date": "2024-01-01"
    }
    
    client.post("/transactions", json=transaction1, headers=headers)
    client.post("/transactions", json=transaction2, headers=headers)
    
    response = client.get(f"/families/{family.id}/risk/summary", headers=headers)
    assert response.status_code == 200
    
    data = response.get_json()  # Use get_json() instead of .json
    assert data["volatilidade"] >= 30
    assert data["score_global"] >= 30 