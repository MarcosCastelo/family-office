"""Tests for ReportService"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

class TestReportService:
    """Test ReportService functionality"""
    
    def setup_method(self):
        """Setup test data for each test method"""
        # Mock the database session to avoid Flask context issues
        with patch('app.services.report_service.db') as mock_db:
            mock_db.session = Mock()
            from app.services.report_service import ReportService
            self.report_service = ReportService()
        
        # Mock family
        self.mock_family = Mock()
        self.mock_family.id = 1
        self.mock_family.name = "Test Family"
        self.mock_family.cash_balance = 10000.0
        
        # Mock assets
        self.mock_asset1 = Mock()
        self.mock_asset1.id = 1
        self.mock_asset1.name = "Test Asset 1"
        self.mock_asset1.asset_type = "renda_fixa"
        self.mock_asset1.current_value = 5000.0
        self.mock_asset1.current_quantity = 100.0
        
        self.mock_asset2 = Mock()
        self.mock_asset2.id = 2
        self.mock_asset2.name = "Test Asset 2"
        self.mock_asset2.asset_type = "renda_variavel"
        self.mock_asset2.current_value = 3000.0
        self.mock_asset2.current_quantity = 50.0
        
        self.mock_family.assets = [self.mock_asset1, self.mock_asset2]
    
    def test_generate_portfolio_summary_success(self):
        """Test successful portfolio summary generation"""
        # Mock family properties
        self.mock_family.total_invested = 8000.0
        self.mock_family.total_patrimony = 18000.0
        self.mock_family.asset_allocation = {
            "renda_fixa": 5000.0,
            "renda_variavel": 3000.0
        }
        
        with patch('app.services.report_service.Family') as mock_family_class:
            mock_family_class.query.get.return_value = self.mock_family
            
            with patch.object(self.report_service, '_html_to_pdf') as mock_html_to_pdf:
                mock_html_to_pdf.return_value = b"fake_pdf_content"
                
                result = self.report_service.generate_portfolio_summary(1)
                
                assert result == b"fake_pdf_content"
                mock_html_to_pdf.assert_called_once()
    
    def test_generate_portfolio_summary_family_not_found(self):
        """Test portfolio summary generation with non-existent family"""
        with patch('app.services.report_service.Family') as mock_family_class:
            mock_family_class.query.get.return_value = None
            
            with pytest.raises(ValueError, match="Family 1 not found"):
                self.report_service.generate_portfolio_summary(1)
    
    def test_generate_risk_analysis_success(self):
        """Test successful risk analysis generation"""
        with patch('app.services.report_service.Family') as mock_family_class:
            mock_family_class.query.get.return_value = self.mock_family
            
            with patch.object(self.report_service, '_html_to_pdf') as mock_html_to_pdf:
                mock_html_to_pdf.return_value = b"fake_pdf_content"
                
                result = self.report_service.generate_risk_analysis(1)
                
                assert result == b"fake_pdf_content"
                mock_html_to_pdf.assert_called_once()
    
    def test_get_portfolio_data_success(self):
        """Test getting portfolio data successfully"""
        # Mock family properties
        self.mock_family.total_invested = 8000.0
        self.mock_family.total_patrimony = 18000.0
        self.mock_family.asset_allocation = {
            "renda_fixa": 5000.0,
            "renda_variavel": 3000.0
        }
        
        result = self.report_service._get_portfolio_data(self.mock_family)
        
        assert result['total_value'] == 18000.0
        assert result['total_invested'] == 8000.0
        assert result['cash_balance'] == 10000.0
        assert result['asset_count'] == 2
        assert 'renda_fixa' in result['allocation']
        assert 'renda_variavel' in result['allocation']
        assert len(result['top_assets']) == 2
    
    def test_calculate_performance_metrics_success(self):
        """Test calculating performance metrics successfully"""
        # Mock family with positive returns
        self.mock_family.total_invested = 8000.0
        self.mock_family.total_patrimony = 10000.0
        
        result = self.report_service._calculate_performance_metrics(self.mock_family)
        
        assert result['total_return_percent'] == 25.0  # (10000-8000)/8000 * 100
        assert result['absolute_return'] == 2000.0
        assert result['cash_ratio'] == 100.0  # 10000/10000 * 100
    
    def test_calculate_performance_metrics_no_investment(self):
        """Test calculating performance metrics with no investment"""
        self.mock_family.total_invested = 0.0
        self.mock_family.total_patrimony = 10000.0
        
        result = self.report_service._calculate_performance_metrics(self.mock_family)
        
        assert result['total_return_percent'] == 0.0
        assert result['absolute_return'] == 10000.0
        assert result['cash_ratio'] == 100.0
    
    def test_calculate_concentration_risk_success(self):
        """Test calculating concentration risk successfully"""
        result = self.report_service._calculate_concentration_risk(self.mock_family)
        
        # Should return a value between 0 and 100
        assert 0 <= result <= 100
    
    def test_calculate_concentration_risk_no_assets(self):
        """Test calculating concentration risk with no assets"""
        self.mock_family.assets = []
        
        result = self.report_service._calculate_concentration_risk(self.mock_family)
        
        assert result == 0.0
    
    def test_calculate_liquidity_risk_success(self):
        """Test calculating liquidity risk successfully"""
        result = self.report_service._calculate_liquidity_risk(self.mock_family)
        
        # Should return a value between 0 and 100
        assert 0 <= result <= 100
    
    def test_calculate_volatility_risk_success(self):
        """Test calculating volatility risk successfully"""
        result = self.report_service._calculate_volatility_risk(self.mock_family)
        
        # Should return a value between 0 and 100
        assert 0 <= result <= 100
    
    @patch('app.services.report_service.HTML')
    def test_html_to_pdf_success(self, mock_html_class):
        """Test successful HTML to PDF conversion"""
        mock_html = Mock()
        mock_html_class.return_value = mock_html
        mock_html.write_pdf.return_value = b"fake_pdf_content"
        
        html_content = "<html><body>Test</body></html>"
        result = self.report_service._html_to_pdf(html_content)
        
        assert result == b"fake_pdf_content"
        mock_html_class.assert_called_once_with(string=html_content)
        mock_html.write_pdf.assert_called_once()
    
    @patch('app.services.report_service.HTML')
    def test_html_to_pdf_error(self, mock_html_class):
        """Test HTML to PDF conversion with error"""
        mock_html_class.side_effect = Exception("PDF generation error")
        
        html_content = "<html><body>Test</body></html>"
        
        with pytest.raises(Exception, match="PDF generation error"):
            self.report_service._html_to_pdf(html_content)
