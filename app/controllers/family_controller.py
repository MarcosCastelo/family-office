"""Family Controller for managing family-related operations including cash balance"""
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from app.models.family import Family
from app.models.user import User
from app.config.extensions import db
from marshmallow import Schema, fields, ValidationError


class CashBalanceSchema(Schema):
    """Schema for cash balance operations"""
    amount = fields.Float(required=True, validate=lambda x: x > 0)
    description = fields.Str(load_default="Operação de caixa")


def add_cash_controller(family_id):
    """Add cash to family balance"""
    try:
        # Validate input
        schema = CashBalanceSchema()
        try:
            validated_data = schema.load(request.get_json())
        except ValidationError as e:
            return jsonify({"error": e.messages}), 400
        
        # Verify family exists and user has access
        family = db.session.get(Family, family_id)
        if not family:
            return jsonify({"error": "Família não encontrada"}), 404
        
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        if not user or not any(f.id == family_id for f in user.families):
            return jsonify({"error": "Acesso negado"}), 403
        
        # Add cash to balance
        amount = validated_data['amount']
        family.cash_balance += amount
        db.session.commit()
        
        return jsonify({
            "message": f"R$ {amount:.2f} adicionado ao saldo",
            "new_balance": family.cash_balance,
            "patrimony_total": family.total_patrimony
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500


def withdraw_cash_controller(family_id):
    """Withdraw cash from family balance"""
    try:
        # Validate input
        schema = CashBalanceSchema()
        try:
            validated_data = schema.load(request.get_json())
        except ValidationError as e:
            return jsonify({"error": e.messages}), 400
        
        # Verify family exists and user has access
        family = db.session.get(Family, family_id)
        if not family:
            return jsonify({"error": "Família não encontrada"}), 404
        
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        if not user or not any(f.id == family_id for f in user.families):
            return jsonify({"error": "Acesso negado"}), 403
        
        # Check if withdrawal is possible
        amount = validated_data['amount']
        if family.cash_balance < amount:
            return jsonify({
                "error": f"Saldo insuficiente. Disponível: R$ {family.cash_balance:.2f}, Solicitado: R$ {amount:.2f}"
            }), 400
        
        # Withdraw cash from balance
        family.cash_balance -= amount
        db.session.commit()
        
        return jsonify({
            "message": f"R$ {amount:.2f} retirado do saldo",
            "new_balance": family.cash_balance,
            "patrimony_total": family.total_patrimony
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500


def get_family_balance_controller(family_id):
    """Get family cash balance and patrimony information"""
    try:
        # Verify family exists and user has access
        family = db.session.get(Family, family_id)
        if not family:
            return jsonify({"error": "Família não encontrada"}), 404
        
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        if not user or not any(f.id == family_id for f in user.families):
            return jsonify({"error": "Acesso negado"}), 403
        
        return jsonify({
            "cash_balance": family.cash_balance,
            "total_invested": family.total_invested,
            "total_patrimony": family.total_patrimony,
            "percentual_investido": round((family.total_invested / family.total_patrimony * 100) if family.total_patrimony > 0 else 0, 2),
            "asset_allocation": family.asset_allocation
        }), 200
        
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500


def get_family_risk_summary_controller(family_id):
    """Get family risk summary"""
    try:
        # Get current user
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 401
        
        # Check if user belongs to the family
        family = db.session.get(Family, family_id)
        if not family:
            return jsonify({"error": "Família não encontrada"}), 404
            
        if family not in user.families:
            return jsonify({"error": "Acesso negado"}), 403
        
        # Calculate risk summary
        total_assets = len(family.assets)
        high_risk_assets = sum(1 for asset in family.assets if asset.asset_type == "renda_variavel")
        medium_risk_assets = sum(1 for asset in family.assets if asset.asset_type == "fundo_imobiliario")
        low_risk_assets = sum(1 for asset in family.assets if asset.asset_type == "renda_fixa")
        
        # Calculate percentages
        high_risk_pct = round((high_risk_assets / total_assets * 100) if total_assets > 0 else 0, 2)
        medium_risk_pct = round((medium_risk_assets / total_assets * 100) if total_assets > 0 else 0, 2)
        low_risk_pct = round((low_risk_assets / total_assets * 100) if total_assets > 0 else 0, 2)
        
        # Calculate global risk score (weighted average)
        score_global = round(
            (high_risk_pct * 0.8 + medium_risk_pct * 0.5 + low_risk_pct * 0.2) / 100 * 100, 1
        ) if total_assets > 0 else 0
        
        # Determine risk classification
        if score_global >= 70:
            classificacao_final = "crítico"
        elif score_global >= 50:
            classificacao_final = "alto"
        elif score_global >= 30:
            classificacao_final = "médio"
        else:
            classificacao_final = "baixo"
        
        return jsonify({
            "family_id": family_id,
            "score_global": score_global,
            "concentracao": round(high_risk_pct, 1),
            "volatilidade": round((high_risk_pct + medium_risk_pct) / 2, 1),
            "liquidez_aggregada": round(100 - high_risk_pct, 1),
            "exposicao_cambial": round(high_risk_pct * 0.3, 1),
            "risco_fiscal_regulatorio": round(medium_risk_pct * 0.4, 1),
            "classificacao_final": classificacao_final
        }), 200
        
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500