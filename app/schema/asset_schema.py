"""Assets Schema"""
from marshmallow import Schema, fields, validate, pre_load
from datetime import datetime
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
    
    @pre_load
    def convert_date_strings(self, data, **kwargs):
        """Convert date strings to date objects before validation"""
        if data and 'acquisition_date' in data and isinstance(data['acquisition_date'], str):
            try:
                data['acquisition_date'] = datetime.strptime(data['acquisition_date'], '%Y-%m-%d').date()
            except ValueError:
                pass  # Let the field validation handle invalid dates
        return data