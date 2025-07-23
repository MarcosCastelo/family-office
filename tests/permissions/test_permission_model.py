import pytest
from app.models.permission import Permission
from app.models.user import User
from app.config.extensions import db

class TestPermissionModel:
    """Testes para o modelo Permission"""
    
    def test_create_permission(self, db):
        """Teste de criação de permissão"""
        permission = Permission(
            name="test_permission",
            description="Test permission description"
        )
        db.session.add(permission)
        db.session.commit()
        
        assert permission.id is not None
        assert permission.name == "test_permission"
        assert permission.description == "Test permission description"
        assert permission.created_at is not None
    
    def test_permission_unique_name(self, db):
        """Teste de unicidade do nome da permissão"""
        # Criar primeira permissão
        permission1 = Permission(name="unique_permission")
        db.session.add(permission1)
        db.session.commit()
        
        # Tentar criar segunda permissão com mesmo nome
        permission2 = Permission(name="unique_permission")
        db.session.add(permission2)
        
        with pytest.raises(Exception):  # SQLAlchemy IntegrityError
            db.session.commit()
    
    def test_permission_user_relationship(self, db, user_fixture):
        """Teste de relacionamento entre permissão e usuário"""
        # Criar permissão
        permission = Permission(name="user_permission")
        db.session.add(permission)
        db.session.commit()
        
        # Adicionar permissão ao usuário
        user_fixture.permissions.append(permission)
        db.session.commit()
        
        # Verificar relacionamento
        assert permission in user_fixture.permissions
        assert user_fixture in permission.users
        assert len(user_fixture.permissions) == 1
        assert len(permission.users) == 1
    
    def test_permission_string_representation(self, db):
        """Teste da representação string da permissão"""
        permission = Permission(name="test_perm")
        assert str(permission) == "test_perm"
        assert repr(permission) == "<Permission test_perm>"
    
    def test_permission_without_description(self, db):
        """Teste de criação de permissão sem descrição"""
        permission = Permission(name="no_desc_permission")
        db.session.add(permission)
        db.session.commit()
        
        assert permission.description is None
        assert permission.name == "no_desc_permission" 