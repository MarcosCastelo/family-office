from app.config.extensions import db

class Family(db.Model):
    __tablename__ = "family"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cash_balance = db.Column(db.Float, default=0.0, nullable=False)  # Saldo disponível para investimentos
    
    # Relationships
    users = db.relationship("User", secondary="user_family", back_populates="families")
    assets = db.relationship("Asset", back_populates="family", cascade="all, delete-orphan")
    suitability_profiles = db.relationship("SuitabilityProfile", back_populates="family", cascade="all, delete-orphan")
    
    @property
    def total_invested(self):
        """Calculate total amount invested across all assets"""
        if not self.assets:
            return 0.0
        
        total = 0.0
        for asset in self.assets:
            total += asset.current_value
        
        return round(total, 2)
    
    @property
    def total_patrimony(self):
        """Calculate total patrimony (invested + cash balance)"""
        return round(self.total_invested + self.cash_balance, 2)
    
    @property
    def asset_allocation(self):
        """Calculate asset allocation by type"""
        if not self.assets:
            return {}
        
        allocation = {}
        for asset in self.assets:
            asset_type = asset.asset_type
            if asset_type not in allocation:
                allocation[asset_type] = 0.0
            allocation[asset_type] += asset.current_value
        
        return allocation