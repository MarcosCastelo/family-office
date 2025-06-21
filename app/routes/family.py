"""Rotas de Family"""
from flask import Blueprint, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.family import Family
from app.models.user import User
from app.config.extensions import db
from app.schema.family_schema import FamilySchema

family_bp = Blueprint("family", __name__, url_prefix="/family")
family_schema = FamilySchema()

@family_bp.route("/join/<int:family_id>", methods=["POST"])
@jwt_required()
def join_family(family_id):
    """Rota de associar um user a uma familia"""
    user = db.session.get(User, int(get_jwt_identity()))
    family = db.session.get(Family, family_id)
    if not family:
        abort(404)
    if family not in user.families:
        user.families.append(family)
        db.session.commit()
    return jsonify({"message": f"Usuário associado a família {family.name}"}), 200
