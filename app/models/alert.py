from app.config.extensions import db
from datetime import datetime

class Alert(db.Model):
    __tablename__ = "alerts"
    id = db.Column(db.Integer, primary_key=True)
    family_id = db.Column(db.Integer, db.ForeignKey("family.id"), nullable=False)
    asset_id = db.Column(db.Integer, db.ForeignKey("assets.id"), nullable=True)
    tipo = db.Column(db.String(50), nullable=False)
    mensagem = db.Column(db.String(255), nullable=False)
    severidade = db.Column(db.String(20), nullable=False, default="info")
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    family = db.relationship("Family", backref="alerts")
    asset = db.relationship("Asset", backref="alerts") 