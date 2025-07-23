import pytest
from app.constants.permissions import (
    PermissionType, 
    ALL_PERMISSIONS, 
    PERMISSION_PROFILES
)

class TestPermissionConstants:
    """Testes para as constantes de permissões"""
    
    def test_permission_type_constants(self):
        """Teste das constantes de tipos de permissão"""
        # Verificar se todas as constantes estão definidas
        assert hasattr(PermissionType, 'USER_VIEW')
        assert hasattr(PermissionType, 'USER_CREATE')
        assert hasattr(PermissionType, 'USER_UPDATE')
        assert hasattr(PermissionType, 'USER_DELETE')
        
        assert hasattr(PermissionType, 'FAMILY_VIEW')
        assert hasattr(PermissionType, 'FAMILY_CREATE')
        assert hasattr(PermissionType, 'FAMILY_UPDATE')
        assert hasattr(PermissionType, 'FAMILY_DELETE')
        assert hasattr(PermissionType, 'FAMILY_MANAGE_MEMBERS')
        
        assert hasattr(PermissionType, 'ASSET_VIEW')
        assert hasattr(PermissionType, 'ASSET_CREATE')
        assert hasattr(PermissionType, 'ASSET_UPDATE')
        assert hasattr(PermissionType, 'ASSET_DELETE')
        assert hasattr(PermissionType, 'ASSET_IMPORT')
        
        assert hasattr(PermissionType, 'REPORT_VIEW')
        assert hasattr(PermissionType, 'REPORT_GENERATE')
        assert hasattr(PermissionType, 'REPORT_EXPORT')
        
        assert hasattr(PermissionType, 'ADMIN_USERS')
        assert hasattr(PermissionType, 'ADMIN_PERMISSIONS')
        assert hasattr(PermissionType, 'ADMIN_SYSTEM')
    
    def test_all_permissions_list(self):
        """Teste da lista ALL_PERMISSIONS"""
        # Verificar se a lista não está vazia
        assert len(ALL_PERMISSIONS) > 0
        
        # Verificar se todas as permissões são strings
        for permission in ALL_PERMISSIONS:
            assert isinstance(permission, str)
            assert len(permission) > 0
        
        # Verificar se não há duplicatas
        assert len(ALL_PERMISSIONS) == len(set(ALL_PERMISSIONS))
        
        # Verificar se todas as constantes estão na lista
        permission_constants = [
            PermissionType.USER_VIEW,
            PermissionType.USER_CREATE,
            PermissionType.USER_UPDATE,
            PermissionType.USER_DELETE,
            PermissionType.FAMILY_VIEW,
            PermissionType.FAMILY_CREATE,
            PermissionType.FAMILY_UPDATE,
            PermissionType.FAMILY_DELETE,
            PermissionType.FAMILY_MANAGE_MEMBERS,
            PermissionType.ASSET_VIEW,
            PermissionType.ASSET_CREATE,
            PermissionType.ASSET_UPDATE,
            PermissionType.ASSET_DELETE,
            PermissionType.ASSET_IMPORT,
            PermissionType.REPORT_VIEW,
            PermissionType.REPORT_GENERATE,
            PermissionType.REPORT_EXPORT,
            PermissionType.ADMIN_USERS,
            PermissionType.ADMIN_PERMISSIONS,
            PermissionType.ADMIN_SYSTEM,
        ]
        
        for constant in permission_constants:
            assert constant in ALL_PERMISSIONS
    
    def test_permission_profiles_structure(self):
        """Teste da estrutura dos perfis de permissão"""
        # Verificar se os perfis existem
        expected_profiles = ["admin", "manager", "viewer", "user"]
        for profile in expected_profiles:
            assert profile in PERMISSION_PROFILES
        
        # Verificar se todos os perfis têm listas de permissões
        for profile_name, permissions in PERMISSION_PROFILES.items():
            assert isinstance(permissions, list)
            assert len(permissions) >= 0  # Pode ser vazio
        
        # Verificar se todas as permissões nos perfis existem em ALL_PERMISSIONS
        for profile_name, permissions in PERMISSION_PROFILES.items():
            for permission in permissions:
                assert permission in ALL_PERMISSIONS, f"Permission {permission} in profile {profile_name} not found in ALL_PERMISSIONS"
    
    def test_admin_profile_has_all_permissions(self):
        """Teste se o perfil admin tem todas as permissões"""
        admin_permissions = PERMISSION_PROFILES["admin"]
        
        # O perfil admin deve ter todas as permissões
        assert len(admin_permissions) == len(ALL_PERMISSIONS)
        
        # Verificar se todas as permissões estão no perfil admin
        for permission in ALL_PERMISSIONS:
            assert permission in admin_permissions
    
    def test_profile_hierarchy(self):
        """Teste da hierarquia dos perfis"""
        admin_permissions = set(PERMISSION_PROFILES["admin"])
        manager_permissions = set(PERMISSION_PROFILES["manager"])
        viewer_permissions = set(PERMISSION_PROFILES["viewer"])
        user_permissions = set(PERMISSION_PROFILES["user"])
        
        # Manager deve ter menos permissões que admin
        assert len(manager_permissions) <= len(admin_permissions)
        
        # Viewer deve ter menos permissões que manager
        assert len(viewer_permissions) <= len(manager_permissions)
        
        # Verificar se as permissões são subconjuntos apropriados
        # Manager deve ter um subconjunto das permissões de admin
        assert manager_permissions.issubset(admin_permissions)
        
        # Viewer deve ter um subconjunto das permissões de manager
        assert viewer_permissions.issubset(manager_permissions)
        
        # User deve ter um subconjunto das permissões de admin
        assert user_permissions.issubset(admin_permissions)
    
    def test_permission_names_format(self):
        """Teste do formato dos nomes das permissões"""
        for permission in ALL_PERMISSIONS:
            # Verificar se segue o padrão snake_case
            assert "_" in permission
            assert permission.islower()
            
            # Verificar se não tem espaços ou caracteres especiais
            assert " " not in permission
            assert permission.replace("_", "").isalnum()
    
    def test_profile_names_format(self):
        """Teste do formato dos nomes dos perfis"""
        for profile_name in PERMISSION_PROFILES.keys():
            # Verificar se são strings válidas
            assert isinstance(profile_name, str)
            assert len(profile_name) > 0
            assert profile_name.islower()
            assert profile_name.isalpha()
    
    def test_no_empty_permissions(self):
        """Teste para garantir que não há permissões vazias"""
        for permission in ALL_PERMISSIONS:
            assert permission.strip() != ""
            assert len(permission.strip()) > 0
    
    def test_no_empty_profiles(self):
        """Teste para garantir que não há perfis vazios"""
        for profile_name in PERMISSION_PROFILES.keys():
            assert profile_name.strip() != ""
            assert len(profile_name.strip()) > 0 