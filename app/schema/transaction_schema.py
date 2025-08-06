"""Transaction Schema for validation and serialization"""
from marshmallow import Schema, fields, ValidationError, post_load, validate
from datetime import date

from app.models.transaction import Transaction


class TransactionSchema(Schema):
    """Schema for Transaction model validation and serialization"""
    
    id = fields.Int(dump_only=True)
    asset_id = fields.Int(required=True, validate=validate.Range(min=1))
    transaction_type = fields.Str(required=True, validate=validate.OneOf(["buy", "sell"]))
    quantity = fields.Float(required=True, validate=validate.Range(min=0, min_inclusive=False))
    unit_price = fields.Float(required=True, validate=validate.Range(min=0, min_inclusive=False))
    total_value = fields.Float(dump_only=True)
    transaction_date = fields.Date(load_default=date.today)
    description = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    # Removed @post_load to allow tests to work with dict data
    # Controllers will create Transaction objects manually


class TransactionSummarySchema(Schema):
    """Schema for transaction summary/aggregation data"""
    
    total_transactions = fields.Int()
    total_buy_transactions = fields.Int()
    total_sell_transactions = fields.Int()
    total_invested = fields.Float()
    total_divested = fields.Float()
    net_investment = fields.Float()
    current_quantity = fields.Float()
    average_cost = fields.Float()
    latest_transaction_date = fields.Date(allow_none=True)