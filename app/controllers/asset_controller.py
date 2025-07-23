from flask import jsonify, request, abort
from app.models.asset import Asset
from app.schema.asset_schema import AssetSchema
from app.config.extensions import db
from app.decorators.family_access import require_family

asset_schema = AssetSchema()
assets_schema = AssetSchema(many=True)

def list_assets_controller(req):
    family_id = req.args.get("family_id")
    if not family_id:
        return jsonify({"error": "family_id é obrigatório"}), 400
    
    try:
        family_id = int(family_id)
    except (ValueError, TypeError):
        return jsonify({"error": "family_id deve ser um número válido"}), 400
    
    # Verificar acesso à família
    from flask_jwt_extended import get_jwt_identity
    from app.models.user import User
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    if not user or not any(f.id == family_id for f in user.families):
        return jsonify({"error": "Acesso à familia negado"}), 403
    
    assets = Asset.query.filter_by(family_id=family_id).all()
    return jsonify(assets_schema.dump(assets)), 200

def get_asset_controller(asset_id):
    family_id = request.args.get("family_id")
    if not family_id:
        return jsonify({"error": "family_id é obrigatório"}), 400
    
    try:
        family_id = int(family_id)
    except (ValueError, TypeError):
        return jsonify({"error": "family_id deve ser um número válido"}), 400
    
    # Verificar acesso à família
    from flask_jwt_extended import get_jwt_identity
    from app.models.user import User
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    if not user or not any(f.id == family_id for f in user.families):
        return jsonify({"error": "Acesso à familia negado"}), 403
    
    asset = db.session.get(Asset, asset_id)
    if not asset:
        abort(404)
    # Verificar se o ativo pertence à família
    if asset.family_id != family_id:
        return jsonify({"error": "Acesso negado"}), 403
    
    return jsonify(asset_schema.dump(asset)), 200

def create_asset_controller(req):
    data = req.get_json()
    errors = asset_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    family_id = data.get("family_id")
    if not family_id:
        return jsonify({"error": "family_id é obrigatório"}), 400
    
    # Verificar acesso à família
    from flask_jwt_extended import get_jwt_identity
    from app.models.user import User
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    if not user or not any(f.id == int(family_id) for f in user.families):
        return jsonify({"error": "Acesso à familia negado"}), 403
    
    asset = Asset(**data)
    db.session.add(asset)
    db.session.commit()
    return jsonify(asset_schema.dump(asset)), 201

def update_asset_controller(asset_id, req):
    family_id = req.args.get("family_id")
    if not family_id:
        return jsonify({"error": "family_id é obrigatório"}), 400
    
    try:
        family_id = int(family_id)
    except (ValueError, TypeError):
        return jsonify({"error": "family_id deve ser um número válido"}), 400
    
    # Verificar acesso à família
    from flask_jwt_extended import get_jwt_identity
    from app.models.user import User
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    if not user or not any(f.id == family_id for f in user.families):
        return jsonify({"error": "Acesso à familia negado"}), 403
    
    asset = db.session.get(Asset, asset_id)
    if not asset:
        abort(404)
    # Verificar se o ativo pertence à família
    if asset.family_id != family_id:
        return jsonify({"error": "Acesso negado"}), 403
    
    data = req.get_json()
    errors = asset_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400
    for key, value in data.items():
        setattr(asset, key, value)
    db.session.commit()
    return jsonify(asset_schema.dump(asset)), 200

def delete_asset_controller(asset_id):
    family_id = request.args.get("family_id")
    if not family_id:
        return jsonify({"error": "family_id é obrigatório"}), 400
    
    try:
        family_id = int(family_id)
    except (ValueError, TypeError):
        return jsonify({"error": "family_id deve ser um número válido"}), 400
    
    # Verificar acesso à família
    from flask_jwt_extended import get_jwt_identity
    from app.models.user import User
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    if not user or not any(f.id == family_id for f in user.families):
        return jsonify({"error": "Acesso à familia negado"}), 403
    
    asset = db.session.get(Asset, asset_id)
    if not asset:
        abort(404)
    # Verificar se o ativo pertence à família
    if asset.family_id != family_id:
        return jsonify({"error": "Acesso negado"}), 403
    
    db.session.delete(asset)
    db.session.commit()
    return jsonify({"msg": "Ativo removido com sucesso"}), 204