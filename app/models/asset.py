"""Model de ativo/passivos core do sistema"""
from datetime import datetime
from app.config.extensions import db
from sqlalchemy.sql import func
from sqlalchemy import desc

class Asset(db.Model):
    __tablename__ = "assets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    asset_type = db.Column(db.String(50), nullable=False)
    # value field deprecated - now calculated from transactions
    value = db.Column(db.Float, nullable=False)  # Keep for backward compatibility
    acquisition_date = db.Column(db.Date)
    details = db.Column(db.JSON, nullable=True)
    family_id = db.Column(db.Integer, db.ForeignKey("family.id"), nullable=False)
    
    created_at = db.Column(db.DateTime, default=func.now())
    
    # Relationships
    family = db.relationship("Family", back_populates="assets")
    transactions = db.relationship(
        "Transaction", 
        back_populates="asset",
        cascade="all, delete-orphan",
        order_by="Transaction.transaction_date.desc()"
    )
    
    @property
    def current_quantity(self):
        """Calculate current quantity based on buy/sell transactions"""
        if not self.transactions:
            return 0.0
        
        total_quantity = 0.0
        for transaction in self.transactions:
            if transaction.transaction_type == "buy":
                total_quantity += transaction.quantity
            elif transaction.transaction_type == "sell":
                total_quantity -= transaction.quantity
        
        return round(total_quantity, 6)
    
    @property
    def current_value(self):
        """Calculate current value based on current quantity and average cost"""
        return round(self.current_quantity * self.average_cost, 2)
    
    @property
    def average_cost(self):
        """Calculate weighted average cost of current holdings"""
        if not self.transactions:
            return 0.0
        
        total_cost = 0.0
        total_quantity = 0.0
        
        # Calculate FIFO average cost
        remaining_quantity = self.current_quantity
        if remaining_quantity <= 0:
            return 0.0
        
        # Process transactions in chronological order
        buy_transactions = [
            t for t in sorted(self.transactions, key=lambda x: x.transaction_date) 
            if t.transaction_type == "buy"
        ]
        
        quantity_needed = remaining_quantity
        for transaction in buy_transactions:
            if quantity_needed <= 0:
                break
            
            quantity_from_this_transaction = min(quantity_needed, transaction.quantity)
            total_cost += quantity_from_this_transaction * transaction.unit_price
            total_quantity += quantity_from_this_transaction
            quantity_needed -= quantity_from_this_transaction
        
        if total_quantity == 0:
            return 0.0
        
        return round(total_cost / total_quantity, 2)
    
    @property
    def total_invested(self):
        """Calculate total amount invested (buy transactions)"""
        if not self.transactions:
            return 0.0
        
        total = 0.0
        for transaction in self.transactions:
            if transaction.transaction_type == "buy":
                total += transaction.total_value
        
        return round(total, 2)
    
    @property
    def total_divested(self):
        """Calculate total amount received from sells"""
        if not self.transactions:
            return 0.0
        
        total = 0.0
        for transaction in self.transactions:
            if transaction.transaction_type == "sell":
                total += transaction.total_value
        
        return round(total, 2)
    
    @property
    def unrealized_gain_loss(self):
        """Calculate unrealized gain/loss for current holdings"""
        if self.current_quantity <= 0:
            return 0.0
        
        # This would require current market price - for now return 0
        # In a real system, you'd integrate with market data API
        return 0.0
    
    @property
    def realized_gain_loss(self):
        """Calculate realized gain/loss from completed sells"""
        if not self.transactions:
            return 0.0
        
        # This is a simplified calculation - in reality you'd need to track
        # cost basis of specific lots sold
        return self.total_divested - self.total_invested
    
    def get_latest_transaction(self):
        """Get the most recent transaction for this asset"""
        if not self.transactions:
            return None
        
        return max(self.transactions, key=lambda t: t.created_at)
    
    def get_transactions_by_type(self, transaction_type):
        """Get all transactions of a specific type (buy/sell)"""
        return [t for t in self.transactions if t.transaction_type == transaction_type]
    
    def __repr__(self):
        """String representation of Asset"""
        return f"<Asset {self.name} ({self.current_quantity} units)>"