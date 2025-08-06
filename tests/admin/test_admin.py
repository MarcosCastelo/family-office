import pytest

def test_admin_list_families_success(client, admin_user_fixture, db):
    from flask_jwt_extended import create_access_token
    token = create_access_token(identity=str(admin_user_fixture.id))
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/admin/families", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_admin_list_families_no_access(client, user, db):
    from flask_jwt_extended import create_access_token
    token = create_access_token(identity=str(user.id))
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/admin/families", headers=headers)
    assert response.status_code == 403

def test_admin_create_family_success(client, admin_user_fixture, db):
    from flask_jwt_extended import create_access_token
    token = create_access_token(identity=str(admin_user_fixture.id))
    headers = {"Authorization": f"Bearer {token}"}
    data = {"name": "Nova Familia"}
    response = client.post("/admin/families", json=data, headers=headers)
    assert response.status_code == 201
    assert response.json["name"] == "Nova Familia"

def test_admin_create_family_no_access(client, user, db):
    from flask_jwt_extended import create_access_token
    token = create_access_token(identity=str(user.id))
    headers = {"Authorization": f"Bearer {token}"}
    data = {"name": "Nova Familia"}
    response = client.post("/admin/families", json=data, headers=headers)
    assert response.status_code == 403

def test_admin_list_users_success(client, admin_user_fixture, db):
    from flask_jwt_extended import create_access_token
    token = create_access_token(identity=str(admin_user_fixture.id))
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/admin/users", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_admin_list_users_no_access(client, user, db):
    from flask_jwt_extended import create_access_token
    token = create_access_token(identity=str(user.id))
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/admin/users", headers=headers)
    assert response.status_code == 403

def test_admin_add_user_to_family(client, admin_user_fixture, db):
    from app.models.user import User
    from app.models.family import Family
    from flask_jwt_extended import create_access_token
    user = User(email="novo@exemplo.com"); user.set_password("123"); db.session.add(user); db.session.commit()
    family = Family(name="Fam Teste"); db.session.add(family); db.session.commit()
    token = create_access_token(identity=str(admin_user_fixture.id))
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(f"/admin/families/{family.id}/add_user/{user.id}", headers=headers)
    assert response.status_code == 200
    assert "adicionado" in response.json["message"]

def test_admin_remove_user_from_family(client, admin_user_fixture, db):
    from app.models.user import User
    from app.models.family import Family
    from flask_jwt_extended import create_access_token
    user = User(email="novo2@exemplo.com"); user.set_password("123"); db.session.add(user); db.session.commit()
    family = Family(name="Fam Teste2"); db.session.add(family); db.session.commit()
    family.users.append(user); db.session.commit()
    token = create_access_token(identity=str(admin_user_fixture.id))
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(f"/admin/families/{family.id}/remove_user/{user.id}", headers=headers)
    assert response.status_code == 200
    assert "removido" in response.json["message"] 