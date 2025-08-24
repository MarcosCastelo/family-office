"""Quote service for fetching asset prices from external APIs"""
import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from app.config.extensions import db
from app.models.asset import Asset
from app.models.quote_history import QuoteHistory

logger = logging.getLogger(__name__)

class QuoteService:
    """Service for managing asset quotes and price updates"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'FamilyOffice/1.0'
        })
    
    def get_yahoo_finance_quote(self, symbol: str) -> Optional[Dict]:
        """Get quote from Yahoo Finance API"""
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
            params = {
                'range': '1d',
                'interval': '1m',
                'includePrePost': False
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
                result = data['chart']['result'][0]
                if 'meta' in result and 'regularMarketPrice' in result['meta']:
                    return {
                        'symbol': symbol,
                        'price': result['meta']['regularMarketPrice'],
                        'currency': result['meta']['currency'],
                        'timestamp': datetime.now(),
                        'source': 'yahoo_finance'
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Error fetching Yahoo Finance quote for {symbol}: {e}")
            return None
    
    def get_coingecko_quote(self, coin_id: str) -> Optional[Dict]:
        """Get cryptocurrency quote from CoinGecko API"""
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price"
            params = {
                'ids': coin_id,
                'vs_currencies': 'usd,brl',
                'include_24hr_change': True
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if coin_id in data and 'usd' in data[coin_id]:
                return {
                    'symbol': coin_id,
                    'price_usd': data[coin_id]['usd'],
                    'price_brl': data[coin_id]['brl'],
                    'change_24h': data[coin_id].get('usd_24h_change', 0),
                    'timestamp': datetime.now(),
                    'source': 'coingecko'
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error fetching CoinGecko quote for {coin_id}: {e}")
            return None
    
    def get_bacen_quote(self, currency: str = 'USD') -> Optional[Dict]:
        """Get currency quote from Banco Central do Brasil"""
        try:
            # API do Banco Central para cotações de moedas
            url = f"https://www.bcb.gov.br/api/servico/sitebcb/indicadorCambio"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse XML response (simplificado)
            # Em produção, usar biblioteca XML apropriada
            if currency in response.text:
                # Extrair cotação (implementação simplificada)
                return {
                    'currency': currency,
                    'rate': 5.0,  # Placeholder - implementar parser real
                    'timestamp': datetime.now(),
                    'source': 'bacen'
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error fetching BACEN quote for {currency}: {e}")
            return None
    
    def update_asset_quotes(self, family_id: Optional[int] = None) -> Dict[str, int]:
        """Update quotes for all assets or specific family"""
        try:
            # Query assets to update
            query = Asset.query
            if family_id:
                query = query.filter_by(family_id=family_id)
            
            assets = query.all()
            updated_count = 0
            error_count = 0
            
            for asset in assets:
                try:
                    quote_data = self._get_quote_for_asset(asset)
                    if quote_data:
                        self._save_quote_history(asset, quote_data)
                        updated_count += 1
                    else:
                        error_count += 1
                        
                except Exception as e:
                    logger.error(f"Error updating quote for asset {asset.id}: {e}")
                    error_count += 1
            
            return {
                'updated': updated_count,
                'errors': error_count,
                'total': len(assets)
            }
            
        except Exception as e:
            logger.error(f"Error in bulk quote update: {e}")
            return {'updated': 0, 'errors': 1, 'total': 0}
    
    def _get_quote_for_asset(self, asset: Asset) -> Optional[Dict]:
        """Get appropriate quote based on asset type"""
        asset_type = asset.asset_type
        
        if asset_type == 'renda_variavel':
            # Buscar ticker dos detalhes
            ticker = asset.details.get('ticker') if asset.details else None
            if ticker:
                return self.get_yahoo_finance_quote(ticker)
                
        elif asset_type == 'criptomoeda':
            # Buscar coin ID dos detalhes
            coin_id = asset.details.get('coin_id') if asset.details else None
            if coin_id:
                return self.get_coingecko_quote(coin_id)
                
        elif asset_type == 'moeda_estrangeira':
            # Buscar cotação de moeda
            currency = asset.details.get('currency') if asset.details else 'USD'
            return self.get_bacen_quote(currency)
        
        return None
    
    def _save_quote_history(self, asset: Asset, quote_data: Dict):
        """Save quote to history table"""
        try:
            quote = QuoteHistory(
                asset_id=asset.id,
                price=quote_data.get('price', quote_data.get('price_usd', 0)),
                currency=quote_data.get('currency', 'USD'),
                source=quote_data['source'],
                timestamp=quote_data['timestamp']
            )
            
            db.session.add(quote)
            db.session.commit()
            
        except Exception as e:
            logger.error(f"Error saving quote history: {e}")
            db.session.rollback()
    
    def get_asset_current_price(self, asset_id: int) -> Optional[float]:
        """Get current price for an asset"""
        try:
            latest_quote = QuoteHistory.query.filter_by(
                asset_id=asset_id
            ).order_by(QuoteHistory.timestamp.desc()).first()
            
            return latest_quote.price if latest_quote else None
            
        except Exception as e:
            logger.error(f"Error getting current price for asset {asset_id}: {e}")
            return None
    
    def get_asset_price_history(self, asset_id: int, days: int = 30) -> List[Dict]:
        """Get price history for an asset"""
        try:
            since_date = datetime.now() - timedelta(days=days)
            
            quotes = QuoteHistory.query.filter(
                QuoteHistory.asset_id == asset_id,
                QuoteHistory.timestamp >= since_date
            ).order_by(QuoteHistory.timestamp.asc()).all()
            
            return [
                {
                    'price': quote.price,
                    'timestamp': quote.timestamp.isoformat(),
                    'source': quote.source
                }
                for quote in quotes
            ]
            
        except Exception as e:
            logger.error(f"Error getting price history for asset {asset_id}: {e}")
            return []
