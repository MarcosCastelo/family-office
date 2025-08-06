"""Transaction routes for CRUD operations"""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.controllers.transaction_controller import (
    create_transaction_controller,
    list_transactions_controller,
    get_transaction_controller,
    update_transaction_controller,
    delete_transaction_controller,
    get_asset_transaction_summary_controller
)

transaction_bp = Blueprint("transaction", __name__, url_prefix="/transactions")


@transaction_bp.route("", methods=["POST"])
@jwt_required()
def create_transaction():
    """Create a new transaction"""
    return create_transaction_controller(request)


@transaction_bp.route("", methods=["GET"])
@jwt_required()
def list_transactions():
    """List transactions with optional filtering"""
    return list_transactions_controller(request)


@transaction_bp.route("/<int:transaction_id>", methods=["GET"])
@jwt_required()
def get_transaction(transaction_id):
    """Get a specific transaction by ID"""
    return get_transaction_controller(transaction_id)


@transaction_bp.route("/<int:transaction_id>", methods=["PUT"])
@jwt_required()
def update_transaction(transaction_id):
    """Update a transaction"""
    return update_transaction_controller(transaction_id, request)


@transaction_bp.route("/<int:transaction_id>", methods=["DELETE"])
@jwt_required()
def delete_transaction(transaction_id):
    """Delete a transaction"""
    return delete_transaction_controller(transaction_id)


@transaction_bp.route("/asset/<int:asset_id>/summary", methods=["GET"])
@jwt_required()
def get_asset_transaction_summary(asset_id):
    """Get transaction summary for a specific asset"""
    return get_asset_transaction_summary_controller(asset_id)