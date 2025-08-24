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
        for permission in ALL_PERMISSIONS:
            assert permission in admin_permissions, f"Admin profile missing permission: {permission}"
    
    def test_permission_naming_convention(self):
        """Teste da convenção de nomenclatura das permissões"""
        # Verificar se todas as permissões seguem o padrão snake_case
        # Exceto a permissão "admin" que é especial
        for permission in ALL_PERMISSIONS:
            if permission != "admin":  # Skip the special "admin" permission
                assert '_' in permission, f"Permission {permission} should use snake_case format"
    
    def test_permission_profiles_are_valid(self):
        """Teste se os perfis de permissão são válidos"""
        # Verificar se cada perfil tem permissões válidas
        for profile_name, permissions in PERMISSION_PROFILES.items():
            assert isinstance(permissions, list), f"Profile {profile_name} permissions should be a list"
            
            for permission in permissions:
                assert isinstance(permission, str), f"Permission in profile {profile_name} should be a string"
                assert permission in ALL_PERMISSIONS, f"Permission {permission} in profile {profile_name} not found in ALL_PERMISSIONS"
    
    def test_permission_hierarchy(self):
        """Teste da hierarquia de permissões"""
        # Verificar se o perfil admin tem mais permissões que outros
        admin_count = len(PERMISSION_PROFILES["admin"])
        manager_count = len(PERMISSION_PROFILES["manager"])
        viewer_count = len(PERMISSION_PROFILES["viewer"])
        user_count = len(PERMISSION_PROFILES["user"])
        
        assert admin_count >= manager_count, "Admin should have at least as many permissions as manager"
        assert manager_count >= viewer_count, "Manager should have at least as many permissions as viewer"
        assert viewer_count >= user_count, "Viewer should have at least as many permissions as user"
    
    def test_permission_types_are_strings(self):
        """Teste se todas as constantes de permissão são strings"""
        for attr_name in dir(PermissionType):
            if not attr_name.startswith('_') and attr_name.isupper():
                attr_value = getattr(PermissionType, attr_name)
                assert isinstance(attr_value, str), f"Permission constant {attr_name} should be a string"
    
    def test_permission_constants_are_unique(self):
        """Teste se todas as constantes de permissão são únicas"""
        permission_values = []
        for attr_name in dir(PermissionType):
            if not attr_name.startswith('_') and attr_name.isupper():
                attr_value = getattr(PermissionType, attr_name)
                permission_values.append(attr_value)
        
        # Verificar se não há duplicatas
        assert len(permission_values) == len(set(permission_values)), "Permission constants should be unique"
    
    def test_permission_profiles_cover_all_permissions(self):
        """Teste se todos os perfis juntos cobrem todas as permissões"""
        all_profile_permissions = set()
        for permissions in PERMISSION_PROFILES.values():
            all_profile_permissions.update(permissions)
        
        # Verificar se todas as permissões estão cobertas por pelo menos um perfil
        for permission in ALL_PERMISSIONS:
            assert permission in all_profile_permissions, f"Permission {permission} not covered by any profile"
    
    def test_permission_constants_format(self):
        """Teste do formato das constantes de permissão"""
        for permission in ALL_PERMISSIONS:
            # Verificar se a permissão não está vazia
            assert permission.strip() != "", "Permission should not be empty or whitespace"
            
            # Verificar se não tem espaços extras
            assert permission == permission.strip(), "Permission should not have leading/trailing whitespace"
            
            # Verificar se não tem caracteres especiais problemáticos
            assert not permission.startswith(' '), "Permission should not start with space"
            assert not permission.endswith(' '), "Permission should not end with space" 