# Script para criar usuário admin (execute no Python do backend)
from app import create_app
from app.models import User, Permission
from app.config.extensions import db

app = create_app()
with app.app_context():
    # Criar usuário admin
    admin_user = User(email="admin@admin.com")
    admin_user.set_password("admin123")
    db.session.add(admin_user)
    
    # Criar permissão admin
    admin_permission = Permission(name="admin", description="Administrador do sistema")
    db.session.add(admin_permission)
    
    # Associar permissão ao usuário
    admin_user.permissions.append(admin_permission)
    
    db.session.commit()
    print("Usuário admin criado!")