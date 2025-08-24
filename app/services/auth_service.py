from app.models.user import User
from app.config.extensions import db
from flask_jwt_extended import create_access_token,  create_refresh_token

def authenticate(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        # Obter permissões do usuário
        user_permissions = [perm.name for perm in user.permissions] if user.permissions else []
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": user.id,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name if hasattr(user, 'name') else None,
                "permissions": user_permissions
            }
        }
    return None