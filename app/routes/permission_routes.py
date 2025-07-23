from flask import Blueprint, request
from app.controllers.permission_controller import (
    list_permissions_controller,
    get_permission_controller,
    create_permission_controller,
    update_permission_controller,
    delete_permission_controller,
    get_user_permissions_controller,
    assign_permissions_controller,
    assign_profile_controller,
    list_available_permissions_controller,
    initialize_permissions_controller
)

permission_bp = Blueprint("permission", __name__)

# Rotas para gerenciar permissões
@permission_bp.route("/permissions", methods=["GET"])
def list_permissions():
    return list_permissions_controller()

@permission_bp.route("/permissions/<int:permission_id>", methods=["GET"])
def get_permission(permission_id):
    return get_permission_controller(permission_id)

@permission_bp.route("/permissions", methods=["POST"])
def create_permission():
    return create_permission_controller(request)

@permission_bp.route("/permissions/<int:permission_id>", methods=["PUT"])
def update_permission(permission_id):
    return update_permission_controller(permission_id, request)

@permission_bp.route("/permissions/<int:permission_id>", methods=["DELETE"])
def delete_permission(permission_id):
    return delete_permission_controller(permission_id)

# Rotas para gerenciar permissões de usuários
@permission_bp.route("/users/<int:user_id>/permissions", methods=["GET"])
def get_user_permissions(user_id):
    return get_user_permissions_controller(user_id)

@permission_bp.route("/users/permissions", methods=["POST"])
def assign_permissions():
    return assign_permissions_controller(request)

@permission_bp.route("/users/profile", methods=["POST"])
def assign_profile():
    return assign_profile_controller(request)

# Rotas utilitárias
@permission_bp.route("/permissions/available", methods=["GET"])
def list_available_permissions():
    return list_available_permissions_controller()

@permission_bp.route("/permissions/initialize", methods=["POST"])
def initialize_permissions():
    return initialize_permissions_controller() 