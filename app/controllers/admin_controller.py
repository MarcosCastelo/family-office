from flask import jsonify, request
from app.models.family import Family
from app.models.user import User
from app.models.permission import Permission
from app.config.extensions import db
from app.schema.family_schema import FamilySchema
from app.schema.user_schema import UserSchema
from app.schema.permission_schema import PermissionSchema
from werkzeug.security import generate_password_hash
import re

family_schema = FamilySchema()
families_schema = FamilySchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)
permission_schema = PermissionSchema()
permissions_schema = PermissionSchema(many=True)

# ===== FAMILY MANAGEMENT =====

def admin_list_families_controller():
    families = Family.query.all()
    return jsonify(families_schema.dump(families)), 200

def admin_create_family_controller(req):
    data = req.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Nome da família é obrigatório"}), 400
    # Validação de nome único
    if Family.query.filter_by(name=data["name"]).first():
        return jsonify({"error": "Nome de família já existe"}), 400
    family = Family(name=data["name"])
    db.session.add(family)
    db.session.commit()
    return jsonify(family_schema.dump(family)), 201

def admin_edit_family_controller(family_id, req):
    family = db.session.get(Family, family_id)
    if not family:
        return jsonify({"error": "Família não encontrada"}), 404
    data = req.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Nome da família é obrigatório"}), 400
    # Validação de nome único (exceto a própria)
    if Family.query.filter(Family.name == data["name"], Family.id != family_id).first():
        return jsonify({"error": "Nome de família já existe"}), 400
    family.name = data["name"]
    db.session.commit()
    return jsonify(family_schema.dump(family)), 200

def admin_delete_family_controller(family_id):
    family = db.session.get(Family, family_id)
    if not family:
        return jsonify({"error": "Família não encontrada"}), 404
    db.session.delete(family)
    db.session.commit()
    return jsonify({"message": f"Família {family.name} excluída"}), 200

def admin_add_user_to_family_controller(family_id, user_id):
    family = db.session.get(Family, family_id)
    user = db.session.get(User, user_id)
    if not family or not user:
        return jsonify({"error": "Família ou usuário não encontrado"}), 404
    if user not in family.users:
        family.users.append(user)
        db.session.commit()
    return jsonify({"message": f"Usuário {user.email} adicionado à família {family.name}"}), 200

def admin_remove_user_from_family_controller(family_id, user_id):
    family = db.session.get(Family, family_id)
    user = db.session.get(User, user_id)
    if not family or not user:
        return jsonify({"error": "Família ou usuário não encontrado"}), 404
    if user in family.users:
        family.users.remove(user)
        db.session.commit()
    return jsonify({"message": f"Usuário {user.email} removido da família {family.name}"}), 200

# ===== USER MANAGEMENT =====

def admin_list_users_controller():
    users = User.query.all()
    return jsonify(users_schema.dump(users)), 200

