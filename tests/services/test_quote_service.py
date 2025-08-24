"""Tests for QuoteService"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

class TestQuoteService:
    """Test QuoteService functionality"""
    
    def setup_method(self):
        """Setup test data for each test method"""
        # Mock the database session to avoid Flask context issues
        with patch('app.services.quote_service.db') as mock_db:
            mock_db.session = Mock()
            from app.services.quote_service import QuoteService
            self.quote_service = QuoteService()
        
        # Mock asset for testing
        self.mock_asset = Mock()
        self.mock_asset.id = 1
        self.mock_asset.asset_type = "renda_variavel"
        self.mock_asset.details = {"ticker": "PETR4"}
    
    def test_get_yahoo_finance_quote_success(self):
        """Test successful Yahoo Finance quote fetch"""
        # Mock the session.get method directly
        with patch.object(self.quote_service.session, 'get') as mock_get:
            # Mock successful response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'chart': {
                    'result': [{
                        'meta': {
                            'regularMarketPrice': 25.50,
                            'currency': 'BRL'
                        }
                    }]
                }
            }
            
            mock_get.return_value = mock_response
            
            # Test quote fetch
            result = self.quote_service.get_yahoo_finance_quote("PETR4")
            
            assert result is not None
            assert result['symbol'] == "PETR4"
            assert result['price'] == 25.50
            assert result['currency'] == "BRL"
            assert result['source'] == "yahoo_finance"
    
    def test_get_yahoo_finance_quote_failure(self):
        """Test Yahoo Finance quote fetch failure"""
        # Mock failed response
        with patch.object(self.quote_service.session, 'get') as mock_get:
            mock_get.side_effect = Exception("Network error")
            
            result = self.quote_service.get_yahoo_finance_quote("PETR4")
            
            assert result is None
    
    def test_get_coingecko_quote_success(self):
        """Test successful CoinGecko quote fetch"""
        # Mock the session.get method directly
        with patch.object(self.quote_service.session, 'get') as mock_get:
            # Mock successful response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'bitcoin': {
                    'usd': 45000.0,
                    'brl': 225000.0,
                    'usd_24h_change': 2.5
                }
            }
            
            mock_get.return_value = mock_response
            
            # Test quote fetch
            result = self.quote_service.get_coingecko_quote("bitcoin")
            
            assert result is not None
            assert result['symbol'] == "bitcoin"
            assert result['price_usd'] == 45000.0
            assert result['price_brl'] == 225000.0
            assert result['change_24h'] == 2.5
            assert result['source'] == "coingecko"
    
    def test_get_bacen_quote_success(self):
        """Test successful BACEN quote fetch"""
        # Mock the session.get method directly
        with patch.object(self.quote_service.session, 'get') as mock_get:
            # Mock successful response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.text = "USD"
            
            mock_get.return_value = mock_response
            
            # Test quote fetch
            result = self.quote_service.get_bacen_quote("USD")
            
            assert result is not None
            assert result['currency'] == "USD"
            assert result['source'] == "bacen"
    
    def test_get_quote_for_asset_renda_variavel(self):
        """Test quote fetching for renda_variavel asset type"""
        with patch.object(self.quote_service, 'get_yahoo_finance_quote') as mock_yahoo:
            mock_yahoo.return_value = {'price': 25.50, 'source': 'yahoo_finance'}
            
            result = self.quote_service._get_quote_for_asset(self.mock_asset)
            
            assert result is not None
            mock_yahoo.assert_called_once_with("PETR4")
    
    def test_get_quote_for_asset_criptomoeda(self):
        """Test quote fetching for criptomoeda asset type"""
        self.mock_asset.asset_type = "criptomoeda"
        self.mock_asset.details = {"coin_id": "bitcoin"}
        
        with patch.object(self.quote_service, 'get_coingecko_quote') as mock_coingecko:
            mock_coingecko.return_value = {'price_usd': 45000.0, 'source': 'coingecko'}
            
            result = self.quote_service._get_quote_for_asset(self.mock_asset)
            
            assert result is not None
            mock_coingecko.assert_called_once_with("bitcoin")
    
    def test_get_quote_for_asset_moeda_estrangeira(self):
        """Test quote fetching for moeda_estrangeira asset type"""
        self.mock_asset.asset_type = "moeda_estrangeira"
        self.mock_asset.details = {"currency": "EUR"}
        
        with patch.object(self.quote_service, 'get_bacen_quote') as mock_bacen:
            mock_bacen.return_value = {'rate': 5.5, 'source': 'bacen'}
            
            result = self.quote_service._get_quote_for_asset(self.mock_asset)
            
            assert result is not None
            mock_bacen.assert_called_once_with("EUR")
    
    def test_get_quote_for_asset_unknown_type(self):
        """Test quote fetching for unknown asset type"""
        self.mock_asset.asset_type = "unknown_type"
        
        result = self.quote_service._get_quote_for_asset(self.mock_asset)
        
        assert result is None
    
    def test_update_asset_quotes_success(self):
        """Test successful bulk quote update"""
        # Mock the Asset class
        with patch('app.services.quote_service.Asset') as mock_asset_class:
            # Mock assets
            mock_assets = [self.mock_asset]
            mock_asset_class.query.filter_by.return_value.all.return_value = mock_assets
            
            with patch.object(self.quote_service, '_get_quote_for_asset') as mock_get_quote:
                with patch.object(self.quote_service, '_save_quote_history') as mock_save:
                    mock_get_quote.return_value = {'price': 25.50, 'source': 'yahoo_finance'}
                    
                    result = self.quote_service.update_asset_quotes()
                    
                    assert result['updated'] == 1
                    assert result['errors'] == 0
                    assert result['total'] == 1
                    mock_save.assert_called_once()
    
    def test_update_asset_quotes_with_errors(self):
        """Test bulk quote update with some errors"""
        # Mock the Asset class
        with patch('app.services.quote_service.Asset') as mock_asset_class:
            # Mock assets
            mock_assets = [self.mock_asset]
            mock_asset_class.query.filter_by.return_value.all.return_value = mock_assets
            
            with patch.object(self.quote_service, '_get_quote_for_asset') as mock_get_quote:
                mock_get_quote.return_value = None  # Simulate error
                
                result = self.quote_service.update_asset_quotes()
                
                assert result['updated'] == 0
                assert result['errors'] == 1
                assert result['total'] == 1
    
    def test_get_asset_current_price_success(self):
        """Test getting current asset price"""
        # Mock the QuoteHistory class
        with patch('app.services.quote_service.QuoteHistory') as mock_quote_history_class:
            # Mock quote
            mock_quote = Mock()
            mock_quote.price = 25.50
            mock_quote_history_class.query.filter_by.return_value.order_by.return_value.first.return_value = mock_quote
            
            result = self.quote_service.get_asset_current_price(1)
            
            assert result == 25.50
    
    def test_get_asset_current_price_no_quotes(self):
        """Test getting current asset price when no quotes exist"""
        # Mock the QuoteHistory class
        with patch('app.services.quote_service.QuoteHistory') as mock_quote_history_class:
            mock_quote_history_class.query.filter_by.return_value.order_by.return_value.first.return_value = None
            
            result = self.quote_service.get_asset_current_price(1)
            
            assert result is None
    
    def test_get_asset_price_history_success(self):
        """Test getting asset price history"""
        # Mock the QuoteHistory class
        with patch('app.services.quote_service.QuoteHistory') as mock_quote_history_class:
            # Mock quotes
            mock_quotes = [
                Mock(price=25.50, timestamp=datetime.now(), source='yahoo_finance'),
                Mock(price=26.00, timestamp=datetime.now(), source='yahoo_finance')
            ]
            mock_quote_history_class.query.filter.return_value.order_by.return_value.all.return_value = mock_quotes
            
            result = self.quote_service.get_asset_price_history(1, days=30)
            
            assert len(result) == 2
            assert result[0]['price'] == 25.50
            assert result[1]['price'] == 26.00
            assert all('source' in quote for quote in result)
