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
    response = client.post(f"/families/join/{family.id}", json={})
    assert response.status_code == 401

def test_join_family_already_member(client, db, access_token, user, family):
    user.families.append(family)
    db.session.commit()
    response = client.post(
        f"/families/join/{family.id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json={}
    )
    assert response.status_code == 200
    assert b"associado" in response.data 

def test_create_family_duplicate_name(client, admin_user_fixture, db):
    from flask_jwt_extended import create_access_token
    token = create_access_token(identity=str(admin_user_fixture.id))
    headers = {"Authorization": f"Bearer {token}"}
    data = {"name": "Familia Unica"}
    client.post("/admin/families", json=data, headers=headers)
    response = client.post("/admin/families", json=data, headers=headers)
    assert response.status_code in [400, 409]

def test_create_family_missing_name(client, admin_user_fixture, db):
    from flask_jwt_extended import create_access_token
    token = create_access_token(identity=str(admin_user_fixture.id))
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/admin/families", json={}, headers=headers)
    assert response.status_code in [400, 422]

def test_list_families_only_linked(client, db, user, family):
    from flask_jwt_extended import create_access_token
    from app.models.family import Family
    outra_familia = Family(name="Outra Familia")
    db.session.add(outra_familia)
    db.session.commit()
    user.families.append(family)
    db.session.commit()
    token = create_access_token(identity=str(user.id))
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/families", headers=headers)
    assert response.status_code == 200
    nomes = [f["name"] for f in response.json]
    assert family.name in nomes
    assert "Outra Familia" not in nomes

def test_delete_family_no_admin(client, user, db, family):
    from flask_jwt_extended import create_access_token
    token = create_access_token(identity=str(user.id))
    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete(f"/admin/families/{family.id}", headers=headers)
    assert response.status_code == 403

def test_edit_family_no_admin(client, user, db, family):
    from flask_jwt_extended import create_access_token
    token = create_access_token(identity=str(user.id))
    headers = {"Authorization": f"Bearer {token}"}
    response = client.put(f"/admin/families/{family.id}", json={"name": "Novo Nome"}, headers=headers)
    assert response.status_code == 403 