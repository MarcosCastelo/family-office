"""User Serializer"""
from marshmallow import Schema, fields, post_load
from app.models.user import User
from .family_schema import FamilySchema
from .permission_schema import PermissionSchema

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    active = fields.Boolean()
    
    families = fields.List(fields.Nested(lambda: FamilySchema(only=("id", "name"))))
    permissions = fields.List(fields.Nested(lambda: PermissionSchema(only=("id", "name"))))
    
    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)