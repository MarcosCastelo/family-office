from flask import Blueprint, request, jsonify

from app.models.user import User
from app.config.extensions import db
from app.services.auth_service import authenticate
from app.schema.user_schema import UserSchema

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
    
    auth = authenticate(email, password)
    if not auth:
        return jsonify({"error": "Credenciais invalidas"}), 401
    return jsonify(auth), 200