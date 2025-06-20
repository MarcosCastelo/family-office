from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.family import Family
from app.models.user import User
from app.config.extensions import db

family_bp = Blueprint("family", __name__, url_prefix="/family")

@family_bp.route("/join/<int:family_id>", methods=["POST"])
@jwt_required
def join_family(family_id):
    user = User.query.get(get_jwt_identity())
    family = Family.query.get_or_404(family_id)
    if family not in user.families:
        user.families.append(family)
        db.session.commit()
    return jsonify({"message": f"Usuário associado a família {family.name}"}), 200