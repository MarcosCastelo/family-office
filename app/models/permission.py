from app.config.extensions import db
from sqlalchemy.sql import func

class Permission(db.Model):
    __tablename__ = "permission"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=func.now())
    
    users = db.relationship("User", secondary="user_permission", back_populates="permissions")
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"<Permission {self.name}>"