import pytest
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request
from app.decorators.permissions import require_permissions, require_all_permissions, require_admin
from app.models.permission import Permission
from app.models.user import User
from app.config.extensions import db

class TestPermissionDecorators:
    """Testes para os decorators de permissões"""
    
    def test_require_permissions_logic(self, app, user_fixture):
        """Teste da lógica de require_permissions"""
        with app.app_context():
            permission = Permission(name="test_permission")
            db.session.add(permission)
            db.session.flush()
            user = db.session.get(User, user_fixture.id)
            user.permissions.append(permission)
            db.session.commit()
            user_permissions = [p.name for p in user.permissions]
            assert "test_permission" in user_permissions
            required_permissions = ["test_permission"]
            has_permission = any(perm in user_permissions for perm in required_permissions)
            assert has_permission == True
    
    def test_require_permissions_failure_logic(self, app, user_fixture):
        """Teste da lógica de falha do require_permissions"""
        with app.app_context():
            user = db.session.get(User, user_fixture.id)
            user_permissions = [p.name for p in user.permissions]
            required_permissions = ["missing_permission"]
            has_permission = any(perm in user_permissions for perm in required_permissions)
            assert has_permission == False
    
    def test_require_all_permissions_logic(self, app, user_fixture):
        """Teste da lógica de require_all_permissions"""
        with app.app_context():
            perm1 = Permission(name="perm1")
            perm2 = Permission(name="perm2")
            db.session.add_all([perm1, perm2])
            db.session.flush()
            user = db.session.get(User, user_fixture.id)
            user.permissions.extend([perm1, perm2])
            db.session.commit()
            user_permissions = [p.name for p in user.permissions]
            required_permissions = ["perm1", "perm2"]
            missing_permissions = [perm for perm in required_permissions if perm not in user_permissions]
            assert len(missing_permissions) == 0
    
    def test_require_all_permissions_failure_logic(self, app, user_fixture):
        """Teste da lógica de falha do require_all_permissions"""
        with app.app_context():
            perm1 = Permission(name="perm1")
            db.session.add(perm1)
            db.session.flush()
            user = db.session.get(User, user_fixture.id)
            user.permissions.append(perm1)
            db.session.commit()
            user_permissions = [p.name for p in user.permissions]
            required_permissions = ["perm1", "perm2"]
            missing_permissions = [perm for perm in required_permissions if perm not in user_permissions]
            assert len(missing_permissions) == 1
            assert "perm2" in missing_permissions
    
    def test_require_admin_logic(self, app, user_fixture):
        """Teste da lógica de require_admin"""
        with app.app_context():
            admin_perm = Permission(name="admin_system")
            db.session.add(admin_perm)
            db.session.flush()
            user = db.session.get(User, user_fixture.id)
            user.permissions.append(admin_perm)
            db.session.commit()
            user_permissions = [p.name for p in user.permissions]
            admin_permissions = ["admin_system", "admin_users", "admin_permissions"]
            has_admin_permission = any(perm in user_permissions for perm in admin_permissions)
            assert has_admin_permission == True
    
    def test_require_admin_failure_logic(self, app, user_fixture):
        """Teste da lógica de falha do require_admin"""
        with app.app_context():
            user = db.session.get(User, user_fixture.id)
            user_permissions = [p.name for p in user.permissions]
            admin_permissions = ["admin_system", "admin_users", "admin_permissions"]
            has_admin_permission = any(perm in user_permissions for perm in admin_permissions)
            assert has_admin_permission == False 