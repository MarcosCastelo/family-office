"""Model de ativo/passivos core do sistema"""
from datetime import datetime
from app.config.extensions import db
from sqlalchemy.sql import func
from sqlalchemy import desc
from app.services.cache_service import cached, invalidate_cache_pattern

class Asset(db.Model):
    __tablename__ = "assets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    asset_type = db.Column(db.String(50), nullable=False)
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
    quote_history = db.relationship(
        "QuoteHistory",
        back_populates="asset",
        cascade="all, delete-orphan",
        order_by="QuoteHistory.timestamp.desc()"
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
        
        # Try to get current market price from quote history
        if hasattr(self, 'quote_history') and self.quote_history:
            latest_quote = self.quote_history[0]  # Most recent quote
            current_price = latest_quote.price
            market_value = self.current_quantity * current_price
            return round(market_value - self.current_value, 2)
        
        return 0.0
    
    @property
    def realized_gain_loss(self):
        """Calculate realized gain/loss from completed sells"""
        if not self.transactions:
            return 0.0
        
        total_realized = 0.0
        for transaction in self.transactions:
            if transaction.transaction_type == "sell":
                # Calculate cost basis for this sell
                cost_basis = self._calculate_cost_basis_for_sell(transaction)
                realized_gain = transaction.total_value - cost_basis
                total_realized += realized_gain
        
        return round(total_realized, 2)
    
    def _calculate_cost_basis_for_sell(self, sell_transaction):
        """Calculate cost basis for a specific sell transaction"""
        if not self.transactions:
            return 0.0
        
        # Get buy transactions before this sell
        buy_transactions = [
            t for t in self.transactions 
            if t.transaction_type == "buy" and t.transaction_date <= sell_transaction.transaction_date
        ]
        
        # Sort by date (FIFO)
        buy_transactions.sort(key=lambda x: x.transaction_date)
        
        quantity_needed = sell_transaction.quantity
        cost_basis = 0.0
        
        for buy_transaction in buy_transactions:
            if quantity_needed <= 0:
                break
            
            quantity_from_buy = min(quantity_needed, buy_transaction.quantity)
            cost_basis += quantity_from_buy * buy_transaction.unit_price
            quantity_needed -= quantity_from_buy
        
        return cost_basis
    
    def get_latest_transaction(self):
        """Get the most recent transaction for this asset"""
        if not self.transactions:
            return None
        
        return max(self.transactions, key=lambda t: t.created_at)
    
    def get_transactions_by_type(self, transaction_type):
        """Get all transactions of a specific type (buy/sell)"""
        return [t for t in self.transactions if t.transaction_type == transaction_type]
    
    @property
    def ticker(self):
        """Get ticker for variable income assets"""
        if self.asset_type == "renda_variavel":
            return self.details.get('ticker') if self.details else None
        return None
    
    @property
    def indexador(self):
        """Get indexador for fixed income assets"""
        if self.asset_type == "renda_fixa":
            return self.details.get('indexador') if self.details else None
        return None
    
    @property
    def vencimento(self):
        """Get vencimento for fixed income assets"""
        if self.asset_type == "renda_fixa":
            return self.details.get('vencimento') if self.details else None
        return None
    
    @property
    def coin_id(self):
        """Get coin ID for cryptocurrency assets"""
        if self.asset_type == "criptomoeda":
            return self.details.get('coin_id') if self.details else None
        return None
    
    @property
    def currency(self):
        """Get currency for foreign exchange assets"""
        if self.asset_type == "moeda_estrangeira":
            return self.details.get('currency') if self.details else None
        return None
    
    @property
    def asset_class(self):
        """Get asset class for categorization"""
        asset_class_mapping = {
            "renda_fixa": "Fixed Income",
            "renda_variavel": "Variable Income", 
            "multimercado": "Multi-Market",
            "ativo_real": "Real Assets",
            "estrategico": "Strategic",
            "internacional": "International",
            "alternativo": "Alternative",
            "protecao": "Protection"
        }
        return asset_class_mapping.get(self.asset_type, "Unknown")
    
    def get_risk_metrics(self):
        """Get risk metrics for the asset"""
        if not hasattr(self, 'quote_history') or not self.quote_history:
            return {}
        
        # Calculate basic risk metrics
        quotes = [q.price for q in self.quote_history if q.price > 0]
        if len(quotes) < 2:
            return {}
        
        import statistics
        returns = []
        for i in range(1, len(quotes)):
            if quotes[i-1] > 0:
                returns.append((quotes[i] - quotes[i-1]) / quotes[i-1])
        
        if not returns:
            return {}
        
        volatility = statistics.stdev(returns) * (252 ** 0.5)  # Annualized
        
        return {
            'volatility': round(volatility * 100, 2),  # Percentage
            'price_change': round((quotes[-1] - quotes[0]) / quotes[0] * 100, 2),
            'latest_price': quotes[-1],
            'price_history_count': len(quotes)
        }
    
    def __repr__(self):
        """String representation of Asset"""
        return f"<Asset {self.name} ({self.current_quantity} units)>"