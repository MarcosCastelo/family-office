"""Assets Schema"""
from marshmallow import Schema, fields, validate
from app.constants.asset_types import ASSET_TYPE_CHOICES

class AssetSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    asset_type = fields.Str(required=True, validate=validate.OneOf(ASSET_TYPE_CHOICES))
    value = fields.Float(required=True)
    acquisition_date = fields.Date()
    details = fields.Dict()
    family_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)