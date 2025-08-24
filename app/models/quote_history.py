"""Model for storing asset quote history"""
from datetime import datetime
from app.config.extensions import db
from sqlalchemy.sql import func

class QuoteHistory(db.Model):
    __tablename__ = "quote_history"
    
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey("assets.id"), nullable=False)
    price = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default="USD", nullable=False)
    source = db.Column(db.String(50), nullable=False)  # yahoo_finance, coingecko, bacen
    timestamp = db.Column(db.DateTime, default=func.now(), nullable=False)
    
    # Relationships
    asset = db.relationship("Asset", back_populates="quote_history")
    
    def __repr__(self):
        return f"<QuoteHistory(asset_id={self.asset_id}, price={self.price}, source={self.source})>"
    
    @property
    def formatted_price(self):
        """Return formatted price with currency"""
        return f"{self.currency} {self.price:.4f}"
    
    @property
    def age_hours(self):
        """Return age of quote in hours"""
        if self.timestamp:
            delta = datetime.now() - self.timestamp
            return delta.total_seconds() / 3600
        return 0
    
    @property
    def is_fresh(self):
        """Check if quote is less than 1 hour old"""
        return self.age_hours < 1
