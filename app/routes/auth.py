from flask import Blueprint, request, jsonify
import re

from app.models.user import User
from app.config.extensions import db
from app.services.auth_service import authenticate
from app.schema.user_schema import UserSchema
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token, get_jwt

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
user_schema = UserSchema()

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
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
        db.session.add(user)
        db.session.commit()
        return jsonify(message="Usuario criado com sucesso"), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro ao criar usuário"}), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Dados são obrigatórios"}), 400
    
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"error": "Email e senha são obrigatórios"}), 400
    
    result = authenticate(email, password)
    if result:
        return jsonify(result), 200
    else:
        return jsonify({"error": "Credenciais inválidas"}), 401

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token), 200

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    """Retorna informações do usuário atual"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404
    
    return jsonify(user_schema.dump(user)), 200

@auth_bp.route("/password", methods=["PUT"])
@jwt_required()
def change_password():
    """Altera a senha do usuário atual"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Dados são obrigatórios"}), 400
    
    current_password = data.get("current_password")
    new_password = data.get("new_password")
    
    if not current_password or not new_password:
        return jsonify({"error": "Senha atual e nova senha são obrigatórias"}), 400
    
    # Validação de senha forte
    if len(new_password) < 6:
        return jsonify({"error": "Nova senha deve ter pelo menos 6 caracteres"}), 400
    
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404
    
    # Verificar senha atual
    if not user.check_password(current_password):
        return jsonify({"error": "Senha atual incorreta"}), 400
    
    try:
        user.set_password(new_password)
        db.session.commit()
        return jsonify({"message": "Senha alterada com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro ao alterar senha"}), 500