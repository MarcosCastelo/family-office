import pytest
from marshmallow import ValidationError
from datetime import datetime
from app.schema.permission_schema import PermissionSchema, UserPermissionSchema, PermissionProfileSchema

class TestPermissionSchema:
    """Testes para o schema PermissionSchema"""
    
    def test_valid_permission_data(self):
        """Teste com dados válidos"""
        schema = PermissionSchema()
        data = {
            "name": "test_permission",
            "description": "Test permission description"
        }
        
        result = schema.load(data)
        assert result["name"] == "test_permission"
        assert result["description"] == "Test permission description"
    
    def test_permission_without_description(self):
        """Teste sem descrição"""
        schema = PermissionSchema()
        data = {"name": "test_permission"}
        
        result = schema.load(data)
        assert result["name"] == "test_permission"
        assert "description" not in result
    
    def test_permission_name_too_long(self):
        """Teste com nome muito longo"""
        schema = PermissionSchema()
        data = {
            "name": "a" * 51,  # Mais de 50 caracteres
            "description": "Test"
        }
        
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        
        assert "name" in exc_info.value.messages
    
    def test_permission_name_empty(self):
        """Teste com nome vazio"""
        schema = PermissionSchema()
        data = {"name": ""}
        
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        
        assert "name" in exc_info.value.messages
    
    def test_permission_dump(self):
        """Teste de serialização"""
        schema = PermissionSchema()
        data = {
            "id": 1,
            "name": "test_permission",
            "description": "Test description",
            "created_at": datetime(2023, 1, 1, 0, 0, 0)
        }
        
        result = schema.dump(data)
        assert result["id"] == 1
        assert result["name"] == "test_permission"
        assert result["description"] == "Test description"
        assert "created_at" in result

class TestUserPermissionSchema:
    """Testes para o schema UserPermissionSchema"""
    
    def test_valid_user_permission_data(self):
        """Teste com dados válidos"""
        schema = UserPermissionSchema()
        data = {
            "user_id": 1,
            "permission_ids": [1, 2, 3]
        }
        
        result = schema.load(data)
        assert result["user_id"] == 1
        assert result["permission_ids"] == [1, 2, 3]
    
    def test_user_permission_missing_user_id(self):
        """Teste sem user_id"""
        schema = UserPermissionSchema()
        data = {"permission_ids": [1, 2]}
        
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        
        assert "user_id" in exc_info.value.messages
    
    def test_user_permission_missing_permission_ids(self):
        """Teste sem permission_ids"""
        schema = UserPermissionSchema()
        data = {"user_id": 1}
        
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        
        assert "permission_ids" in exc_info.value.messages
    
    def test_user_permission_empty_permission_ids(self):
        """Teste com permission_ids vazio"""
        schema = UserPermissionSchema()
        data = {
            "user_id": 1,
            "permission_ids": []
        }
        
        result = schema.load(data)
        assert result["permission_ids"] == []

class TestPermissionProfileSchema:
    """Testes para o schema PermissionProfileSchema"""
    
    def test_valid_profile_data(self):
        """Teste com dados válidos"""
        schema = PermissionProfileSchema()
        data = {
            "profile_name": "admin",
            "user_id": 1
        }
        
        result = schema.load(data)
        assert result["profile_name"] == "admin"
        assert result["user_id"] == 1
    
    def test_valid_profile_names(self):
        """Teste com todos os nomes de perfil válidos"""
        schema = PermissionProfileSchema()
        valid_profiles = ["admin", "manager", "viewer", "user"]
        
        for profile in valid_profiles:
            data = {
                "profile_name": profile,
                "user_id": 1
            }
            result = schema.load(data)
            assert result["profile_name"] == profile
    
    def test_invalid_profile_name(self):
        """Teste com nome de perfil inválido"""
        schema = PermissionProfileSchema()
        data = {
            "profile_name": "invalid_profile",
            "user_id": 1
        }
        
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        
        assert "profile_name" in exc_info.value.messages
    
    def test_profile_missing_user_id(self):
        """Teste sem user_id"""
        schema = PermissionProfileSchema()
        data = {"profile_name": "admin"}
        
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        
        assert "user_id" in exc_info.value.messages
    
    def test_profile_missing_profile_name(self):
        """Teste sem profile_name"""
        schema = PermissionProfileSchema()
        data = {"user_id": 1}
        
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        
        assert "profile_name" in exc_info.value.messages 