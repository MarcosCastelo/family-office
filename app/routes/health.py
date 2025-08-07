from flask import Blueprint, jsonify
from app.config.extensions import db

health_bp = Blueprint('health', __name__)

@health_bp.route('/health')
def health_check():
    """Health check endpoint for Railway and Docker"""
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        db_status = 'healthy'
    except Exception as e:
        db_status = f'unhealthy: {str(e)}'
    
    return jsonify({
        'status': 'healthy',
        'database': db_status,
        'timestamp': db.func.now()
    }), 200 