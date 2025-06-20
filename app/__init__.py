from flask import Flask
from .config.config import Config
from .config.extensions import db, jwt, cors, migrate
from app.routes import auth, family

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    print(">>> DATABASE URI:", app.config["SQLALCHEMY_DATABASE_URI"])
    
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    migrate.init_app(app,db)
    
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(family.family_bp)
    
    return app