"""Risk Analysis Routes - Endpoints para análise de risco em tempo real"""
from flask import Blueprint, request, make_response
from flask_jwt_extended import jwt_required
from app.controllers.risk_analysis_controller import (
    get_portfolio_risk_analysis_controller,
    get_asset_risk_metrics_controller,
    update_asset_quotes_controller,
    get_market_overview_controller,
    get_risk_alerts_controller
)
from app.decorators.permissions import require_permission

risk_analysis_bp = Blueprint('risk_analysis', __name__, url_prefix='/risk')

def add_cors_headers(response):
    """Adiciona headers CORS para resolver problemas de preflight"""
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

@risk_analysis_bp.route('/portfolio/risk', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_portfolio_risk():
    """Obtém análise completa de risco da carteira"""
    if request.method == 'OPTIONS':
        response = make_response()
        return add_cors_headers(response)
    
    result = get_portfolio_risk_analysis_controller(request)
    
    # Se o controller retornar tuple (data, status), converter para Response
    if isinstance(result, tuple):
        data, status_code = result
        response = make_response(data, status_code)
    else:
        response = make_response(result)
    
    return add_cors_headers(response)

@risk_analysis_bp.route('/assets/<int:asset_id>/risk', methods=['GET'])
@jwt_required()
@require_permission('risk_view')
def get_asset_risk(asset_id):
    """Obtém métricas de risco para um ativo específico"""
    result = get_asset_risk_metrics_controller(asset_id, request)
    
    # Se o controller retornar tuple (data, status), converter para Response
    if isinstance(result, tuple):
        data, status_code = result
        response = make_response(data, status_code)
    else:
        response = make_response(result)
    
    return add_cors_headers(response)

@risk_analysis_bp.route('/quotes/update', methods=['POST'])
@jwt_required()
@require_permission('asset_update')
def update_quotes():
    """Atualiza cotações de todos os ativos de uma família"""
    result = update_asset_quotes_controller(request)
    
    # Se o controller retornar tuple (data, status), converter para Response
    if isinstance(result, tuple):
        data, status_code = result
        response = make_response(data, status_code)
    else:
        response = make_response(result)
    
    return add_cors_headers(response)

@risk_analysis_bp.route('/market/overview', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_market_overview():
    """Obtém visão geral do mercado para análise comparativa"""
    if request.method == 'OPTIONS':
        response = make_response()
        return add_cors_headers(response)
    
    result = get_market_overview_controller(request)
    
    # Se o controller retornar tuple (data, status), converter para Response
    if isinstance(result, tuple):
        data, status_code = result
        response = make_response(data, status_code)
    else:
        response = make_response(result)
    
    return add_cors_headers(response)

@risk_analysis_bp.route('/alerts', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_risk_alerts():
    """Obtém alertas de risco baseados em métricas em tempo real"""
    if request.method == 'OPTIONS':
        response = make_response()
        return add_cors_headers(response)
    
    result = get_risk_alerts_controller(request)
    
    # Se o controller retornar tuple (data, status), converter para Response
    if isinstance(result, tuple):
        data, status_code = result
        response = make_response(data, status_code)
    else:
        response = make_response(result)
    
    return add_cors_headers(response)

@risk_analysis_bp.route('/test', methods=['GET', 'OPTIONS'])
def test_risk_route():
    """Rota de teste para verificar se as rotas estão funcionando"""
    if request.method == 'OPTIONS':
        response = make_response()
        return add_cors_headers(response)
    
    response = make_response({"pong": "risk_analysis"}, 200)
    return add_cors_headers(response)

@risk_analysis_bp.route('/ping', methods=['GET', 'OPTIONS'])
def ping():
    """Rota simples para teste de conectividade"""
    if request.method == 'OPTIONS':
        response = make_response()
        return add_cors_headers(response)
    
    response = make_response({"pong": "risk_analysis"}, 200)
    return add_cors_headers(response)


