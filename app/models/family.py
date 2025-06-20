from app.config.extensions import db

class Family(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    users = db.relationship("User", secondary="user_family", back_populates="families")