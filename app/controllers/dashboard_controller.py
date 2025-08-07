from flask import jsonify, request
from app.models.family import Family
from app.models.user import User
from app.models.asset import Asset
from app.models.alert import Alert
from app.config.extensions import db

def dashboard_controller(req):
    from flask_jwt_extended import get_jwt_identity
    family_id = req.args.get("family_id")
    if not family_id:
        return jsonify({"error": "family_id é obrigatório"}), 400
    try:
        family_id = int(family_id)
    except (ValueError, TypeError):
        return jsonify({"error": "family_id deve ser um número válido"}), 400
    family = db.session.get(Family, family_id)
    if not family:
        return jsonify({"error": "Família não encontrada"}), 404
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    if not user or not any(f.id == family_id for f in user.families):
        return jsonify({"error": "Acesso à família negado"}), 403
    # Agregação de dados baseada no novo sistema de patrimônio
    ativos = Asset.query.filter_by(family_id=family_id).all()
    
    # Patrimônio investido (soma dos valores atuais dos ativos)
    patrimonio_investido = family.total_invested
    
    # Patrimônio não investido (saldo disponível)
    patrimonio_nao_investido = family.cash_balance
    
    # Patrimônio total
    patrimonio_total = family.total_patrimony
    
    num_ativos = len(ativos)
    
    # Distribuição por classe baseada no valor atual dos ativos
    distribuicao_classes = []
    for asset_type, value in family.asset_allocation.items():
        distribuicao_classes.append({"classe": asset_type, "valor": value})
    
    # Top 5 ativos por valor atual
    top_ativos = sorted(ativos, key=lambda x: x.current_value, reverse=True)[:5]
    top_ativos = [
        {
            "id": a.id, 
            "name": a.name, 
            "value": a.current_value, 
            "asset_type": a.asset_type,
            "quantity": a.current_quantity,
            "average_cost": a.average_cost
        } 
        for a in top_ativos
    ]
    # Alertas recentes
    alertas = Alert.query.filter_by(family_id=family_id).order_by(Alert.criado_em.desc()).limit(5).all()
    alertas_recentes = [{"tipo": a.tipo, "mensagem": a.mensagem, "severidade": a.severidade, "criado_em": a.criado_em.isoformat()} for a in alertas]
    # Score de risco (mock)
    score_risco = {"score_global": 23, "classificacao_final": "médio"}
    return jsonify({
        "patrimonio_total": patrimonio_total,
        "patrimonio_investido": patrimonio_investido,
        "patrimonio_nao_investido": patrimonio_nao_investido,
        "percentual_investido": round((patrimonio_investido / patrimonio_total * 100) if patrimonio_total > 0 else 0, 2),
        "num_ativos": num_ativos,
        "distribuicao_classes": distribuicao_classes,
        "top_ativos": top_ativos,
        "alertas_recentes": alertas_recentes,
        "score_risco": score_risco
    }), 200 