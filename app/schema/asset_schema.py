"""Assets Schema"""
from marshmallow import Schema, fields, validate, pre_load
from datetime import datetime
from app.constants.asset_types import ASSET_TYPE_CHOICES

class AssetSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    asset_type = fields.Str(required=True, validate=validate.OneOf(ASSET_TYPE_CHOICES))
    
    # Dynamic calculated fields
    current_quantity = fields.Float(dump_only=True)
    current_value = fields.Float(dump_only=True)
    average_cost = fields.Float(dump_only=True)
    total_invested = fields.Float(dump_only=True)
    total_divested = fields.Float(dump_only=True)
    realized_gain_loss = fields.Float(dump_only=True)
    unrealized_gain_loss = fields.Float(dump_only=True)
    
    # Asset-specific properties
    ticker = fields.Str(dump_only=True)
    indexador = fields.Str(dump_only=True)
    vencimento = fields.Method("get_vencimento", dump_only=True)
    coin_id = fields.Str(dump_only=True)
    currency = fields.Str(dump_only=True)
    asset_class = fields.Str(dump_only=True)
    
    acquisition_date = fields.Method("get_acquisition_date", required=False, allow_none=True)
    details = fields.Dict(required=False, allow_none=True)
    family_id = fields.Int(required=True)
    created_at = fields.Method("get_created_at", dump_only=True)
    
    # Include transaction count for quick reference
    transaction_count = fields.Method("get_transaction_count", dump_only=True)
    
    def get_transaction_count(self, obj):
        """Get the number of transactions for this asset"""
        return len(obj.transactions) if hasattr(obj, 'transactions') and obj.transactions else 0
    
    def get_vencimento(self, obj):
        """Get vencimento as a proper date object"""
        vencimento = obj.vencimento
        if vencimento:
            if isinstance(vencimento, str):
                try:
                    return datetime.strptime(vencimento, '%Y-%m-%d').date()
                except ValueError:
                    return None
            elif hasattr(vencimento, 'isoformat'):
                return vencimento
        return None
    
    def get_acquisition_date(self, obj):
        """Get acquisition_date as a proper date object"""
        acquisition_date = obj.acquisition_date
        if acquisition_date:
            if isinstance(acquisition_date, str):
                try:
                    return datetime.strptime(acquisition_date, '%Y-%m-%d').date()
                except ValueError:
                    return None
            elif hasattr(acquisition_date, 'isoformat'):
                return acquisition_date
        return None
    
    def get_created_at(self, obj):
        """Get created_at as a proper datetime object"""
        created_at = obj.created_at
        if created_at:
            if isinstance(created_at, str):
                try:
                    return datetime.fromisoformat(created_at)
                except ValueError:
                    return None
            elif hasattr(created_at, 'isoformat'):
                return created_at
        return None
    
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