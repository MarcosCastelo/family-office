import pytest
from flask_jwt_extended import create_access_token
from datetime import date

from app import create_app
from app.config.extensions import db as _db
from app.models.user import User
from app.models.family import Family
from app.models.permission import Permission
from app.constants.permissions import ALL_PERMISSIONS

@pytest.fixture(scope="session")
def app():
    """Create test app and setup db schema"""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "testsecret"
    })
    return app

@pytest.fixture()
def db(app):
    """Access to test database"""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()

@pytest.fixture()
def client(db, app):
    """Return test client, ensuring db is ready before client."""
    return app.test_client()

@pytest.fixture()
def user(db):
    """Create new user for test"""
    user = User(email="test@example.com")
    user.set_password("123456")
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture()
def user_fixture(db):
    """Create new user for test with password"""
    user = User(email="test@example.com")
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture()
def admin_user_fixture(db):
    """Create admin user with all permissions, including 'admin'"""
    user = User(email="admin@example.com")
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()
    # Criar todas as permissões e atribuir ao admin
    from app.models.permission import Permission
    from app.constants.permissions import ALL_PERMISSIONS
    for permission_name in ALL_PERMISSIONS:
        permission = Permission(name=permission_name)
        db.session.add(permission)
    # Garante permissão 'admin' explícita
    if not Permission.query.filter_by(name="admin").first():
        db.session.add(Permission(name="admin"))
    db.session.commit()
    # Atribuir todas as permissões ao usuário admin
    all_permissions = Permission.query.all()
    user.permissions.extend(all_permissions)
    db.session.commit()
    return user

@pytest.fixture()
def permission_fixture(db):
    """Create a test permission"""
    permission = Permission(name="test_permission", description="Test permission")
    db.session.add(permission)
    db.session.commit()
    return permission

@pytest.fixture
def family(db):
    fam = Family(name="Família Teste")
    db.session.add(fam)
    db.session.commit()
    return fam

@pytest.fixture()
def access_token(user):
    """Return access token for test user"""
    return create_access_token(identity=str(user.id))

@pytest.fixture()
def headers(user, family, db):
    user.families.append(family)
    db.session.commit()
    access_token = create_access_token(identity=str(user.id))
    return {
        "Authorization": f"Bearer {access_token}"
    }

@pytest.fixture()
def asset_payload(family):
    """Payload padrão para testes de ativos"""
    return {
        "name": "Tesouro IPCA",
        "asset_type": "renda_fixa",
        "value": 15000.0,
        "acquisition_date": "2024-01-01",  # String para JSON
        "details": {
            "indexador": "IPCA",
            "vencimento": "2030-01-01",
            "taxa": 6.5
        },
        "family_id": family.id
    }

