"""Assets Schema"""
from marshmallow import Schema, fields, validate, pre_load
from datetime import datetime
from app.constants.asset_types import ASSET_TYPE_CHOICES

class AssetSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    asset_type = fields.Str(required=True, validate=validate.OneOf(ASSET_TYPE_CHOICES))
    
    # Legacy value field - now calculated from transactions
    value = fields.Float(required=False, allow_none=True)
    
    # Dynamic calculated fields
    current_quantity = fields.Float(dump_only=True)
    current_value = fields.Float(dump_only=True)
    average_cost = fields.Float(dump_only=True)
    total_invested = fields.Float(dump_only=True)
    total_divested = fields.Float(dump_only=True)
    realized_gain_loss = fields.Float(dump_only=True)
    unrealized_gain_loss = fields.Float(dump_only=True)
    
    acquisition_date = fields.Date(required=False, allow_none=True)
    details = fields.Dict(required=False, allow_none=True)
    family_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    
    # Include transaction count for quick reference
    transaction_count = fields.Method("get_transaction_count", dump_only=True)
    
    def get_transaction_count(self, obj):
        """Get the number of transactions for this asset"""
        return len(obj.transactions) if hasattr(obj, 'transactions') and obj.transactions else 0
    
    @pre_load
    def convert_date_strings(self, data, **kwargs):
        """Convert date strings to date objects before validation"""
        if data and 'acquisition_date' in data and isinstance(data['acquisition_date'], str):
            try:
                data['acquisition_date'] = datetime.strptime(data['acquisition_date'], '%Y-%m-%d').date()
            except ValueError:
                # If date parsing fails, set to today's date
                from datetime import date
                data['acquisition_date'] = date.today()
        elif data and ('acquisition_date' not in data or not data['acquisition_date']):
            # If acquisition_date is missing or null, set to today's date
            from datetime import date
            data['acquisition_date'] = date.today()
        
        # Ensure details is a dict
        if data and ('details' not in data or not data['details']):
            data['details'] = {}
        
        return data