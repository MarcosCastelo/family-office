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
            if not user or not any(f.id == int(family_id) for f in user.families):
                return jsonify({"error": "Acesso à familia negado"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator