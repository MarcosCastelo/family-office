"""Permission Schema"""
from marshmallow import Schema, fields, validate

class PermissionSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    description = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)

class UserPermissionSchema(Schema):
    user_id = fields.Int(required=True)
    permission_ids = fields.List(fields.Int(), required=True)

class PermissionProfileSchema(Schema):
    profile_name = fields.Str(required=True, validate=validate.OneOf(["admin", "manager", "viewer", "user"]))
    user_id = fields.Int(required=True)