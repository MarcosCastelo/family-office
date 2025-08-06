from flask import jsonify
from app.models.family import Family
from app.models.user import User
from app.models.asset import Asset
from app.config.extensions import db
from app.models.alert import Alert
from app.schema.alert_schema import AlertSchema

alert_schema = AlertSchema()
alerts_schema = AlertSchema(many=True)

def get_family_risk_summary_controller(family_id):
    from flask_jwt_extended import get_jwt_identity
    # Verifica se família existe
    family = db.session.get(Family, family_id)
    if not family:
        return jsonify({"error": "Família não encontrada"}), 404
    # Verifica permissão
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    if not user or not any(f.id == family_id for f in user.families):
        return jsonify({"error": "Acesso à família negado"}), 403
    # Busca ativos da família
    assets = Asset.query.filter_by(family_id=family_id).all()
    if not assets:
        score = {
            "family_id": family_id,
            "score_global": 0,
            "concentracao": 0,
            "volatilidade": 0,
            "liquidez_aggregada": 0,
            "exposicao_cambial": 0,
            "risco_fiscal_regulatorio": 0,
            "classificacao_final": "baixo"
        }
        return jsonify(score), 200
    total = sum(a.value for a in assets)
    # [DEBUG] prints removidos
    # Concentração: maior ativo / total
    maior = max(a.value for a in assets)
    concentracao = int((maior / total) * 100) if total > 0 else 0
    # Volatilidade: renda_variavel = 20, outros = 0
    volatilidade = int(20 * sum(1 for a in assets if a.asset_type == "renda_variavel") / len(assets))
    # Liquidez agregada: ativos ilíquidos (>50%) = 20, senão 0
    def is_iliquido(a):
        d = a.details or {}
        return str(d.get("liquidez", "alta")).lower() == "baixa"
    iliquidos = [a for a in assets if is_iliquido(a)]
    # [DEBUG] prints removidos
    liq_agg = 20 if total > 0 and sum(a.value for a in iliquidos) / total > 0.5 else 0
    # Exposição cambial: ativos com details['moeda'] != 'BRL'
    exp_cambial = int(15 * sum(1 for a in assets if (a.details or {}).get("moeda", "BRL") != "BRL") / len(assets))
    # Risco fiscal/regulatório: mock 0
    risco_fiscal = 0
    # Score global ponderado
    score_global = int(0.3 * concentracao + 0.2 * volatilidade + 0.2 * liq_agg + 0.15 * exp_cambial + 0.15 * risco_fiscal)
    # Classificação final
    if score_global >= 70:
        classificacao_final = "crítico"
    elif score_global >= 50:
        classificacao_final = "alto"
    elif score_global >= 30:
        classificacao_final = "médio"
    else:
        classificacao_final = "baixo"
    score = {
        "family_id": family_id,
        "score_global": score_global,
        "concentracao": concentracao,
        "volatilidade": volatilidade,
        "liquidez_aggregada": liq_agg,
        "exposicao_cambial": exp_cambial,
        "risco_fiscal_regulatorio": risco_fiscal,
        "classificacao_final": classificacao_final
    }
    return jsonify(score), 200

def list_family_alerts_controller(family_id):
    from flask_jwt_extended import get_jwt_identity
    from flask import jsonify
    family = db.session.get(Family, family_id)
    if not family:
        return jsonify({"error": "Família não encontrada"}), 404
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    if not user or not any(f.id == family_id for f in user.families):
        return jsonify({"error": "Acesso à família negado"}), 403
    alerts = Alert.query.filter_by(family_id=family_id).order_by(Alert.criado_em.desc()).all()
    return jsonify(alerts_schema.dump(alerts)), 200
