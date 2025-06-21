from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.controllers.asset_controller import (
    list_assets_controller,
    get_asset_controller,
    create_asset_controller,
    update_asset_controller,
    delete_asset_controller,
)

asset_bp = Blueprint("asset", __name__, url_prefix="/assets")

@asset_bp.route("", methods=["GET"])
@jwt_required()
def list_assets():
    return list_assets_controller(request)

@asset_bp.route("/<int:asset_id>", methods=["GET"])
@jwt_required()
def get_asset(asset_id):
    return get_asset_controller(asset_id)

@asset_bp.route("", methods=["POST"])
@jwt_required()
def create_asset():
    return create_asset_controller(request)

@asset_bp.route("/<int:asset_id>", methods=["PUT"])
@jwt_required()
def update_asset(asset_id):
    return update_asset_controller(asset_id, request)

@asset_bp.route("/<int:asset_id>", methods=["DELETE"])
@jwt_required()
def delete_asset(asset_id):
    return delete_asset_controller(asset_id)