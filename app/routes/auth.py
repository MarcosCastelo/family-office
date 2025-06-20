from flask import Blueprint, request, jsonify

from app.models.user import User
from app.config.extensions import db
from app.services.auth_service import authenticate

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    user = User(email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify(message="Usuário criado com sucesso"), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    auth = authenticate(data["email"], data["password"])
    if not auth:
        return jsonify({"error": "Credenciais inválidas"}), 401
    return jsonify(auth), 200