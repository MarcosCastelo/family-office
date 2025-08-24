"""Constantes de permissões do sistema"""

class PermissionType:
    # Permissões de usuário
    USER_VIEW = "user_view"
    USER_CREATE = "user_create"
    USER_UPDATE = "user_update"
    USER_DELETE = "user_delete"
    
    # Permissões de família
    FAMILY_VIEW = "family_view"
    FAMILY_CREATE = "family_create"
    FAMILY_UPDATE = "family_update"
    FAMILY_DELETE = "family_delete"
    FAMILY_MANAGE_MEMBERS = "family_manage_members"
    
    # Permissões de ativos
    ASSET_VIEW = "asset_view"
    ASSET_CREATE = "asset_create"
    ASSET_UPDATE = "asset_update"
    ASSET_DELETE = "asset_delete"
    ASSET_IMPORT = "asset_import"
    
    # Permissões de relatórios
    REPORT_VIEW = "report_view"
    REPORT_GENERATE = "report_generate"
    REPORT_EXPORT = "report_export"
    
    # Permissões de análise de risco
    RISK_VIEW = "risk_view"
    RISK_ANALYSIS = "risk_analysis"
    RISK_UPDATE = "risk_update"
    
    # Permissões administrativas
    ADMIN = "admin"
    ADMIN_USERS = "admin_users"
    ADMIN_PERMISSIONS = "admin_permissions"
    ADMIN_SYSTEM = "admin_system"

# Lista de todas as permissões
ALL_PERMISSIONS = [
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
    PermissionType.RISK_VIEW,
    PermissionType.RISK_ANALYSIS,
    PermissionType.RISK_UPDATE,
    PermissionType.ADMIN,
    PermissionType.ADMIN_USERS,
    PermissionType.ADMIN_PERMISSIONS,
    PermissionType.ADMIN_SYSTEM,
]

# Perfis de permissões predefinidos
PERMISSION_PROFILES = {
    "admin": ALL_PERMISSIONS,
    "manager": [
        PermissionType.USER_VIEW,
        PermissionType.FAMILY_VIEW,
        PermissionType.FAMILY_UPDATE,
        PermissionType.FAMILY_MANAGE_MEMBERS,
        PermissionType.ASSET_VIEW,
        PermissionType.ASSET_CREATE,
        PermissionType.ASSET_UPDATE,
        PermissionType.ASSET_DELETE,
        PermissionType.ASSET_IMPORT,
        PermissionType.REPORT_VIEW,
        PermissionType.REPORT_GENERATE,
        PermissionType.REPORT_EXPORT,
    ],
    "viewer": [
        PermissionType.FAMILY_VIEW,
        PermissionType.ASSET_VIEW,
        PermissionType.ASSET_CREATE,
        PermissionType.ASSET_UPDATE,
        PermissionType.ASSET_DELETE,
        PermissionType.REPORT_VIEW,
        PermissionType.RISK_VIEW,
    ],
    "user": [
        PermissionType.ASSET_VIEW,
        PermissionType.ASSET_CREATE,
        PermissionType.ASSET_UPDATE,
        PermissionType.ASSET_DELETE,
        PermissionType.RISK_VIEW,
    ]
} 