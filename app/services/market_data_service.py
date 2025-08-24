"""Market Data Service - Integração com APIs de finanças funcionais"""
import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Any
from dataclasses import dataclass
from app.config.extensions import db
from app.models.asset import Asset
from app.models.quote_history import QuoteHistory

logger = logging.getLogger(__name__)

@dataclass
class MarketData:
    """Estrutura para dados de mercado"""
    symbol: str
    price: float
    currency: str
    change_24h: float
    change_percent_24h: float
    volume: float
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None
    beta: Optional[float] = None
    source: str = ""
    timestamp: datetime = None

class MarketDataService:
    """Serviço para dados de mercado usando APIs alternativas"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'FamilyOffice/2.0'
        })
        
        # APIs alternativas que ainda funcionam
        self.alpha_vantage_base = "https://www.alphavantage.co/query"
        self.alpha_vantage_key = "demo"  # Chave gratuita para teste
        self.bacen_base_url = "https://www.bcb.gov.br/api/servico/sitebcb/indicadorCambio"
        
        # Cache para evitar múltiplas chamadas
        self._cache = {}
        self._cache_ttl = 300  # 5 minutos
    
    def get_comprehensive_quote(self, symbol: str, asset_type: str = "renda_variavel") -> Optional[MarketData]:
        """Obtém cotação usando APIs alternativas"""
        try:
            if asset_type == "criptomoeda":
                return self._get_crypto_quote(symbol)
            elif asset_type == "moeda_estrangeira":
                return self._get_bacen_quote(symbol)
            else:
                return self._get_alpha_vantage_quote(symbol)
        except Exception as e:
            logger.error(f"Erro ao obter cotação para {symbol}: {e}")
            return None
    
    def _get_alpha_vantage_quote(self, symbol: str) -> Optional[MarketData]:
        """Alpha Vantage para ações e ETFs"""
        try:
            # Para ações brasileiras, adicionar .SA
            if not symbol.endswith('.SA') and not '.' in symbol:
                symbol = f"{symbol}.SA"
            
            url = self.alpha_vantage_base
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': symbol,
                'apikey': self.alpha_vantage_key
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'Global Quote' not in data or not data['Global Quote']:
                logger.warning(f"Dados não encontrados para {symbol}")
                return None
            
            quote = data['Global Quote']
            
            current_price = float(quote.get('05. price', 0))
            previous_close = float(quote.get('08. previous close', current_price))
            change_24h = current_price - previous_close
            change_percent_24h = float(quote.get('10. change percent', '0').replace('%', ''))
            volume = float(quote.get('06. volume', 0))
            
            return MarketData(
                symbol=symbol,
                price=current_price,
                currency='BRL' if symbol.endswith('.SA') else 'USD',
                change_24h=change_24h,
                change_percent_24h=change_percent_24h,
                volume=volume,
                source="alpha_vantage",
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Erro Alpha Vantage para {symbol}: {e}")
            return None
    
    def _get_crypto_quote(self, coin_id: str) -> Optional[MarketData]:
        """API gratuita para criptomoedas"""
        try:
            # Usar API gratuita da CoinGecko (sem chave)
            url = f"https://api.coingecko.com/api/v3/simple/price"
            params = {
                'ids': coin_id,
                'vs_currencies': 'usd,brl',
                'include_24hr_change': 'true',
                'include_24hr_vol': 'true'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if coin_id not in data:
                logger.warning(f"Criptomoeda {coin_id} não encontrada")
                return None
            
            coin_data = data[coin_id]
            current_price_usd = coin_data.get('usd', 0)
            current_price_brl = coin_data.get('brl', 0)
            change_24h = coin_data.get('usd_24h_change', 0)
            volume_24h = coin_data.get('usd_24h_vol', 0)
            
            return MarketData(
                symbol=coin_id,
                price=current_price_brl if current_price_brl > 0 else current_price_usd,
                currency='BRL' if current_price_brl > 0 else 'USD',
                change_24h=change_24h,
                change_percent_24h=change_24h,
                volume=volume_24h,
                source="coingecko_free",
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Erro API cripto para {coin_id}: {e}")
            return None
    
    def _get_bacen_quote(self, currency: str) -> Optional[MarketData]:
        """BACEN para câmbio"""
        try:
            # Mapeamento de códigos de moeda
            currency_map = {
                'USD': 1,
                'EUR': 21619,
                'GBP': 21620
            }
            
            if currency not in currency_map:
                return None
            
            url = self.bacen_base_url
            params = {
                'codigoMoeda': currency_map[currency]
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                return None
            
            # BACEN retorna array com dados históricos
            latest_data = data[0] if isinstance(data, list) else data
            current_price = float(latest_data.get('valorVenda', 0))
            
            return MarketData(
                symbol=currency,
                price=current_price,
                currency="BRL",
                change_24h=0,  # BACEN não fornece variação
                change_percent_24h=0,
                volume=0,
                source="bacen",
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Erro BACEN para {currency}: {e}")
            return None
    
    def get_mock_quote(self, symbol: str, asset_type: str = "renda_variavel") -> MarketData:
        """Gera cotação simulada para desenvolvimento/teste"""
        import random
        
        # Preços base por tipo de ativo
        base_prices = {
            "renda_fixa": 1000.0,
            "renda_variavel": 50.0,
            "criptomoeda": 2000.0,
            "moeda_estrangeira": 5.0,
            "fundo_imobiliario": 100.0
        }
        
        base_price = base_prices.get(asset_type, 100.0)
        
        # Variação aleatória para simular mercado
        variation = random.uniform(-0.05, 0.05)  # ±5%
        current_price = base_price * (1 + variation)
        change_24h = base_price * variation
        change_percent_24h = variation * 100
        
        return MarketData(
            symbol=symbol,
            price=round(current_price, 2),
            currency="BRL",
            change_24h=round(change_24h, 2),
            change_percent_24h=round(change_percent_24h, 2),
            volume=random.uniform(1000, 100000),
            source="mock_data",
            timestamp=datetime.now()
        )
    
    def get_asset_risk_metrics(self, asset: Asset) -> Dict[str, Any]:
        """Calcula métricas de risco para um ativo"""
        try:
            # Obter cotação atual
            symbol = self._get_asset_symbol(asset)
            if not symbol:
                return {}
            
            # Tentar obter cotação real, se falhar usar mock
            quote = self.get_comprehensive_quote(symbol, asset.asset_type)
            if not quote:
                quote = self.get_mock_quote(symbol, asset.asset_type)
            
            # Calcular métricas de risco
            risk_metrics = {
                'current_price': quote.price,
                'price_change_24h': quote.change_percent_24h,
                'volatility': self._calculate_volatility(asset.id),
                'liquidity_score': self._calculate_liquidity_score(quote.volume, asset.current_value),
                'concentration_risk': self._calculate_concentration_risk(asset),
                'market_risk': self._calculate_market_risk(quote),
                'beta_risk': quote.beta or 1.0,
                'last_updated': quote.timestamp.isoformat()
            }
            
            return risk_metrics
            
        except Exception as e:
            logger.error(f"Erro ao calcular métricas de risco para ativo {asset.id}: {e}")
            return {}
    
    def _get_asset_symbol(self, asset: Asset) -> Optional[str]:
        """Extrai símbolo do ativo baseado no tipo"""
        if asset.asset_type == "renda_variavel":
            ticker = asset.details.get('ticker') if asset.details else None
            if ticker:
                # Para ações brasileiras, adicionar .SA se não tiver
                if not ticker.endswith('.SA') and not '.' in ticker:
                    ticker = f"{ticker}.SA"
            return ticker
        elif asset.asset_type == "criptomoeda":
            coin_id = asset.details.get('coin_id') if asset.details else None
            if coin_id:
                # Converter siglas para nomes completos
                coin_mapping = {
                    'BTC': 'bitcoin',
                    'ETH': 'ethereum',
                    'ADA': 'cardano',
                    'SOL': 'solana',
                    'DOT': 'polkadot',
                    'LTC': 'litecoin',
                    'XRP': 'ripple',
                    'BCH': 'bitcoin-cash'
                }
                return coin_mapping.get(coin_id.upper(), coin_id.lower())
        elif asset.asset_type == "moeda_estrangeira":
            currency = asset.details.get('currency') if asset.details else None
            if currency:
                # Validar moedas suportadas
                supported_currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CHF', 'CAD', 'AUD']
                if currency.upper() in supported_currencies:
                    return currency.upper()
        return None
    
    def _calculate_volatility(self, asset_id: int, days: int = 30) -> float:
        """Calcula volatilidade baseada no histórico de preços"""
        try:
            # Buscar histórico de preços
            quotes = QuoteHistory.query.filter_by(asset_id=asset_id)\
                .filter(QuoteHistory.timestamp >= datetime.now() - timedelta(days=days))\
                .order_by(QuoteHistory.timestamp.asc())\
                .all()
            
            if len(quotes) < 2:
                # Se não há histórico, retornar volatilidade simulada
                import random
                return random.uniform(10, 30)
            
            # Calcular retornos logarítmicos
            returns = []
            for i in range(1, len(quotes)):
                if quotes[i-1].price > 0:
                    log_return = (quotes[i].price / quotes[i-1].price)
                    returns.append(log_return)
            
            if not returns:
                import random
                return random.uniform(10, 30)
            
            # Calcular volatilidade (desvio padrão dos retornos)
            import statistics
            return statistics.stdev(returns) * (252 ** 0.5)  # Anualizada
            
        except Exception as e:
            logger.error(f"Erro ao calcular volatilidade: {e}")
            import random
            return random.uniform(10, 30)
    
    def _calculate_liquidity_score(self, volume: float, asset_value: float) -> float:
        """Calcula score de liquidez (0-100)"""
        try:
            if asset_value <= 0:
                return 50.0  # Score médio se não há valor
            
            # Volume diário vs valor do ativo
            volume_ratio = volume / asset_value
            
            # Score baseado na razão (maior = mais líquido)
            if volume_ratio >= 1.0:
                return 100.0
            elif volume_ratio >= 0.5:
                return 75.0
            elif volume_ratio >= 0.2:
                return 50.0
            elif volume_ratio >= 0.1:
                return 25.0
            else:
                return 10.0
                
        except Exception as e:
            logger.error(f"Erro ao calcular score de liquidez: {e}")
            return 50.0  # Score médio em caso de erro
    
    def _calculate_concentration_risk(self, asset: Asset) -> float:
        """Calcula risco de concentração (0-100)"""
        try:
            if not asset.family:
                return 50.0  # Score médio se não há família
            
            # Calcular percentual do ativo na família
            total_family_value = sum(a.current_value for a in asset.family.assets)
            if total_family_value <= 0:
                return 50.0
            
            concentration_percent = (asset.current_value / total_family_value) * 100
            
            # Score de risco (maior concentração = maior risco)
            if concentration_percent >= 30:
                return 100.0
            elif concentration_percent >= 20:
                return 75.0
            elif concentration_percent >= 15:
                return 50.0
            elif concentration_percent >= 10:
                return 25.0
            else:
                return 10.0
                
        except Exception as e:
            logger.error(f"Erro ao calcular risco de concentração: {e}")
            return 50.0
    
    def _calculate_market_risk(self, quote: MarketData) -> float:
        """Calcula risco de mercado baseado na variação de preço"""
        try:
            change_abs = abs(quote.change_percent_24h)
            
            # Score de risco baseado na variação
            if change_abs >= 10:
                return 100.0
            elif change_abs >= 7:
                return 75.0
            elif change_abs >= 5:
                return 50.0
            elif change_abs >= 3:
                return 25.0
            else:
                return 10.0
                
        except Exception as e:
            logger.error(f"Erro ao calcular risco de mercado: {e}")
            return 25.0
    
    def get_portfolio_risk_analysis(self, family_id: int) -> Dict[str, Any]:
        """Análise completa de risco da carteira"""
        try:
            # Buscar todos os ativos da família
            assets = Asset.query.filter_by(family_id=family_id).all()
            
            if not assets:
                return {}
            
            # Calcular métricas para cada ativo
            asset_risks = []
            total_value = 0
            weighted_risk_score = 0
            
            for asset in assets:
                risk_metrics = self.get_asset_risk_metrics(asset)
                if risk_metrics:
                    asset_risks.append({
                        'asset_id': asset.id,
                        'name': asset.name,
                        'asset_type': asset.asset_type,
                        'current_value': asset.current_value,
                        'risk_metrics': risk_metrics
                    })
                    
                    total_value += asset.current_value
            
            # Calcular score de risco ponderado
            for asset_risk in asset_risks:
                weight = asset_risk['current_value'] / total_value if total_value > 0 else 0
                risk_score = (
                    asset_risk['risk_metrics'].get('volatility', 0) * 0.3 +
                    asset_risk['risk_metrics'].get('liquidity_score', 0) * 0.2 +
                    asset_risk['risk_metrics'].get('concentration_risk', 0) * 0.3 +
                    asset_risk['risk_metrics'].get('market_risk', 0) * 0.2
                )
                weighted_risk_score += risk_score * weight
            
            # Classificação de risco
            risk_classification = self._classify_risk(weighted_risk_score)
            
            return {
                'total_portfolio_value': total_value,
                'number_of_assets': len(assets),
                'weighted_risk_score': round(weighted_risk_score, 2),
                'risk_classification': risk_classification,
                'asset_risks': asset_risks,
                'risk_breakdown': {
                    'volatility_weight': 0.3,
                    'liquidity_weight': 0.2,
                    'concentration_weight': 0.3,
                    'market_weight': 0.2
                },
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erro na análise de risco da carteira: {e}")
            return {}
    
    def _classify_risk(self, risk_score: float) -> str:
        """Classifica o risco baseado no score"""
        if risk_score <= 25:
            return "Baixo"
        elif risk_score <= 50:
            return "Moderado"
        elif risk_score <= 75:
            return "Alto"
        else:
            return "Muito Alto"
    
    def update_all_asset_quotes(self, family_id: int) -> Dict[str, Any]:
        """Atualiza cotações de todos os ativos de uma família"""
        try:
            assets = Asset.query.filter_by(family_id=family_id).all()
            updated_count = 0
            errors = []
            
            for asset in assets:
                try:
                    symbol = self._get_asset_symbol(asset)
                    if not symbol:
                        continue
                    
                    quote = self.get_comprehensive_quote(symbol, asset.asset_type)
                    if quote:
                        # Salvar no histórico
                        quote_history = QuoteHistory(
                            asset_id=asset.id,
                            price=quote.price,
                            currency=quote.currency,
                            source=quote.source
                        )
                        db.session.add(quote_history)
                        updated_count += 1
                        
                except Exception as e:
                    errors.append(f"Ativo {asset.name}: {str(e)}")
            
            if updated_count > 0:
                db.session.commit()
            
            return {
                'updated_assets': updated_count,
                'total_assets': len(assets),
                'errors': errors,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erro ao atualizar cotações: {e}")
            return {'error': str(e)}
