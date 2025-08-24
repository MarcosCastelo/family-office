from flask import Flask
from .config.config import Config
from .config.extensions import db, jwt, cors, migrate
from app.routes import auth, family, asset, permission, transaction, risk_analysis

def create_app():
    from app.models import User, Family, Permission, Transaction
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    migrate.init_app(app,db)
    
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(family.family_bp)
    app.register_blueprint(asset.asset_bp)
    app.register_blueprint(permission.permission_bp)
    app.register_blueprint(transaction.transaction_bp)
    app.register_blueprint(risk_analysis.risk_analysis_bp)
    from app.routes import dashboard_bp, admin_bp
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_bp)
    
    # Register reports blueprint
    from app.routes.reports import reports_bp
    app.register_blueprint(reports_bp)
    
    # Register health check blueprint
    from app.routes.health import health_bp
    app.register_blueprint(health_bp)
    
    return app