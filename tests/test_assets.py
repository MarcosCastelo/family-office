import pytest
from app.models.asset import Asset

@pytest.fixture()
def asset_payload(family):
    return {
        "name": "Tesouro IPCA",
        "asset_type": "renda_fixa",
        "value": 15000.0,
        "acquisition_date": "2024-01-01",
        "details": {
            "indexador": "IPCA",
            "vencimento": "2030-01-01",
            "taxa": 6.5
        },
        "family_id": family.id
    }
    
def test_create_asset(client, headers, asset_payload):
    response = client.post("/assets", json=asset_payload, headers=headers)
    assert response.status_code == 201
    assert response.json["name"] == asset_payload["name"]