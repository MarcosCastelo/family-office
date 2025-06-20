from flask_jwt_extended import get_jwt_identity
from functools import wraps
from flask import jsonify
from app.models.user import User

def require_permissions(permission_name):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user or permission_name not in [p.name for p in user.permissions]:
                return jsonify({"error": "Permissão negada"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator