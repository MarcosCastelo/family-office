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
    # Agregação de dados
    ativos = Asset.query.filter_by(family_id=family_id).all()
    valor_total = sum(a.value for a in ativos)
    num_ativos = len(ativos)
    # Distribuição por classe
    dist = {}
    for a in ativos:
        dist[a.asset_type] = dist.get(a.asset_type, 0) + a.value
    distribuicao_classes = [{"classe": k, "valor": v} for k, v in dist.items()]
    # Top 5 ativos
    top_ativos = sorted(ativos, key=lambda x: x.value, reverse=True)[:5]
    top_ativos = [{"id": a.id, "name": a.name, "value": a.value, "asset_type": a.asset_type} for a in top_ativos]
    # Alertas recentes
    alertas = Alert.query.filter_by(family_id=family_id).order_by(Alert.criado_em.desc()).limit(5).all()
    alertas_recentes = [{"tipo": a.tipo, "mensagem": a.mensagem, "severidade": a.severidade, "criado_em": a.criado_em.isoformat()} for a in alertas]
    # Score de risco (mock)
    score_risco = {"score_global": 23, "classificacao_final": "médio"}
    return jsonify({
        "valor_total": valor_total,
        "num_ativos": num_ativos,
        "distribuicao_classes": distribuicao_classes,
        "top_ativos": top_ativos,
        "alertas_recentes": alertas_recentes,
        "score_risco": score_risco
    }), 200 