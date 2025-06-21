import pytest
from flask_jwt_extended import create_access_token

from app import create_app
from app.config.extensions import db as _db
from app.models.user import User

@pytest.fixture(scope="session")
def app():
    """Create test app and setup db schema"""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "testsecret"
    })
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()

@pytest.fixture()
def db(app):
    """Access to test database"""
    yield _db
    _db.session.remove()
    _db.drop_all()
    _db.create_all()

@pytest.fixture()
def client(app):
    """Return test client"""
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture()
def user(db):
    """Create new user for test"""
    user = User(email="test@example.com")
    user.set_password("123456")
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture()
def access_token(user):
    """Return access token for test user"""
    return create_access_token(identity=str(user.id))

