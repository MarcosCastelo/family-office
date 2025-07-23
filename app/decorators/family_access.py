from flask_jwt_extended import get_jwt_identity
from functools import wraps
from flask import jsonify, request
from app.models.user import User

def require_family(family_id_param="family_id"):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            family_id = kwargs.get(family_id_param) or request.view_args.get(family_id_param)
            
            # Verificar se family_id é válido
            if family_id is None:
                return jsonify({"error": "family_id é obrigatório"}), 400
            
            try:
                family_id = int(family_id)
            except (ValueError, TypeError):
                return jsonify({"error": "family_id deve ser um número válido"}), 400
            
            if not user or not any(f.id == family_id for f in user.families):
                return jsonify({"error": "Acesso à familia negado"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator

def check_family_access(family_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    try:
        family_id = int(family_id)
        return any(f.id == family_id for f in user.families)
    except (ValueError, TypeError):
        return False