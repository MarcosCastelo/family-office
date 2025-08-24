from app.config.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

user_family = db.Table('user_family',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('family_id', db.Integer, db.ForeignKey('family.id'))
)

user_permission = db.Table('user_permission',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'))
)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean, default=True)
    
    # Relationships - using strings to avoid circular imports
    families = db.relationship("Family", secondary="user_family", back_populates="users")
    permissions = db.relationship("Permission", secondary="user_permission", back_populates="users")
    suitability_profiles = db.relationship("SuitabilityProfile", back_populates="user", cascade="all, delete-orphan")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)