from flask import jsonify, request
from app.models.permission import Permission
from app.models.user import User
from app.schema.permission_schema import PermissionSchema, UserPermissionSchema, PermissionProfileSchema
from app.config.extensions import db
from app.constants.permissions import ALL_PERMISSIONS, PERMISSION_PROFILES

permission_schema = PermissionSchema()
permissions_schema = PermissionSchema(many=True)
user_permission_schema = UserPermissionSchema()
permission_profile_schema = PermissionProfileSchema()

def list_permissions_controller():
    """Listar todas as permissões"""
    permissions = Permission.query.all()
    return jsonify(permissions_schema.dump(permissions)), 200

def get_permission_controller(permission_id):
    """Obter uma permissão específica"""
    permission = db.session.get(Permission, permission_id)
    if not permission:
        return jsonify({"error": "Permissão não encontrada"}), 404
    
    return jsonify(permission_schema.dump(permission)), 200

def create_permission_controller(req):
    """Criar uma nova permissão"""
    data = req.get_json()
    errors = permission_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    # Verificar se a permissão já existe
    existing = Permission.query.filter_by(name=data["name"]).first()
    if existing:
        return jsonify({"error": "Permissão já existe"}), 400
    
    permission = Permission(**data)
    db.session.add(permission)
    db.session.commit()
    
    return jsonify(permission_schema.dump(permission)), 201

def update_permission_controller(permission_id, req):
    """Atualizar uma permissão"""
    permission = db.session.get(Permission, permission_id)
    if not permission:
        return jsonify({"error": "Permissão não encontrada"}), 404
    
    data = req.get_json()
    errors = permission_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400
    
    # Verificar se o nome já existe em outra permissão
    if "name" in data and data["name"] != permission.name:
        existing = Permission.query.filter_by(name=data["name"]).first()
        if existing:
            return jsonify({"error": "Nome de permissão já existe"}), 400
    
    for key, value in data.items():
        setattr(permission, key, value)
    
    db.session.commit()
    return jsonify(permission_schema.dump(permission)), 200

def delete_permission_controller(permission_id):
    """Deletar uma permissão"""
    permission = db.session.get(Permission, permission_id)
    if not permission:
        return jsonify({"error": "Permissão não encontrada"}), 404
    
    db.session.delete(permission)
    db.session.commit()
    
    return jsonify({"message": "Permissão removida com sucesso"}), 204

def get_user_permissions_controller(user_id):
    """Obter permissões de um usuário"""
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404
    
    permissions = user.permissions
    return jsonify(permissions_schema.dump(permissions)), 200

def assign_permissions_controller(req):
    """Atribuir permissões a um usuário"""
    data = req.get_json()
    errors = user_permission_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    user = db.session.get(User, data["user_id"])
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404
    
    # Limpar permissões existentes
    user.permissions.clear()
    
    # Adicionar novas permissões
    permissions = Permission.query.filter(Permission.id.in_(data["permission_ids"])).all()
    user.permissions.extend(permissions)
    
    db.session.commit()
    
    return jsonify({
        "message": f"Permissões atribuídas com sucesso ao usuário {user.email}",
        "permissions": permissions_schema.dump(permissions)
    }), 200

def assign_profile_controller(req):
    """Atribuir um perfil de permissões a um usuário"""
    data = req.get_json()
    errors = permission_profile_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    user = db.session.get(User, data["user_id"])
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404
    
    profile_name = data["profile_name"]
    if profile_name not in PERMISSION_PROFILES:
        return jsonify({"error": "Perfil inválido"}), 400
    
    # Limpar permissões existentes
    user.permissions.clear()
    
    # Adicionar permissões do perfil
    profile_permissions = PERMISSION_PROFILES[profile_name]
    permissions = Permission.query.filter(Permission.name.in_(profile_permissions)).all()
    user.permissions.extend(permissions)
    
    db.session.commit()
    
    return jsonify({
        "message": f"Perfil '{profile_name}' atribuído com sucesso ao usuário {user.email}",
        "permissions": permissions_schema.dump(permissions)
    }), 200

def list_available_permissions_controller():
    """Listar todas as permissões disponíveis no sistema"""
    return jsonify({
        "permissions": ALL_PERMISSIONS,
        "profiles": list(PERMISSION_PROFILES.keys())
    }), 200

def initialize_permissions_controller():
    """Inicializar permissões do sistema (criar se não existirem)"""
    created_count = 0
    
    for permission_name in ALL_PERMISSIONS:
        existing = Permission.query.filter_by(name=permission_name).first()
        if not existing:
            permission = Permission(name=permission_name)
            db.session.add(permission)
            created_count += 1
    
    db.session.commit()
    
    return jsonify({
        "message": f"{created_count} permissões criadas com sucesso",
        "total_permissions": len(ALL_PERMISSIONS)
    }), 200 