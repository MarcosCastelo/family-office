"""Tests for report routes"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from flask import Flask

class TestReportRoutes:
    """Test report route functionality"""
    
    def setup_method(self):
        """Setup test data for each test method"""
        # Create a test Flask app with proper JWT configuration
        self.app = Flask(__name__)
        self.app.config.update({
            'TESTING': True,
            'JWT_SECRET_KEY': 'test-secret-key',
            'JWT_TOKEN_LOCATION': ['headers'],
            'JWT_HEADER_NAME': 'Authorization',
            'JWT_HEADER_TYPE': 'Bearer'
        })
        
        self.family_id = 1
        self.user_id = 1
        
        # Mock user and family
        self.mock_user = Mock()
        self.mock_user.id = self.user_id
        self.mock_user.families = [Mock(id=self.family_id)]
        
        self.mock_family = Mock()
        self.mock_family.id = self.family_id
        self.mock_family.name = "Test Family"
    
    def test_generate_portfolio_report_success(self):
        """Test successful portfolio report generation"""
        # Mock the JWT decorator to return the original function
        with patch('app.routes.reports.jwt_required', lambda f: f):
            with self.app.test_request_context():
                from app.routes.reports import generate_portfolio_report
                
                # Mock user query
                with patch('app.routes.reports.User') as mock_user_class:
                    mock_user_class.query.get.return_value = self.mock_user
                    
                    # Mock report service
                    with patch('app.routes.reports.ReportService') as mock_report_service_class:
                        mock_report_service = Mock()
                        mock_report_service_class.return_value = mock_report_service
                        mock_report_service.generate_portfolio_summary.return_value = b"fake_pdf_content"
                        
                        # Mock request context
                        with patch('app.routes.reports.get_jwt_identity') as mock_jwt:
                            mock_jwt.return_value = self.user_id
                            
                            # Mock Flask response
                            with patch('app.routes.reports.send_file') as mock_send_file:
                                mock_send_file.return_value = Mock()
                                
                                # Call the function
                                result = generate_portfolio_report(self.family_id)
                                
                                # Verify report service was called
                                mock_report_service.generate_portfolio_summary.assert_called_once_with(self.family_id)
                                
                                # Verify send_file was called
                                mock_send_file.assert_called_once()
    
    def test_generate_portfolio_report_access_denied(self):
        """Test portfolio report generation with access denied"""
        # Mock the JWT decorator to return the original function
        with patch('app.routes.reports.jwt_required', lambda f: f):
            with self.app.test_request_context():
                from app.routes.reports import generate_portfolio_report
                
                # Mock user without access to family
                mock_user = Mock()
                mock_user.id = self.user_id
                mock_user.families = [Mock(id=999)]  # Different family
                
                with patch('app.routes.reports.User') as mock_user_class:
                    mock_user_class.query.get.return_value = mock_user
                    
                    with patch('app.routes.reports.get_jwt_identity') as mock_jwt:
                        mock_jwt.return_value = self.user_id
                        
                        with patch('app.routes.reports.jsonify') as mock_jsonify:
                            mock_jsonify.return_value = Mock()
                            
                            result = generate_portfolio_report(self.family_id)
                            
                            # Verify access denied response
                            mock_jsonify.assert_called_with({"error": "Acesso negado"})
    
    def test_generate_risk_report_success(self):
        """Test successful risk report generation"""
        # Mock the JWT decorator to return the original function
        with patch('app.routes.reports.jwt_required', lambda f: f):
            with self.app.test_request_context():
                from app.routes.reports import generate_risk_report
                
                # Mock user query
                with patch('app.routes.reports.User') as mock_user_class:
                    mock_user_class.query.get.return_value = self.mock_user
                    
                    # Mock report service
                    with patch('app.routes.reports.ReportService') as mock_report_service_class:
                        mock_report_service = Mock()
                        mock_report_service_class.return_value = mock_report_service
                        mock_report_service.generate_risk_analysis.return_value = b"fake_pdf_content"
                        
                        with patch('app.routes.reports.get_jwt_identity') as mock_jwt:
                            mock_jwt.return_value = self.user_id
                            
                            with patch('app.routes.reports.send_file') as mock_send_file:
                                mock_send_file.return_value = Mock()
                                
                                result = generate_risk_report(self.family_id)
                                
                                mock_report_service.generate_risk_analysis.assert_called_once_with(self.family_id)
                                mock_send_file.assert_called_once()
    
    def test_generate_transaction_report_success(self):
        """Test successful transaction report generation"""
        # Mock the JWT decorator to return the original function
        with patch('app.routes.reports.jwt_required', lambda f: f):
            with self.app.test_request_context():
                from app.routes.reports import generate_transaction_report
                
                # Mock user query
                with patch('app.routes.reports.User') as mock_user_class:
                    mock_user_class.query.get.return_value = self.mock_user
                    
                    # Mock report service
                    with patch('app.routes.reports.ReportService') as mock_report_service_class:
                        mock_report_service = Mock()
                        mock_report_service_class.return_value = mock_report_service
                        mock_report_service.generate_transaction_history.return_value = b"fake_pdf_content"
                        
                        with patch('app.routes.reports.get_jwt_identity') as mock_jwt:
                            mock_jwt.return_value = self.user_id
                            
                            with patch('app.routes.reports.request') as mock_request:
                                mock_request.args.get.side_effect = lambda key, default=None: {
                                    'start_date': '2024-01-01',
                                    'end_date': '2024-01-31'
                                }.get(key, default)
                                
                                with patch('app.routes.reports.send_file') as mock_send_file:
                                    mock_send_file.return_value = Mock()
                                    
                                    result = generate_transaction_report(self.family_id)
                                    
                                    # Verify dates were parsed correctly
                                    mock_report_service.generate_transaction_history.assert_called_once()
                                    call_args = mock_report_service.generate_transaction_history.call_args
                                    assert call_args[0][0] == self.family_id  # family_id
                                    assert call_args[0][1].strftime('%Y-%m-%d') == '2024-01-01'  # start_date
                                    assert call_args[0][2].strftime('%Y-%m-%d') == '2024-01-31'  # end_date
    
    def test_generate_transaction_report_missing_dates(self):
        """Test transaction report generation with missing dates"""
        # Mock the JWT decorator to return the original function
        with patch('app.routes.reports.jwt_required', lambda f: f):
            with self.app.test_request_context():
                from app.routes.reports import generate_transaction_report
                
                # Mock user query
                with patch('app.routes.reports.User') as mock_user_class:
                    mock_user_class.query.get.return_value = self.mock_user
                    
                    with patch('app.routes.reports.get_jwt_identity') as mock_jwt:
                        mock_jwt.return_value = self.user_id
                        
                        with patch('app.routes.reports.request') as mock_request:
                            mock_request.args.get.return_value = None  # Missing dates
                            
                            with patch('app.routes.reports.jsonify') as mock_jsonify:
                                mock_jsonify.return_value = Mock()
                                
                                result = generate_transaction_report(self.family_id)
                                
                                # Verify error response
                                mock_jsonify.assert_called_with({"error": "start_date e end_date são obrigatórios"})
    
    def test_generate_transaction_report_invalid_date_format(self):
        """Test transaction report generation with invalid date format"""
        # Mock the JWT decorator to return the original function
        with patch('app.routes.reports.jwt_required', lambda f: f):
            with self.app.test_request_context():
                from app.routes.reports import generate_transaction_report
                
                # Mock user query
                with patch('app.routes.reports.User') as mock_user_class:
                    mock_user_class.query.get.return_value = self.mock_user
                    
                    with patch('app.routes.reports.get_jwt_identity') as mock_jwt:
                        mock_jwt.return_value = self.user_id
                        
                        with patch('app.routes.reports.request') as mock_request:
                            mock_request.args.get.side_effect = lambda key, default=None: {
                                'start_date': 'invalid-date',
                                'end_date': '2024-01-31'
                            }.get(key, default)
                            
                            with patch('app.routes.reports.jsonify') as mock_jsonify:
                                mock_jsonify.return_value = Mock()
                                
                                result = generate_transaction_report(self.family_id)
                                
                                # Verify error response
                                mock_jsonify.assert_called_with({"error": "Formato de data inválido. Use ISO format (YYYY-MM-DD)"})
    
    def test_generate_fiscal_report_success(self):
        """Test successful fiscal report generation"""
        # Mock the JWT decorator to return the original function
        with patch('app.routes.reports.jwt_required', lambda f: f):
            with self.app.test_request_context():
                from app.routes.reports import generate_fiscal_report
                
                # Mock user query
                with patch('app.routes.reports.User') as mock_user_class:
                    mock_user_class.query.get.return_value = self.mock_user
                    
                    # Mock report service
                    with patch('app.routes.reports.ReportService') as mock_report_service_class:
                        mock_report_service = Mock()
                        mock_report_service_class.return_value = mock_report_service
                        mock_report_service.generate_fiscal_report.return_value = b"fake_pdf_content"
                        
                        with patch('app.routes.reports.get_jwt_identity') as mock_jwt:
                            mock_jwt.return_value = self.user_id
                            
                            with patch('app.routes.reports.request') as mock_request:
                                mock_request.args.get.return_value = '2024'  # Year parameter
                                
                                with patch('app.routes.reports.send_file') as mock_send_file:
                                    mock_send_file.return_value = Mock()
                                    
                                    result = generate_fiscal_report(self.family_id)
                                    
                                    mock_report_service.generate_fiscal_report.assert_called_once_with(self.family_id, 2024)
                                    mock_send_file.assert_called_once()
    
    def test_generate_fiscal_report_default_year(self):
        """Test fiscal report generation with default year"""
        # Mock the JWT decorator to return the original function
        with patch('app.routes.reports.jwt_required', lambda f: f):
            with self.app.test_request_context():
                from app.routes.reports import generate_fiscal_report
                
                # Mock user query
                with patch('app.routes.reports.User') as mock_user_class:
                    mock_user_class.query.get.return_value = self.mock_user
                    
                    # Mock report service
                    with patch('app.routes.reports.ReportService') as mock_report_service_class:
                        mock_report_service = Mock()
                        mock_report_service_class.return_value = mock_report_service
                        mock_report_service.generate_fiscal_report.return_value = b"fake_pdf_content"
                        
                        with patch('app.routes.reports.get_jwt_identity') as mock_jwt:
                            mock_jwt.return_value = self.user_id
                            
                            with patch('app.routes.reports.request') as mock_request:
                                mock_request.args.get.return_value = None  # No year parameter
                                
                                with patch('app.routes.reports.send_file') as mock_send_file:
                                    mock_send_file.return_value = Mock()
                                    
                                    with patch('app.routes.reports.datetime') as mock_datetime:
                                        mock_datetime.now.return_value = Mock(year=2024)
                                        
                                        result = generate_fiscal_report(self.family_id)
                                        
                                        # Verify default year was used
                                        mock_report_service.generate_fiscal_report.assert_called_once_with(self.family_id, 2024)
    
    def test_generate_fiscal_report_invalid_year(self):
        """Test fiscal report generation with invalid year"""
        # Mock the JWT decorator to return the original function
        with patch('app.routes.reports.jwt_required', lambda f: f):
            with self.app.test_request_context():
                from app.routes.reports import generate_fiscal_report
                
                # Mock user query
                with patch('app.routes.reports.User') as mock_user_class:
                    mock_user_class.query.get.return_value = self.mock_user
                    
                    with patch('app.routes.reports.get_jwt_identity') as mock_jwt:
                        mock_jwt.return_value = self.user_id
                        
                        with patch('app.routes.reports.request') as mock_request:
                            mock_request.args.get.return_value = '1800'  # Invalid year
                            
                            with patch('app.routes.reports.jsonify') as mock_jsonify:
                                mock_jsonify.return_value = Mock()
                                
                                result = generate_fiscal_report(self.family_id)
                                
                                # Verify error response
                                mock_jsonify.assert_called_with({"error": "Ano deve estar entre 1900 e 2100"})
    
    def test_get_available_reports_success(self):
        """Test getting available reports successfully"""
        # Mock the JWT decorator to return the original function
        with patch('app.routes.reports.jwt_required', lambda f: f):
            with self.app.test_request_context():
                from app.routes.reports import get_available_reports
                
                # Mock user query
                with patch('app.routes.reports.User') as mock_user_class:
                    mock_user_class.query.get.return_value = self.mock_user
                    
                    with patch('app.routes.reports.get_jwt_identity') as mock_jwt:
                        mock_jwt.return_value = self.user_id
                        
                        with patch('app.routes.reports.jsonify') as mock_jsonify:
                            mock_jsonify.return_value = Mock()
                            
                            result = get_available_reports(self.family_id)
                            
                            # Verify response structure
                            mock_jsonify.assert_called_once()
                            call_args = mock_jsonify.call_args[0][0]
                            
                            assert call_args['family_id'] == self.family_id
                            assert 'reports' in call_args
                            assert len(call_args['reports']) == 4
                            
                            # Verify report types
                            report_types = [r['type'] for r in call_args['reports']]
                            assert 'portfolio' in report_types
                            assert 'risk' in report_types
                            assert 'transactions' in report_types
                            assert 'fiscal' in report_types
    
    def test_get_available_reports_access_denied(self):
        """Test getting available reports with access denied"""
        # Mock the JWT decorator to return the original function
        with patch('app.routes.reports.jwt_required', lambda f: f):
            with self.app.test_request_context():
                from app.routes.reports import get_available_reports
                
                # Mock user without access to family
                mock_user = Mock()
                mock_user.id = self.user_id
                mock_user.families = [Mock(id=999)]  # Different family
                
                with patch('app.routes.reports.User') as mock_user_class:
                    mock_user_class.query.get.return_value = mock_user
                    
                    with patch('app.routes.reports.get_jwt_identity') as mock_jwt:
                        mock_jwt.return_value = self.user_id
                        
                        with patch('app.routes.reports.jsonify') as mock_jsonify:
                            mock_jsonify.return_value = Mock()
                            
                            result = get_available_reports(self.family_id)
                            
                            # Verify access denied response
                            mock_jsonify.assert_called_with({"error": "Acesso negado"})
    
    def test_report_generation_error_handling(self):
        """Test error handling in report generation"""
        # Mock the JWT decorator to return the original function
        with patch('app.routes.reports.jwt_required', lambda f: f):
            with self.app.test_request_context():
                from app.routes.reports import generate_portfolio_report
                
                # Mock user query
                with patch('app.routes.reports.User') as mock_user_class:
                    mock_user_class.query.get.return_value = self.mock_user
                    
                    # Mock report service that raises an error
                    with patch('app.routes.reports.ReportService') as mock_report_service_class:
                        mock_report_service = Mock()
                        mock_report_service_class.return_value = mock_report_service
                        mock_report_service.generate_portfolio_summary.side_effect = Exception("Report generation failed")
                        
                        with patch('app.routes.reports.get_jwt_identity') as mock_jwt:
                            mock_jwt.return_value = self.user_id
                            
                            with patch('app.routes.reports.jsonify') as mock_jsonify:
                                mock_jsonify.return_value = Mock()
                                
                                result = generate_portfolio_report(self.family_id)
                                
                                # Verify error response
                                mock_jsonify.assert_called_with({"error": "Erro ao gerar relatório: Report generation failed"})
