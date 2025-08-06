from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from functools import wraps
from flask import jsonify
from app.models.user import User
from app.config.extensions import db

def require_permissions(*permission_names):
    """
    Decorator para verificar se o usuário tem as permissões necessárias.
    Aceita uma ou múltiplas permissões.
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Verificar JWT primeiro
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = db.session.get(User, user_id)
            if not user:
                return jsonify({"error": "Usuário não encontrado"}), 401
            user_permissions = [p.name for p in user.permissions]
            # Verificar se o usuário tem pelo menos uma das permissões
            if not any(perm in user_permissions for perm in permission_names):
                return jsonify({
                    "error": f"Permissão negada. Necessário: {', '.join(permission_names)}"
                }), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator

require_permission = require_permissions

def require_all_permissions(*permission_names):
    """
    Decorator para verificar se o usuário tem TODAS as permissões necessárias.
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Verificar JWT primeiro
            verify_jwt_in_request()
            
            user_id = get_jwt_identity()
            user = db.session.get(User, user_id)
            
            if not user:
                return jsonify({"error": "Usuário não encontrado"}), 401
            
            user_permissions = [p.name for p in user.permissions]
            
            # Verificar se o usuário tem todas as permissões
            missing_permissions = [perm for perm in permission_names if perm not in user_permissions]
            if missing_permissions:
                return jsonify({
                    "error": f"Permissões insuficientes. Faltando: {', '.join(missing_permissions)}"
                }), 403
            
            return f(*args, **kwargs)
        return wrapper
    return decorator

def require_admin():
    """
    Decorator para verificar se o usuário tem permissões administrativas.
    """
    return require_permissions("admin_system", "admin_users", "admin_permissions")