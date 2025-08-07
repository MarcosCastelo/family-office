# Routes package 
from flask_jwt_extended import jwt_required
from flask import Blueprint, request
from app.decorators.permissions import require_permission

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    from app.controllers.dashboard_controller import dashboard_controller
    return dashboard_controller(request) 

admin_bp = Blueprint("admin", __name__)

# ===== FAMILY MANAGEMENT =====

@admin_bp.route("/admin/families", methods=["GET"])
@require_permission("admin")
def admin_list_families():
    from app.controllers.admin_controller import admin_list_families_controller
    return admin_list_families_controller()

@admin_bp.route("/admin/families", methods=["POST"])
@require_permission("admin")
def admin_create_family():
    from app.controllers.admin_controller import admin_create_family_controller
    return admin_create_family_controller(request)

@admin_bp.route("/admin/families/<int:family_id>", methods=["PUT"])
@require_permission("admin")
def admin_edit_family(family_id):
    from app.controllers.admin_controller import admin_edit_family_controller
    return admin_edit_family_controller(family_id, request)

@admin_bp.route("/admin/families/<int:family_id>", methods=["DELETE"])
@require_permission("admin")
def admin_delete_family(family_id):
    from app.controllers.admin_controller import admin_delete_family_controller
    return admin_delete_family_controller(family_id)

@admin_bp.route("/admin/families/<int:family_id>/add_user/<int:user_id>", methods=["POST"])
@require_permission("admin")
def admin_add_user_to_family(family_id, user_id):
    from app.controllers.admin_controller import admin_add_user_to_family_controller
    return admin_add_user_to_family_controller(family_id, user_id)

@admin_bp.route("/admin/families/<int:family_id>/remove_user/<int:user_id>", methods=["POST"])
@require_permission("admin")
def admin_remove_user_from_family(family_id, user_id):
    from app.controllers.admin_controller import admin_remove_user_from_family_controller
    return admin_remove_user_from_family_controller(family_id, user_id) 

# ===== USER MANAGEMENT =====

@admin_bp.route("/admin/users", methods=["GET"])
@require_permission("admin")
def admin_list_users():
    from app.controllers.admin_controller import admin_list_users_controller
    return admin_list_users_controller()

@admin_bp.route("/admin/users", methods=["POST"])
@require_permission("admin")
def admin_create_user():
    from app.controllers.admin_controller import admin_create_user_controller
    return admin_create_user_controller(request)

@admin_bp.route("/admin/users/<int:user_id>", methods=["GET"])
@require_permission("admin")
def admin_get_user_details(user_id):
    from app.controllers.admin_controller import admin_get_user_details_controller
    return admin_get_user_details_controller(user_id)

@admin_bp.route("/admin/users/<int:user_id>", methods=["PUT"])
@require_permission("admin")
def admin_edit_user(user_id):
    from app.controllers.admin_controller import admin_edit_user_controller
    return admin_edit_user_controller(user_id, request)

@admin_bp.route("/admin/users/<int:user_id>", methods=["DELETE"])
@require_permission("admin")
def admin_delete_user(user_id):
    from app.controllers.admin_controller import admin_delete_user_controller
    return admin_delete_user_controller(user_id)

# ===== PERMISSION MANAGEMENT =====

@admin_bp.route("/admin/permissions", methods=["GET"])
@require_permission("admin")
def admin_list_permissions():
    from app.controllers.admin_controller import admin_list_permissions_controller
    return admin_list_permissions_controller()

@admin_bp.route("/admin/permissions", methods=["POST"])
@require_permission("admin")
def admin_create_permission():
    from app.controllers.admin_controller import admin_create_permission_controller
    return admin_create_permission_controller(request)

@admin_bp.route("/admin/permissions/<int:permission_id>", methods=["PUT"])
@require_permission("admin")
def admin_edit_permission(permission_id):
    from app.controllers.admin_controller import admin_edit_permission_controller
    return admin_edit_permission_controller(permission_id, request)

@admin_bp.route("/admin/permissions/<int:permission_id>", methods=["DELETE"])
@require_permission("admin")
def admin_delete_permission(permission_id):
    from app.controllers.admin_controller import admin_delete_permission_controller
    return admin_delete_permission_controller(permission_id)

# ===== USER PERMISSIONS MANAGEMENT =====

@admin_bp.route("/admin/users/<int:user_id>/permissions/<int:permission_id>", methods=["POST"])
@require_permission("admin")
def admin_add_permission_to_user(user_id, permission_id):
    from app.controllers.admin_controller import admin_add_permission_to_user_controller
    return admin_add_permission_to_user_controller(user_id, permission_id)

@admin_bp.route("/admin/users/<int:user_id>/permissions/<int:permission_id>", methods=["DELETE"])
@require_permission("admin")
def admin_remove_permission_from_user(user_id, permission_id):
    from app.controllers.admin_controller import admin_remove_permission_from_user_controller
    return admin_remove_permission_from_user_controller(user_id, permission_id)

# ===== ADMIN DASHBOARD =====

@admin_bp.route("/admin/dashboard", methods=["GET"])
@require_permission("admin")
def admin_dashboard():
    from app.controllers.admin_controller import admin_dashboard_controller
    return admin_dashboard_controller()

 