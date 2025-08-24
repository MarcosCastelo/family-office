"""Report routes for generating PDF reports"""
from flask import Blueprint, request, send_file, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.report_service import ReportService
from app.models.user import User
from app.models.family import Family
from datetime import datetime
import io

reports_bp = Blueprint("reports", __name__, url_prefix="/reports")

@reports_bp.route("/portfolio/<int:family_id>", methods=["GET"])
@jwt_required()
def generate_portfolio_report(family_id):
    """Generate portfolio summary report"""
    try:
        # Verify user has access to family
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or not any(f.id == family_id for f in user.families):
            return jsonify({"error": "Acesso negado"}), 403
        
        # Generate report
        report_service = ReportService()
        pdf_content = report_service.generate_portfolio_summary(family_id)
        
        # Return PDF file
        pdf_io = io.BytesIO(pdf_content)
        pdf_io.seek(0)
        
        return send_file(
            pdf_io,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"portfolio_report_{family_id}_{datetime.now().strftime('%Y%m%d')}.pdf"
        )
        
    except Exception as e:
        return jsonify({"error": f"Erro ao gerar relatório: {str(e)}"}), 500

@reports_bp.route("/risk/<int:family_id>", methods=["GET"])
@jwt_required()
def generate_risk_report(family_id):
    """Generate risk analysis report"""
    try:
        # Verify user has access to family
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or not any(f.id == family_id for f in user.families):
            return jsonify({"error": "Acesso negado"}), 403
        
        # Generate report
        report_service = ReportService()
        pdf_content = report_service.generate_risk_analysis(family_id)
        
        # Return PDF file
        pdf_io = io.BytesIO(pdf_content)
        pdf_io.seek(0)
        
        return send_file(
            pdf_io,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"risk_report_{family_id}_{datetime.now().strftime('%Y%m%d')}.pdf"
        )
        
    except Exception as e:
        return jsonify({"error": f"Erro ao gerar relatório: {str(e)}"}), 500

@reports_bp.route("/transactions/<int:family_id>", methods=["GET"])
@jwt_required()
def generate_transaction_report(family_id):
    """Generate transaction history report"""
    try:
        # Verify user has access to family
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or not any(f.id == family_id for f in user.families):
            return jsonify({"error": "Acesso negado"}), 403
        
        # Get date parameters
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        if not start_date_str or not end_date_str:
            return jsonify({"error": "start_date e end_date são obrigatórios"}), 400
        
        try:
            start_date = datetime.fromisoformat(start_date_str)
            end_date = datetime.fromisoformat(end_date_str)
        except ValueError:
            return jsonify({"error": "Formato de data inválido. Use ISO format (YYYY-MM-DD)"}), 400
        
        # Generate report
        report_service = ReportService()
        pdf_content = report_service.generate_transaction_history(family_id, start_date, end_date)
        
        # Return PDF file
        pdf_io = io.BytesIO(pdf_content)
        pdf_io.seek(0)
        
        return send_file(
            pdf_io,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"transactions_report_{family_id}_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.pdf"
        )
        
    except Exception as e:
        return jsonify({"error": f"Erro ao gerar relatório: {str(e)}"}), 500

@reports_bp.route("/fiscal/<int:family_id>", methods=["GET"])
@jwt_required()
def generate_fiscal_report(family_id):
    """Generate fiscal report"""
    try:
        # Verify user has access to family
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or not any(f.id == family_id for f in user.families):
            return jsonify({"error": "Acesso negado"}), 403
        
        # Get year parameter
        year_str = request.args.get('year')
        if not year_str:
            year = datetime.now().year
        else:
            try:
                year = int(year_str)
                if year < 1900 or year > 2100:
                    return jsonify({"error": "Ano deve estar entre 1900 e 2100"}), 400
            except ValueError:
                return jsonify({"error": "Ano deve ser um número válido"}), 400
        
        # Generate report
        report_service = ReportService()
        pdf_content = report_service.generate_fiscal_report(family_id, year)
        
        # Return PDF file
        pdf_io = io.BytesIO(pdf_content)
        pdf_io.seek(0)
        
        return send_file(
            pdf_io,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"fiscal_report_{family_id}_{year}.pdf"
        )
        
    except Exception as e:
        return jsonify({"error": f"Erro ao gerar relatório: {str(e)}"}), 500

@reports_bp.route("/available/<int:family_id>", methods=["GET"])
@jwt_required()
def get_available_reports(family_id):
    """Get list of available reports for a family"""
    try:
        # Verify user has access to family
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or not any(f.id == family_id for f in user.families):
            return jsonify({"error": "Acesso negado"}), 403
        
        reports = [
            {
                "type": "portfolio",
                "name": "Relatório de Carteira",
                "description": "Visão geral da carteira com alocação e performance",
                "endpoint": f"/reports/portfolio/{family_id}",
                "parameters": {}
            },
            {
                "type": "risk",
                "name": "Análise de Risco",
                "description": "Análise detalhada de risco da carteira",
                "endpoint": f"/reports/risk/{family_id}",
                "parameters": {}
            },
            {
                "type": "transactions",
                "name": "Histórico de Transações",
                "description": "Relatório de transações por período",
                "endpoint": f"/reports/transactions/{family_id}",
                "parameters": {
                    "start_date": "YYYY-MM-DD",
                    "end_date": "YYYY-MM-DD"
                }
            },
            {
                "type": "fiscal",
                "name": "Relatório Fiscal",
                "description": "Relatório para declaração de imposto de renda",
                "endpoint": f"/reports/fiscal/{family_id}",
                "parameters": {
                    "year": "YYYY (opcional, padrão: ano atual)"
                }
            }
        ]
        
        return jsonify({
            "family_id": family_id,
            "reports": reports
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao listar relatórios: {str(e)}"}), 500
