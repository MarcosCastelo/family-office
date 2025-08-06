from flask import jsonify, request
from app.models.family import Family
from app.models.user import User
from app.config.extensions import db
from app.schema.family_schema import FamilySchema
from app.schema.user_schema import UserSchema

family_schema = FamilySchema()
families_schema = FamilySchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

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

def admin_list_users_controller():
    users = User.query.all()
    return jsonify(users_schema.dump(users)), 200

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