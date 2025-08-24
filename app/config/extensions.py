from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate

db = SQLAlchemy()
jwt = JWTManager()
# Configuração CORS mais específica para resolver problemas de preflight
cors = CORS(
    resources={r"/*": {"origins": ["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"]}},
    supports_credentials=True,
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"]
)
migrate = Migrate()