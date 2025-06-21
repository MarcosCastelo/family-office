"""Model de ativo/passivos core do sistema"""
from datetime import datetime
from app.config.extensions import db
from sqlalchemy.sql import func

class Asset(db.Model):
    __tablename__ = "assets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    asset_type = db.Column(db.String(50), nullable=False)
    value = db.Column(db.Float, nullable=False)
    acquisition_date = db.Column(db.Date)
    details = db.Column(db.JSON, nullable=True)
    family_id = db.Column(db.Integer, db.ForeignKey("family.id"), nullable=False)
    
    created_at = db.Column(db.DateTime, default=func.now())
    
    family = db.relationship("Family", back_populates="assets")