def admin_create_user_controller(req):
    data = req.get_json()
    if not data:
        return jsonify({"error": "Dados são obrigatórios"}), 400
    
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"error": "Email e senha são obrigatórios"}), 400
    
    if not email.strip() or not password.strip():
        return jsonify({"error": "Email e senha não podem estar vazios"}), 400
    
    # Validação de e-mail
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_regex, email):
        return jsonify({"error": "Email inválido"}), 400
    
    # Validação de senha forte
    if len(password) < 6:
        return jsonify({"error": "Senha deve ter pelo menos 6 caracteres"}), 400
    
    # Verificar se usuário já existe
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Usuário já existe"}), 400
    
    try:
        user = User(email=email)
        user.set_password(password)
        user.active = data.get("active", True)
        
        db.session.add(user)
        db.session.commit()
        return jsonify(user_schema.dump(user)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro ao criar usuário"}), 500

def admin_edit_user_controller(user_id, req):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404
    
    data = req.get_json()
    if not data:
        return jsonify({"error": "Dados são obrigatórios"}), 400
    
    try:
        # Atualizar email se fornecido
        if "email" in data:
            email = data["email"]
            if not email.strip():
                return jsonify({"error": "Email não pode estar vazio"}), 400
            
            # Validação de e-mail
            email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            if not re.match(email_regex, email):
                return jsonify({"error": "Email inválido"}), 400
            
            # Verificar se email já existe (exceto o próprio usuário)
            existing_user = User.query.filter(User.email == email, User.id != user_id).first()
            if existing_user:
                return jsonify({"error": "Email já está em uso"}), 400
            
            user.email = email
        
        # Atualizar senha se fornecida
        if "password" in data and data["password"]:
            password = data["password"]
            if len(password) < 6:
                return jsonify({"error": "Senha deve ter pelo menos 6 caracteres"}), 400
            user.set_password(password)
        
        # Atualizar status ativo
        if "active" in data:
            user.active = bool(data["active"])
        
        db.session.commit()
        return jsonify(user_schema.dump(user)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro ao atualizar usuário"}), 500

def admin_delete_user_controller(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404
    
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"Usuário {user.email} excluído"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro ao excluir usuário"}), 500

def admin_get_user_details_controller(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404
    
    # Incluir informações de famílias e permissões
    user_data = user_schema.dump(user)
    user_data["families"] = [{"id": f.id, "name": f.name} for f in user.families]
    user_data["permissions"] = [{"id": p.id, "name": p.name} for p in user.permissions]
    
    return jsonify(user_data), 200

# ===== PERMISSION MANAGEMENT =====

def admin_list_permissions_controller():
    permissions = Permission.query.all()
    return jsonify(permissions_schema.dump(permissions)), 200

def admin_create_permission_controller(req):
    data = req.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Nome da permissão é obrigatório"}), 400
    
    # Verificar se permissão já existe
    existing_permission = Permission.query.filter_by(name=data["name"]).first()
    if existing_permission:
        return jsonify({"error": "Permissão já existe"}), 400
    
    try:
        permission = Permission(
            name=data["name"],
            description=data.get("description", "")
        )
        db.session.add(permission)
        db.session.commit()
        return jsonify(permission_schema.dump(permission)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro ao criar permissão"}), 500

def admin_edit_permission_controller(permission_id, req):
    permission = db.session.get(Permission, permission_id)
    if not permission:
        return jsonify({"error": "Permissão não encontrada"}), 404
    
    data = req.get_json()
    if not data:
        return jsonify({"error": "Dados são obrigatórios"}), 400
    
    try:
        if "name" in data:
            # Verificar se nome já existe (exceto a própria permissão)
            existing_permission = Permission.query.filter(
                Permission.name == data["name"], 
                Permission.id != permission_id
            ).first()
            if existing_permission:
                return jsonify({"error": "Nome de permissão já existe"}), 400
            permission.name = data["name"]
        
        if "description" in data:
            permission.description = data["description"]
        
        db.session.commit()
        return jsonify(permission_schema.dump(permission)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro ao atualizar permissão"}), 500

def admin_delete_permission_controller(permission_id):
    permission = db.session.get(Permission, permission_id)
    if not permission:
        return jsonify({"error": "Permissão não encontrada"}), 404
    
    try:
        db.session.delete(permission)
        db.session.commit()
        return jsonify({"message": f"Permissão {permission.name} excluída"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro ao excluir permissão"}), 500

# ===== USER PERMISSIONS MANAGEMENT =====

def admin_add_permission_to_user_controller(user_id, permission_id):
    user = db.session.get(User, user_id)
    permission = db.session.get(Permission, permission_id)
    
    if not user or not permission:
        return jsonify({"error": "Usuário ou permissão não encontrado"}), 404
    
    if permission not in user.permissions:
        user.permissions.append(permission)
        db.session.commit()
        return jsonify({"message": f"Permissão {permission.name} adicionada ao usuário {user.email}"}), 200
    else:
        return jsonify({"message": f"Usuário {user.email} já possui a permissão {permission.name}"}), 200

def admin_remove_permission_from_user_controller(user_id, permission_id):
    user = db.session.get(User, user_id)
    permission = db.session.get(Permission, permission_id)
    
    if not user or not permission:
        return jsonify({"error": "Usuário ou permissão não encontrado"}), 404
    
    if permission in user.permissions:
        user.permissions.remove(permission)
        db.session.commit()
        return jsonify({"message": f"Permissão {permission.name} removida do usuário {user.email}"}), 200
    else:
        return jsonify({"message": f"Usuário {user.email} não possui a permissão {permission.name}"}), 200

# ===== ADMIN DASHBOARD =====

def admin_dashboard_controller():
    """Retorna métricas administrativas"""
    try:
        total_users = User.query.count()
        active_users = User.query.filter_by(active=True).count()
        total_families = Family.query.count()
        total_permissions = Permission.query.count()
        
        # Usuários por família
        families_with_users = []
        families = Family.query.all()
        for family in families:
            families_with_users.append({
                "id": family.id,
                "name": family.name,
                "user_count": len(family.users)
            })
        
        # Permissões mais comuns
        permission_stats = []
        permissions = Permission.query.all()
        for permission in permissions:
            user_count = len(permission.users)
            permission_stats.append({
                "id": permission.id,
                "name": permission.name,
                "user_count": user_count
            })
        
        return jsonify({
            "metrics": {
                "total_users": total_users,
                "active_users": active_users,
                "total_families": total_families,
                "total_permissions": total_permissions
            },
            "families": families_with_users,
            "permissions": permission_stats
        }), 200
    except Exception as e:
        return jsonify({"error": "Erro ao carregar dashboard administrativo"}), 500 