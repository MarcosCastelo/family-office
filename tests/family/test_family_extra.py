from app.models.family import Family
import pytest

def test_join_nonexistent_family(client, db, access_token):
    response = client.post(
        f"/family/join/9999",
        headers={"Authorization": f"Bearer {access_token}"},
        json={}
    )
    assert response.status_code == 404

def test_join_family_unauthenticated(client, db, family):
    response = client.post(f"/family/join/{family.id}", json={})
    assert response.status_code == 401

def test_join_family_already_member(client, db, access_token, user, family):
    user.families.append(family)
    db.session.commit()
    response = client.post(
        f"/family/join/{family.id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json={}
    )
    assert response.status_code == 200
    assert b"associado" in response.data 