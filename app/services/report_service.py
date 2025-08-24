"""Report service for generating PDF reports using WeasyPrint"""
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from weasyprint import HTML, CSS
from jinja2 import Template
import json
from app.models.family import Family
from app.models.asset import Asset
from app.models.transaction import Transaction
from app.services.quote_service import QuoteService

logger = logging.getLogger(__name__)

class ReportService:
    """Service for generating various reports"""
    
    def __init__(self):
        self.quote_service = QuoteService()
        self._load_templates()
    
    def _load_templates(self):
        """Load HTML templates for reports"""
        self.templates = {
            'portfolio_summary': self._get_portfolio_template(),
            'risk_analysis': self._get_risk_template(),
            'transaction_history': self._get_transaction_template(),
            'fiscal_report': self._get_fiscal_template()
        }
    
    def generate_portfolio_summary(self, family_id: int, include_charts: bool = True) -> bytes:
        """Generate portfolio summary report"""
        try:
            family = Family.query.get(family_id)
            if not family:
                raise ValueError(f"Family {family_id} not found")
            
            # Gather portfolio data
            portfolio_data = self._get_portfolio_data(family)
            
            # Generate HTML
            html_content = self.templates['portfolio_summary'].render(
                family=family,
                portfolio=portfolio_data,
                include_charts=include_charts,
                generated_at=datetime.now()
            )
            
            # Convert to PDF
            pdf_content = self._html_to_pdf(html_content)
            
            logger.info(f"Portfolio summary generated for family {family_id}")
            return pdf_content
            
        except Exception as e:
            logger.error(f"Error generating portfolio summary: {e}")
            raise
    
    def generate_risk_analysis(self, family_id: int) -> bytes:
        """Generate risk analysis report"""
        try:
            family = Family.query.get(family_id)
            if not family:
                raise ValueError(f"Family {family_id} not found")
            
            # Gather risk data
            risk_data = self._get_risk_data(family)
            
            # Generate HTML
            html_content = self.templates['risk_analysis'].render(
                family=family,
                risk=risk_data,
                generated_at=datetime.now()
            )
            
            # Convert to PDF
            pdf_content = self._html_to_pdf(html_content)
            
            logger.info(f"Risk analysis generated for family {family_id}")
            return pdf_content
            
        except Exception as e:
            logger.error(f"Error generating risk analysis: {e}")
            raise
    
    def generate_transaction_history(self, family_id: int, start_date: datetime, end_date: datetime) -> bytes:
        """Generate transaction history report"""
        try:
            family = Family.query.get(family_id)
            if not family:
                raise ValueError(f"Family {family_id} not found")
            
            # Gather transaction data
            transaction_data = self._get_transaction_data(family, start_date, end_date)
            
            # Generate HTML
            html_content = self.templates['transaction_history'].render(
                family=family,
                transactions=transaction_data,
                start_date=start_date,
                end_date=end_date,
                generated_at=datetime.now()
            )
            
            # Convert to PDF
            pdf_content = self._html_to_pdf(html_content)
            
            logger.info(f"Transaction history generated for family {family_id}")
            return pdf_content
            
        except Exception as e:
            logger.error(f"Error generating transaction history: {e}")
            raise
    
    def generate_fiscal_report(self, family_id: int, year: int) -> bytes:
        """Generate fiscal report for tax purposes"""
        try:
            family = Family.query.get(family_id)
            if not family:
                raise ValueError(f"Family {family_id} not found")
            
            # Gather fiscal data
            fiscal_data = self._get_fiscal_data(family, year)
            
            # Generate HTML
            html_content = self.templates['fiscal_report'].render(
                family=family,
                fiscal=fiscal_data,
                year=year,
                generated_at=datetime.now()
            )
            
            # Convert to PDF
            pdf_content = self._html_to_pdf(html_content)
            
            logger.info(f"Fiscal report generated for family {family_id}, year {year}")
            return pdf_content
            
        except Exception as e:
            logger.error(f"Error generating fiscal report: {e}")
            raise
    
    def _get_portfolio_data(self, family: Family) -> Dict:
        """Gather portfolio data for report"""
        try:
            assets = family.assets
            total_value = family.total_patrimony
            total_invested = family.total_invested
            cash_balance = family.cash_balance
            
            # Asset allocation by type
            allocation = family.asset_allocation
            
            # Top assets by value
            top_assets = sorted(assets, key=lambda x: x.current_value, reverse=True)[:10]
            
            # Performance metrics
            performance = self._calculate_performance_metrics(family)
            
            return {
                'total_value': total_value,
                'total_invested': total_invested,
                'cash_balance': cash_balance,
                'allocation': allocation,
                'top_assets': top_assets,
                'performance': performance,
                'asset_count': len(assets)
            }
            
        except Exception as e:
            logger.error(f"Error gathering portfolio data: {e}")
            return {}
    
    def _get_risk_data(self, family: Family) -> Dict:
        """Gather risk analysis data"""
        try:
            # Get current alerts (simplified - just count them)
            try:
                from app.models.alert import Alert
                alerts = Alert.query.filter_by(family_id=family.id, is_resolved=False).all()
            except:
                alerts = []  # If Alert model doesn't exist yet
            
            # Calculate risk scores
            risk_scores = {
                'concentration': self._calculate_concentration_risk(family),
                'liquidity': self._calculate_liquidity_risk(family),
                'volatility': self._calculate_volatility_risk(family),
                'overall': 0.0
            }
            
            # Calculate overall risk score
            risk_scores['overall'] = sum(risk_scores.values()) / len(risk_scores)
            
            return {
                'risk_scores': risk_scores,
                'alerts': alerts,
                'recommendations': self._generate_risk_recommendations(risk_scores)
            }
            
        except Exception as e:
            logger.error(f"Error gathering risk data: {e}")
            return {}
    
    def _get_transaction_data(self, family: Family, start_date: datetime, end_date: datetime) -> Dict:
        """Gather transaction data for report"""
        try:
            # Get transactions in date range
            transactions = Transaction.query.join(Asset).filter(
                Asset.family_id == family.id,
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date
            ).order_by(Transaction.transaction_date.desc()).all()
            
            # Group by month
            monthly_data = {}
            for transaction in transactions:
                month_key = transaction.transaction_date.strftime('%Y-%m')
                if month_key not in monthly_data:
                    monthly_data[month_key] = {'buys': 0, 'sells': 0, 'count': 0}
                
                if transaction.transaction_type == 'buy':
                    monthly_data[month_key]['buys'] += transaction.total_value
                else:
                    monthly_data[month_key]['sells'] += transaction.total_value
                
                monthly_data[month_key]['count'] += 1
            
            return {
                'transactions': transactions,
                'monthly_summary': monthly_data,
                'total_buys': sum(t.total_value for t in transactions if t.transaction_type == 'buy'),
                'total_sells': sum(t.total_value for t in transactions if t.transaction_type == 'sell'),
                'transaction_count': len(transactions)
            }
            
        except Exception as e:
            logger.error(f"Error gathering transaction data: {e}")
            return {}
    
    def _get_fiscal_data(self, family: Family, year: int) -> Dict:
        """Gather fiscal data for tax reporting"""
        try:
            start_date = datetime(year, 1, 1)
            end_date = datetime(year, 12, 31)
            
            # Get all transactions for the year
            transactions = Transaction.query.join(Asset).filter(
                Asset.family_id == family.id,
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date
            ).all()
            
            # Calculate gains/losses
            fiscal_summary = {
                'total_buys': 0,
                'total_sells': 0,
                'realized_gains': 0,
                'realized_losses': 0,
                'dividends': 0,
                'interest': 0
            }
            
            for transaction in transactions:
                if transaction.transaction_type == 'buy':
                    fiscal_summary['total_buys'] += transaction.total_value
                elif transaction.transaction_type == 'sell':
                    fiscal_summary['total_sells'] += transaction.total_value
                    # Calculate realized gain/loss (simplified)
                    # In production, implement proper FIFO/LIFO calculation
            
            return fiscal_summary
            
        except Exception as e:
            logger.error(f"Error gathering fiscal data: {e}")
            return {}
    
    def _calculate_performance_metrics(self, family: Family) -> Dict:
        """Calculate portfolio performance metrics"""
        try:
            # Simplified performance calculation
            # In production, implement proper time-weighted returns
            
            total_return = 0
            if family.total_invested > 0:
                total_return = ((family.total_patrimony - family.total_invested) / family.total_invested) * 100
            
            return {
                'total_return_percent': round(total_return, 2),
                'absolute_return': family.total_patrimony - family.total_invested,
                'cash_ratio': round((family.cash_balance / family.total_patrimony) * 100, 2) if family.total_patrimony > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"Error calculating performance metrics: {e}")
            return {}
    
    def _calculate_concentration_risk(self, family: Family) -> float:
        """Calculate concentration risk score"""
        try:
            if not family.assets:
                return 0.0
            
            # Calculate Herfindahl-Hirschman Index
            total_value = family.total_patrimony
            if total_value <= 0:
                return 0.0
            
            hhi = sum((asset.current_value / total_value) ** 2 for asset in family.assets)
            
            # Normalize to 0-100 scale
            return min(hhi * 100, 100.0)
            
        except Exception as e:
            logger.error(f"Error calculating concentration risk: {e}")
            return 0.0
    
    def _calculate_liquidity_risk(self, family: Family) -> float:
        """Calculate liquidity risk score"""
        try:
            if not family.assets:
                return 0.0
            
            # Simplified liquidity calculation
            # In production, implement proper liquidity scoring
            illiquid_assets = sum(1 for asset in family.assets if asset.asset_type in ['imoveis', 'fundos_imobiliarios'])
            total_assets = len(family.assets)
            
            if total_assets == 0:
                return 0.0
            
            illiquidity_ratio = illiquid_assets / total_assets
            return illiquidity_ratio * 100
            
        except Exception as e:
            logger.error(f"Error calculating liquidity risk: {e}")
            return 0.0
    
    def _calculate_volatility_risk(self, family: Family) -> float:
        """Calculate volatility risk score"""
        try:
            if not family.assets:
                return 0.0
            
            # Simplified volatility calculation
            # In production, implement proper volatility scoring
            high_volatility_assets = sum(1 for asset in family.assets if asset.asset_type in ['renda_variavel', 'criptomoeda'])
            total_assets = len(family.assets)
            
            if total_assets == 0:
                return 0.0
            
            volatility_ratio = high_volatility_assets / total_assets
            return volatility_ratio * 100
            
        except Exception as e:
            logger.error(f"Error calculating volatility risk: {e}")
            return 0.0
    
    def _generate_risk_recommendations(self, risk_scores: Dict) -> List[str]:
        """Generate risk management recommendations"""
        recommendations = []
        
        if risk_scores['concentration'] > 70:
            recommendations.append("Considerar diversificação da carteira para reduzir concentração")
        
        if risk_scores['liquidity'] > 50:
            recommendations.append("Avaliar alocação em ativos mais líquidos")
        
        if risk_scores['volatility'] > 60:
            recommendations.append("Considerar aumento da alocação em renda fixa para estabilidade")
        
        if risk_scores['overall'] > 70:
            recommendations.append("Recomenda-se revisão completa da estratégia de investimento")
        
        if not recommendations:
            recommendations.append("Carteira bem balanceada, manter estratégia atual")
        
        return recommendations
    
    def _html_to_pdf(self, html_content: str) -> bytes:
        """Convert HTML content to PDF"""
        try:
            # Create HTML object
            html = HTML(string=html_content)
            
            # Convert to PDF
            pdf_bytes = html.write_pdf()
            
            return pdf_bytes
            
        except Exception as e:
            logger.error(f"Error converting HTML to PDF: {e}")
            raise
    
    def _get_portfolio_template(self) -> Template:
        """Get portfolio summary HTML template"""
        template_str = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Relatório de Carteira - {{ family.name }}</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; }
                .section { margin: 20px 0; }
                .metric { display: inline-block; margin: 10px; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
                .metric-value { font-size: 24px; font-weight: bold; color: #2c3e50; }
                .metric-label { font-size: 12px; color: #7f8c8d; }
                table { width: 100%; border-collapse: collapse; margin: 10px 0; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f8f9fa; }
                .positive { color: #27ae60; }
                .negative { color: #e74c3c; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Relatório de Carteira</h1>
                <h2>{{ family.name }}</h2>
                <p>Gerado em: {{ generated_at.strftime('%d/%m/%Y às %H:%M') }}</p>
            </div>
            
            <div class="section">
                <h3>Resumo Geral</h3>
                <div class="metric">
                    <div class="metric-value">R$ {{ "%.2f"|format(portfolio.total_value) }}</div>
                    <div class="metric-label">Patrimônio Total</div>
                </div>
                <div class="metric">
                    <div class="metric-value">R$ {{ "%.2f"|format(portfolio.total_invested) }}</div>
                    <div class="metric-label">Investido</div>
                </div>
                <div class="metric">
                    <div class="metric-value">R$ {{ "%.2f"|format(portfolio.cash_balance) }}</div>
                    <div class="metric-label">Disponível</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{{ portfolio.asset_count }}</div>
                    <div class="metric-label">Ativos</div>
                </div>
            </div>
            
            <div class="section">
                <h3>Alocação por Classe</h3>
                <table>
                    <tr><th>Classe</th><th>Valor</th><th>Percentual</th></tr>
                    {% for classe, valor in portfolio.allocation.items() %}
                    <tr>
                        <td>{{ classe.replace('_', ' ').title() }}</td>
                        <td>R$ {{ "%.2f"|format(valor) }}</td>
                        <td>{{ "%.1f"|format((valor / portfolio.total_value) * 100) }}%</td>
                    </tr>
                    {% endfor %}
                </table>
            </div>
            
            <div class="section">
                <h3>Principais Ativos</h3>
                <table>
                    <tr><th>Nome</th><th>Tipo</th><th>Valor Atual</th><th>Quantidade</th></tr>
                    {% for asset in portfolio.top_assets %}
                    <tr>
                        <td>{{ asset.name }}</td>
                        <td>{{ asset.asset_type.replace('_', ' ').title() }}</td>
                        <td>R$ {{ "%.2f"|format(asset.current_value) }}</td>
                        <td>{{ "%.2f"|format(asset.current_quantity) }}</td>
                    </tr>
                    {% endfor %}
                </table>
            </div>
            
            <div class="section">
                <h3>Performance</h3>
                <div class="metric">
                    <div class="metric-value {% if portfolio.performance.total_return_percent >= 0 %}positive{% else %}negative{% endif %}">
                        {{ "%.2f"|format(portfolio.performance.total_return_percent) }}%
                    </div>
                    <div class="metric-label">Retorno Total</div>
                </div>
                <div class="metric">
                    <div class="metric-value {% if portfolio.performance.absolute_return >= 0 %}positive{% else %}negative{% endif %}">
                        R$ {{ "%.2f"|format(portfolio.performance.absolute_return) }}
                    </div>
                    <div class="metric-label">Retorno Absoluto</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{{ "%.1f"|format(portfolio.performance.cash_ratio) }}%</div>
                    <div class="metric-label">Razão Caixa</div>
                </div>
            </div>
        </body>
        </html>
        """
        return Template(template_str)
    
    def _get_risk_template(self) -> Template:
        """Get risk analysis HTML template"""
        template_str = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Análise de Risco - {{ family.name }}</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; }
                .section { margin: 20px 0; }
                .risk-score { display: inline-block; margin: 10px; padding: 15px; border-radius: 5px; }
                .low-risk { background-color: #d4edda; border: 1px solid #c3e6cb; }
                .medium-risk { background-color: #fff3cd; border: 1px solid #ffeaa7; }
                .high-risk { background-color: #f8d7da; border: 1px solid #f5c6cb; }
                .score-value { font-size: 24px; font-weight: bold; }
                .recommendations { background-color: #f8f9fa; padding: 15px; border-radius: 5px; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Análise de Risco</h1>
                <h2>{{ family.name }}</h2>
                <p>Gerado em: {{ generated_at.strftime('%d/%m/%Y às %H:%M') }}</p>
            </div>
            
            <div class="section">
                <h3>Score de Risco Geral</h3>
                <div class="risk-score {% if risk.risk_scores.overall < 30 %}low-risk{% elif risk.risk_scores.overall < 70 %}medium-risk{% else %}high-risk{% endif %}">
                    <div class="score-value">{{ "%.1f"|format(risk.risk_scores.overall) }}</div>
                    <div>Score de Risco</div>
                </div>
            </div>
            
            <div class="section">
                <h3>Análise Detalhada</h3>
                <div class="risk-score {% if risk.risk_scores.concentration < 30 %}low-risk{% elif risk.risk_scores.concentration < 70 %}medium-risk{% else %}high-risk{% endif %}">
                    <div class="score-value">{{ "%.1f"|format(risk.risk_scores.concentration) }}</div>
                    <div>Risco de Concentração</div>
                </div>
                <div class="risk-score {% if risk.risk_scores.liquidity < 30 %}low-risk{% elif risk.risk_scores.liquidity < 70 %}medium-risk{% else %}high-risk{% endif %}">
                    <div class="score-value">{{ "%.1f"|format(risk.risk_scores.liquidity) }}</div>
                    <div>Risco de Liquidez</div>
                </div>
                <div class="risk-score {% if risk.risk_scores.volatility < 30 %}low-risk{% elif risk.risk_scores.volatility < 70 %}medium-risk{% else %}high-risk{% endif %}">
                    <div class="score-value">{{ "%.1f"|format(risk.risk_scores.volatility) }}</div>
                    <div>Risco de Volatilidade</div>
                </div>
            </div>
            
            <div class="section">
                <h3>Alertas Ativos</h3>
                {% if risk.alerts %}
                    <ul>
                    {% for alert in risk.alerts %}
                        <li><strong>{{ alert.type }}:</strong> {{ alert.message }}</li>
                    {% endfor %}
                    </ul>
                {% else %}
                    <p>Nenhum alerta ativo.</p>
                {% endif %}
            </div>
            
            <div class="section">
                <h3>Recomendações</h3>
                <div class="recommendations">
                    <ul>
                    {% for rec in risk.recommendations %}
                        <li>{{ rec }}</li>
                    {% endfor %}
                    </ul>
                </div>
            </div>
        </body>
        </html>
        """
        return Template(template_str)
    
    def _get_transaction_template(self) -> Template:
        """Get transaction history HTML template"""
        template_str = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Histórico de Transações - {{ family.name }}</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; }
                .section { margin: 20px 0; }
                table { width: 100%; border-collapse: collapse; margin: 10px 0; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f8f9fa; }
                .buy { color: #27ae60; }
                .sell { color: #e74c3c; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Histórico de Transações</h1>
                <h2>{{ family.name }}</h2>
                <p>Período: {{ start_date.strftime('%d/%m/%Y') }} a {{ end_date.strftime('%d/%m/%Y') }}</p>
                <p>Gerado em: {{ generated_at.strftime('%d/%m/%Y às %H:%M') }}</p>
            </div>
            
            <div class="section">
                <h3>Resumo do Período</h3>
                <p><strong>Total de Compras:</strong> R$ {{ "%.2f"|format(transactions.total_buys) }}</p>
                <p><strong>Total de Vendas:</strong> R$ {{ "%.2f"|format(transactions.total_sells) }}</p>
                <p><strong>Número de Transações:</strong> {{ transactions.transaction_count }}</p>
            </div>
            
            <div class="section">
                <h3>Transações</h3>
                <table>
                    <tr><th>Data</th><th>Tipo</th><th>Ativo</th><th>Quantidade</th><th>Preço Unit.</th><th>Valor Total</th></tr>
                    {% for transaction in transactions.transactions %}
                    <tr>
                        <td>{{ transaction.transaction_date.strftime('%d/%m/%Y') }}</td>
                        <td class="{% if transaction.transaction_type == 'buy' %}buy{% else %}sell{% endif %}">
                            {{ 'Compra' if transaction.transaction_type == 'buy' else 'Venda' }}
                        </td>
                        <td>{{ transaction.asset.name }}</td>
                        <td>{{ "%.2f"|format(transaction.quantity) }}</td>
                        <td>R$ {{ "%.2f"|format(transaction.unit_price) }}</td>
                        <td>R$ {{ "%.2f"|format(transaction.total_value) }}</td>
                    </tr>
                    {% endfor %}
                </table>
            </div>
        </body>
        </html>
        """
        return Template(template_str)
    
    def _get_fiscal_template(self) -> Template:
        """Get fiscal report HTML template"""
        template_str = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Relatório Fiscal {{ year }} - {{ family.name }}</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; }
                .section { margin: 20px 0; }
                .metric { display: inline-block; margin: 10px; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
                .metric-value { font-size: 24px; font-weight: bold; color: #2c3e50; }
                .metric-label { font-size: 12px; color: #7f8c8d; }
                .positive { color: #27ae60; }
                .negative { color: #e74c3c; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Relatório Fiscal {{ year }}</h1>
                <h2>{{ family.name }}</h2>
                <p>Gerado em: {{ generated_at.strftime('%d/%m/%Y às %H:%M') }}</p>
            </div>
            
            <div class="section">
                <h3>Resumo Fiscal</h3>
                <div class="metric">
                    <div class="metric-value">R$ {{ "%.2f"|format(fiscal.total_buys) }}</div>
                    <div class="metric-label">Total de Compras</div>
                </div>
                <div class="metric">
                    <div class="metric-value">R$ {{ "%.2f"|format(fiscal.total_sells) }}</div>
                    <div class="metric-label">Total de Vendas</div>
                </div>
                <div class="metric">
                    <div class="metric-value {% if fiscal.realized_gains >= 0 %}positive{% else %}negative{% endif %}">
                        R$ {{ "%.2f"|format(fiscal.realized_gains) }}
                    </div>
                    <div class="metric-label">Ganhos Realizados</div>
                </div>
                <div class="metric">
                    <div class="metric-value {% if fiscal.realized_losses >= 0 %}positive{% else %}negative{% endif %}">
                        R$ {{ "%.2f"|format(fiscal.realized_losses) }}
                    </div>
                    <div class="metric-label">Perdas Realizadas</div>
                </div>
            </div>
            
            <div class="section">
                <h3>Rendimentos</h3>
                <p><strong>Dividendos:</strong> R$ {{ "%.2f"|format(fiscal.dividends) }}</p>
                <p><strong>Juros:</strong> R$ {{ "%.2f"|format(fiscal.interest) }}</p>
            </div>
            
            <div class="section">
                <h3>Observações</h3>
                <p>Este relatório é gerado automaticamente e deve ser revisado por um contador ou consultor fiscal antes da declaração.</p>
                <p>Os valores são calculados com base nas transações registradas no sistema.</p>
            </div>
        </body>
        </html>
        """
        return Template(template_str)
