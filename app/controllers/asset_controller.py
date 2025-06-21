from flask import jsonify
from app.models.asset import Asset
from app.schema.asset_schema import AssetSchema
from app.config.extensions import db
from app.decorators.family_access import require_family

asset_schema = AssetSchema()
assets_schema = AssetSchema(many=True)

@require_family(lambda req: int(req.args.get("family_id", 0)))
def list_assets_controller(req):
    family_id = int(req.args.get("family_id"))
    assets = Asset.query.filter_by(family_id=family_id).all()
    return jsonify(assets_schema.dump(assets)), 200


@require_family(lambda req: int(req.args.get("family_id", 0)))
def get_asset_controller(asset_id):
    asset = Asset.query.get_or_404(asset_id)
    return jsonify(asset_schema.dump(asset)), 200


@require_family(lambda req: int(req.args.get("family_id", 0)))
def create_asset_controller(req):
    data = req.get_json()
    errors = asset_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    asset = Asset(**data)
    db.session.add(asset)
    db.session.commit()
    return jsonify(asset_schema.dump(asset)), 201


@require_family(lambda req: int(req.args.get("family_id", 0)))
def update_asset_controller(asset_id, req):
    asset = Asset.query.get_or_404(asset_id)
    data = req.get_json()
    errors = asset_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400
    for key, value in data.items():
        setattr(asset, key, value)
    db.session.commit()
    return jsonify(asset_schema.dump(asset)), 200

@require_family(lambda req: int(req.args.get("family_id", 0)))
def delete_asset_controller(asset_id):
    asset = Asset.query.get_or_404(asset_id)
    db.session.delete(asset)
    db.session.commit()
    return jsonify({"msg": "Ativo removido com sucesso"}), 204