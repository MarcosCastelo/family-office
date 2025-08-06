"""Transaction model for tracking asset buy/sell operations"""
from datetime import datetime, date
from app.config.extensions import db
from sqlalchemy.sql import func
from sqlalchemy.orm import validates


class Transaction(db.Model):
    """Model representing a financial transaction (buy/sell) for an asset"""
    
    __tablename__ = "transactions"
    
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey("assets.id"), nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False)  # 'buy' or 'sell'
    quantity = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    total_value = db.Column(db.Float, nullable=False)
    transaction_date = db.Column(db.Date, nullable=False, default=date.today)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
    
    # Relationship
    asset = db.relationship("Asset", back_populates="transactions")
    
    def __init__(self, **kwargs):
        """Initialize transaction with basic validation"""
        # Validate before setting attributes
        if 'quantity' in kwargs and kwargs['quantity'] <= 0:
            raise ValueError("Quantity must be positive")
        
        if 'unit_price' in kwargs and kwargs['unit_price'] <= 0:
            raise ValueError("Unit price must be positive")
        
        if 'transaction_type' in kwargs and kwargs['transaction_type'] not in ['buy', 'sell']:
            raise ValueError("Transaction type must be 'buy' or 'sell'")
        
        super().__init__(**kwargs)
        
        # Calculate total value
        if hasattr(self, 'quantity') and hasattr(self, 'unit_price'):
            self.total_value = round(self.quantity * self.unit_price, 2)
    
    @staticmethod
    def validate_sell_quantity(asset_id, quantity):
        """Validate that sell quantity doesn't exceed current holdings"""
        from app.models.asset import Asset
        from app.config.extensions import db
        
        asset = db.session.get(Asset, asset_id)
        if asset and asset.current_quantity < quantity:
            raise ValueError("Cannot sell more than current quantity")
    
    @validates('transaction_type')
    def validate_transaction_type(self, key, value):
        """Validate transaction type is 'buy' or 'sell'"""
        if value not in ['buy', 'sell']:
            raise ValueError("Transaction type must be 'buy' or 'sell'")
        return value
    
    @validates('quantity')
    def validate_quantity(self, key, value):
        """Validate quantity is positive"""
        if value <= 0:
            raise ValueError("Quantity must be positive")
        return value
    
    @validates('unit_price')
    def validate_unit_price(self, key, value):
        """Validate unit price is positive"""
        if value <= 0:
            raise ValueError("Unit price must be positive")
        return value
    
    def __repr__(self):
        """String representation of Transaction"""
        return f"<Transaction {self.transaction_type} {self.quantity} @ {self.unit_price}>"
    
    def __str__(self):
        """Human readable string representation"""
        return f"{self.transaction_type.title()} {self.quantity} units at ${self.unit_price}"