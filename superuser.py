# Script para criar usuário admin (execute no Python do backend)
from app import create_app
from app.models import User, Permission
from app.config.extensions import db

app = create_app()
with app.app_context():
    # Verificar se usuário admin já existe
    admin_user = User.query.filter_by(email="admin@admin.com").first()
    if not admin_user:
        # Criar usuário admin
        admin_user = User(email="admin@admin.com")
        admin_user.set_password("admin123")
        db.session.add(admin_user)
        print("Usuário admin criado!")
    else:
        print("Usuário admin já existe!")
    
    # Verificar se permissão admin já existe
    admin_permission = Permission.query.filter_by(name="admin").first()
    if not admin_permission:
        # Criar permissão admin
        admin_permission = Permission(name="admin", description="Administrador do sistema")
        db.session.add(admin_permission)
        print("Permissão admin criada!")
    else:
        print("Permissão admin já existe!")
    
    # Associar permissão ao usuário se não estiver associada
    if admin_permission not in admin_user.permissions:
        admin_user.permissions.append(admin_permission)
        print("Permissão admin associada ao usuário!")
    else:
        print("Usuário já possui permissão admin!")
    
    db.session.commit()
    print("Processo concluído!")