"""Asset validation service for robust ticker and field validation"""
import re
from typing import Dict, List, Tuple, Optional
from datetime import datetime

class AssetValidationService:
    """Service for validating asset data and ticker formats"""
    
    # Supported stock exchanges and their suffixes
    STOCK_EXCHANGES = {
        'B3': '.SA',      # Brazilian Stock Exchange
        'NYSE': '',       # New York Stock Exchange
        'NASDAQ': '',     # NASDAQ
        'LSE': '.L',      # London Stock Exchange
        'TSE': '.T',      # Tokyo Stock Exchange
        'ASX': '.AX',     # Australian Stock Exchange
        'TSX': '.TO',     # Toronto Stock Exchange
    }
    
    # Supported cryptocurrencies
    SUPPORTED_CRYPTOS = [
        'bitcoin', 'ethereum', 'binancecoin', 'cardano', 'solana',
        'polkadot', 'dogecoin', 'avalanche-2', 'chainlink', 'polygon'
    ]
    
    # Supported currencies
    SUPPORTED_CURRENCIES = ['USD', 'EUR', 'GBP', 'JPY', 'CHF', 'CAD', 'AUD', 'CNY', 'BRL']
    
    # Supported fixed income indices
    SUPPORTED_INDICES = ['CDI', 'IPCA', 'SELIC', 'IGPM', 'LIBOR', 'EURIBOR', 'SOFR']
    
    @classmethod
    def validate_ticker(cls, ticker: str, asset_type: str, exchange: str = 'B3') -> Tuple[bool, str]:
        """
        Validate ticker format based on asset type and exchange
        
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not ticker:
            return False, "Ticker é obrigatório"
        
        ticker = ticker.upper().strip()
        
        if asset_type == "renda_variavel":
            return cls._validate_stock_ticker(ticker, exchange)
        elif asset_type == "criptomoeda":
            return cls._validate_crypto_ticker(ticker)
        elif asset_type == "moeda_estrangeira":
            return cls._validate_currency_ticker(ticker)
        
        return True, ""
    
    @classmethod
    def _validate_stock_ticker(cls, ticker: str, exchange: str) -> Tuple[bool, str]:
        """Validate stock ticker format"""
        if exchange == 'B3':
            # Brazilian stocks: 4 letters + numbers + .SA
            if not re.match(r'^[A-Z]{4}\d+\.SA$', ticker):
                return False, "Ticker brasileiro deve seguir formato: PETR4.SA, VALE3.SA, etc."
        elif exchange == 'NYSE' or exchange == 'NASDAQ':
            # US stocks: letters only, no special characters
            if not re.match(r'^[A-Z]+$', ticker):
                return False, "Ticker americano deve conter apenas letras: AAPL, GOOGL, MSFT, etc."
        elif exchange == 'LSE':
            # London stocks: letters + .L
            if not re.match(r'^[A-Z]+\.L$', ticker):
                return False, "Ticker londrino deve terminar com .L: BP.L, HSBA.L, etc."
        
        return True, ""
    
    @classmethod
    def _validate_crypto_ticker(cls, ticker: str) -> Tuple[bool, str]:
        """Validate cryptocurrency ticker"""
        ticker_lower = ticker.lower()
        
        # Check if it's a supported crypto
        if ticker_lower not in cls.SUPPORTED_CRYPTOS:
            return False, f"Criptomoeda não suportada. Use: {', '.join(cls.SUPPORTED_CRYPTOS[:5])}..."
        
        return True, ""
    
    @classmethod
    def _validate_currency_ticker(cls, ticker: str) -> Tuple[bool, str]:
        """Validate currency ticker"""
        if ticker not in cls.SUPPORTED_CURRENCIES:
            return False, f"Moeda não suportada. Use: {', '.join(cls.SUPPORTED_CURRENCIES)}"
        
        return True, ""
    
    @classmethod
    def validate_fixed_income_fields(cls, details: Dict) -> Tuple[bool, str]:
        """Validate fixed income specific fields"""
        indexador = details.get('indexador')
        vencimento = details.get('vencimento')
        
        if not indexador:
            return False, "Indexador é obrigatório para renda fixa"
        
        if indexador not in cls.SUPPORTED_INDICES:
            return False, f"Indexador não suportado. Use: {', '.join(cls.SUPPORTED_INDICES)}"
        
        if not vencimento:
            return False, "Data de vencimento é obrigatória para renda fixa"
        
        try:
            if isinstance(vencimento, str):
                vencimento_date = datetime.strptime(vencimento, '%Y-%m-%d').date()
            else:
                vencimento_date = vencimento
            
            if vencimento_date <= datetime.now().date():
                return False, "Data de vencimento deve ser futura"
        except (ValueError, TypeError):
            return False, "Data de vencimento deve estar no formato YYYY-MM-DD"
        
        return True, ""
    
    @classmethod
    def normalize_ticker(cls, ticker: str, asset_type: str, exchange: str = 'B3') -> str:
        """Normalize ticker to standard format"""
        if not ticker:
            return ticker
        
        ticker = ticker.upper().strip()
        
        if asset_type == "renda_variavel":
            if exchange == 'B3' and not ticker.endswith('.SA'):
                # Add .SA suffix for Brazilian stocks if missing
                if re.match(r'^[A-Z]{4}\d+$', ticker):
                    ticker += '.SA'
            elif exchange in ['NYSE', 'NASDAQ'] and ticker.endswith('.SA'):
                # Remove .SA suffix for US stocks
                ticker = ticker.replace('.SA', '')
        
        elif asset_type == "criptomoeda":
            # Map common acronyms to full names
            crypto_mapping = {
                'BTC': 'bitcoin',
                'ETH': 'ethereum',
                'BNB': 'binancecoin',
                'ADA': 'cardano',
                'SOL': 'solana',
                'DOT': 'polkadot',
                'DOGE': 'dogecoin',
                'AVAX': 'avalanche-2',
                'LINK': 'chainlink',
                'MATIC': 'polygon'
            }
            ticker = crypto_mapping.get(ticker, ticker.lower())
        
        return ticker
    
    @classmethod
    def get_suggested_tickers(cls, asset_type: str, exchange: str = 'B3') -> List[str]:
        """Get suggested tickers for asset type and exchange"""
        if asset_type == "renda_variavel":
            if exchange == 'B3':
                return ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'BBDC4.SA', 'ABEV3.SA']
            elif exchange == 'NYSE':
                return ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
            elif exchange == 'NASDAQ':
                return ['NVDA', 'META', 'NFLX', 'ADBE', 'PYPL']
        elif asset_type == "criptomoeda":
            return ['bitcoin', 'ethereum', 'binancecoin', 'cardano', 'solana']
        elif asset_type == "moeda_estrangeira":
            return ['USD', 'EUR', 'GBP', 'JPY', 'CHF']
        
        return []
    
    @classmethod
    def validate_asset_name(cls, name: str) -> Tuple[bool, str]:
        """Validate asset name"""
        if not name or len(name.strip()) < 2:
            return False, "Nome do ativo deve ter pelo menos 2 caracteres"
        
        if len(name.strip()) > 100:
            return False, "Nome do ativo deve ter no máximo 100 caracteres"
        
        # Check for invalid characters
        if re.search(r'[<>:"/\\|?*]', name):
            return False, "Nome do ativo contém caracteres inválidos"
        
        return True, ""
