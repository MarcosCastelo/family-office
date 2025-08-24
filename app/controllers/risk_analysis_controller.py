"""Risk Analysis Controller - Análise de risco em tempo real"""
from flask import jsonify, request
from app.services.market_data_service import MarketDataService
from app.models.asset import Asset
from app.config.extensions import db
from app.decorators.family_access import require_family
from flask_jwt_extended import get_jwt_identity
from app.models.user import User
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

market_data_service = MarketDataService()

def get_portfolio_risk_analysis_controller(req):
    """Obtém análise completa de risco da carteira"""
    try:
        family_id = req.args.get("family_id")
        if not family_id:
            return jsonify({"error": "family_id é obrigatório"}), 400
        
        try:
            family_id = int(family_id)
        except (ValueError, TypeError):
            return jsonify({"error": "family_id deve ser um número válido"}), 400
        
        # Verificar acesso à família
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        if not user or not any(f.id == family_id for f in user.families):
            return jsonify({"error": "Acesso à familia negado"}), 403
        
        # Obter análise de risco
        risk_analysis = market_data_service.get_portfolio_risk_analysis(family_id)
        
        if not risk_analysis:
            return jsonify({"error": "Não foi possível analisar o risco da carteira"}), 500
        
        return jsonify(risk_analysis), 200
        
    except Exception as e:
        logger.error(f"Erro na análise de risco: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

def get_asset_risk_metrics_controller(asset_id, req):
    """Obtém métricas de risco para um ativo específico"""
    try:
        family_id = req.args.get("family_id")
        if not family_id:
            return jsonify({"error": "family_id é obrigatório"}), 400
        
        try:
            family_id = int(family_id)
        except (ValueError, TypeError):
            return jsonify({"error": "family_id deve ser um número válido"}), 400
        
        # Verificar acesso à família
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        if not user or not any(f.id == family_id for f in user.families):
            return jsonify({"error": "Acesso à familia negado"}), 403
        
        # Buscar ativo
        asset = db.session.get(Asset, asset_id)
        if not asset:
            return jsonify({"error": "Ativo não encontrado"}), 404
        
        # Verificar se o ativo pertence à família
        if asset.family_id != family_id:
            return jsonify({"error": "Acesso negado"}), 403
        
        # Obter métricas de risco
        risk_metrics = market_data_service.get_asset_risk_metrics(asset)
        
        if not risk_metrics:
            return jsonify({"error": "Não foi possível calcular as métricas de risco"}), 500
        
        return jsonify({
            'asset_id': asset.id,
            'asset_name': asset.name,
            'asset_type': asset.asset_type,
            'risk_metrics': risk_metrics
        }), 200
        
    except Exception as e:
        logger.error(f"Erro nas métricas de risco: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

def update_asset_quotes_controller(req):
    """Atualiza cotações de todos os ativos de uma família"""
    try:
        family_id = req.args.get("family_id")
        if not family_id:
            return jsonify({"error": "family_id é obrigatório"}), 400
        
        try:
            family_id = int(family_id)
        except (ValueError, TypeError):
            return jsonify({"error": "family_id deve ser um número válido"}), 400
        
        # Verificar acesso à família
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        if not user or not any(f.id == family_id for f in user.families):
            return jsonify({"error": "Acesso à familia negado"}), 403
        
        # Atualizar cotações
        update_result = market_data_service.update_all_asset_quotes(family_id)
        
        if 'error' in update_result:
            return jsonify({"error": update_result['error']}), 500
        
        return jsonify({
            'message': 'Cotações atualizadas com sucesso',
            'result': update_result
        }), 200
        
    except Exception as e:
        logger.error(f"Erro na atualização de cotações: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

def get_market_overview_controller(req):
    """Obtém visão geral do mercado para análise comparativa"""
    try:
        family_id = req.args.get("family_id")
        if not family_id:
            return jsonify({"error": "family_id é obrigatório"}), 400
        
        try:
            family_id = int(family_id)
        except (ValueError, TypeError):
            return jsonify({"error": "family_id deve ser um número válido"}), 400
        
        # Verificar acesso à família
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        if not user or not any(f.id == family_id for f in user.families):
            return jsonify({"error": "Acesso à familia negado"}), 403
        
        # Buscar ativos da família
        assets = Asset.query.filter_by(family_id=family_id).all()
        
        if not assets:
            return jsonify({"error": "Nenhum ativo encontrado"}), 404
        
        # Obter dados de mercado para análise comparativa
        market_overview = {
            'total_assets': len(assets),
            'asset_types': {},
            'market_performance': {},
            'risk_distribution': {
                'low_risk': 0,
                'moderate_risk': 0,
                'high_risk': 0,
                'very_high_risk': 0
            },
            'liquidity_analysis': {
                'high_liquidity': 0,
                'medium_liquidity': 0,
                'low_liquidity': 0
            },
            'concentration_analysis': {
                'well_diversified': 0,
                'moderately_concentrated': 0,
                'highly_concentrated': 0
            }
        }
        
        # Analisar cada ativo
        total_value = 0
        for asset in assets:
            total_value += asset.current_value or 0
            
            # Contar por tipo
            asset_type = asset.asset_type
            if asset_type not in market_overview['asset_types']:
                market_overview['asset_types'][asset_type] = {
                    'count': 0,
                    'total_value': 0
                }
            market_overview['asset_types'][asset_type]['count'] += 1
            market_overview['asset_types'][asset_type]['total_value'] += asset.current_value or 0
        
        # Calcular percentuais
        for asset_type in market_overview['asset_types']:
            market_overview['asset_types'][asset_type]['percentage'] = (
                market_overview['asset_types'][asset_type]['total_value'] / total_value * 100
            ) if total_value > 0 else 0
        
        # Análise de concentração
        if total_value > 0:
            for asset in assets:
                concentration = (asset.current_value or 0) / total_value * 100
                if concentration <= 10:
                    market_overview['concentration_analysis']['well_diversified'] += 1
                elif concentration <= 20:
                    market_overview['concentration_analysis']['moderately_concentrated'] += 1
                else:
                    market_overview['concentration_analysis']['highly_concentrated'] += 1
        
        market_overview['total_portfolio_value'] = total_value
        market_overview['analysis_timestamp'] = datetime.now().isoformat()
        
        return jsonify(market_overview), 200
        
    except Exception as e:
        logger.error(f"Erro na visão geral do mercado: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

def get_risk_alerts_controller(req):
    """Obtém alertas de risco baseados em métricas em tempo real"""
    try:
        family_id = req.args.get("family_id")
        if not family_id:
            return jsonify({"error": "family_id é obrigatório"}), 400
        
        try:
            family_id = int(family_id)
        except (ValueError, TypeError):
            return jsonify({"error": "family_id deve ser um número válido"}), 400
        
        # Verificar acesso à família
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        if not user or not any(f.id == family_id for f in user.families):
            return jsonify({"error": "Acesso à familia negado"}), 403
        
        # Buscar ativos da família
        assets = Asset.query.filter_by(family_id=family_id).all()
        
        if not assets:
            return jsonify({"alerts": [], "message": "Nenhum ativo encontrado"}), 200
        
        alerts = []
        total_value = sum(asset.current_value or 0 for asset in assets)
        
        for asset in assets:
            asset_value = asset.current_value or 0
            if asset_value <= 0:
                continue
            
            # Alerta de concentração
            concentration = (asset_value / total_value * 100) if total_value > 0 else 0
            if concentration > 30:
                alerts.append({
                    'type': 'concentration',
                    'severity': 'high',
                    'asset_id': asset.id,
                    'asset_name': asset.name,
                    'message': f'Ativo representa {concentration:.1f}% da carteira (limite: 30%)',
                    'value': concentration,
                    'limit': 30
                })
            elif concentration > 20:
                alerts.append({
                    'type': 'concentration',
                    'severity': 'medium',
                    'asset_id': asset.id,
                    'asset_name': asset.name,
                    'message': f'Ativo representa {concentration:.1f}% da carteira (limite: 20%)',
                    'value': concentration,
                    'limit': 20
                })
            
            # Alerta de liquidez (se disponível)
            if hasattr(asset, 'details') and asset.details:
                liquidity_score = asset.details.get('liquidity_score', 100)
                if liquidity_score < 25:
                    alerts.append({
                        'type': 'liquidity',
                        'severity': 'high',
                        'asset_id': asset.id,
                        'asset_name': asset.name,
                        'message': f'Baixa liquidez detectada (score: {liquidity_score})',
                        'value': liquidity_score,
                        'limit': 25
                    })
        
        # Ordenar alertas por severidade
        severity_order = {'high': 3, 'medium': 2, 'low': 1}
        alerts.sort(key=lambda x: severity_order.get(x['severity'], 0), reverse=True)
        
        return jsonify({
            'alerts': alerts,
            'total_alerts': len(alerts),
            'high_severity': len([a for a in alerts if a['severity'] == 'high']),
            'medium_severity': len([a for a in alerts if a['severity'] == 'medium']),
            'low_severity': len([a for a in alerts if a['severity'] == 'low']),
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Erro nos alertas de risco: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500
