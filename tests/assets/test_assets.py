import pytest
from app.models.asset import Asset

def test_create_asset(client, headers, asset_payload):
    response = client.post("/assets", json=asset_payload, headers=headers)
    assert response.status_code == 201
    assert response.json["name"] == asset_payload["name"] 