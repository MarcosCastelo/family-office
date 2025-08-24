"""Tests for SuitabilityProfile model"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

class TestSuitabilityProfile:
    """Test SuitabilityProfile model functionality"""
    
    def setup_method(self):
        """Setup test data for each test method"""
        self.profile_data = {
            'user_id': 1,
            'family_id': 1,
            'risk_tolerance': 'moderate',
            'investment_horizon': 'medium_term',
            'liquidity_needs': 'medium',
            'annual_income': 100000.0,
            'net_worth': 500000.0,
            'investment_experience': 'intermediate',
            'primary_goal': 'growth',
            'secondary_goals': ['income', 'capital_preservation'],
            'investment_constraints': ['ethical'],
            'preferred_asset_classes': ['renda_fixa', 'renda_variavel'],
            'excluded_asset_classes': ['criptomoeda']
        }
    
    def test_create_suitability_profile(self):
        """Test creating a suitability profile"""
        # Mock the model to avoid database issues
        with patch('app.models.suitability.db') as mock_db:
            mock_db.Model = Mock()
            mock_db.Column = Mock()
            mock_db.Integer = Mock()
            mock_db.String = Mock()
            mock_db.Float = Mock()
            mock_db.Boolean = Mock()
            mock_db.DateTime = Mock()
            mock_db.ForeignKey = Mock()
            mock_db.relationship = Mock()
            mock_db.func = Mock()
            mock_db.func.now = Mock()
            
            from app.models.suitability import SuitabilityProfile
            
            profile = SuitabilityProfile(**self.profile_data)
            
            assert profile.user_id == 1
            assert profile.family_id == 1
            assert profile.risk_tolerance == 'moderate'
            assert profile.investment_horizon == 'medium_term'
            assert profile.liquidity_needs == 'medium'
            assert profile.annual_income == 100000.0
            assert profile.net_worth == 500000.0
            assert profile.investment_experience == 'intermediate'
            assert profile.primary_goal == 'growth'
            assert profile.secondary_goals == ['income', 'capital_preservation']
            assert profile.investment_constraints == ['ethical']
            assert profile.preferred_asset_classes == ['renda_fixa', 'renda_variavel']
            assert profile.excluded_asset_classes == ['criptomoeda']
            assert profile.is_active is True
    
    def test_risk_level_description_conservative(self):
        """Test risk level description for conservative profile"""
        with patch('app.models.suitability.db') as mock_db:
            mock_db.Model = Mock()
            mock_db.Column = Mock()
            mock_db.Integer = Mock()
            mock_db.String = Mock()
            mock_db.Float = Mock()
            mock_db.Boolean = Mock()
            mock_db.DateTime = Mock()
            mock_db.ForeignKey = Mock()
            mock_db.relationship = Mock()
            mock_db.func = Mock()
            mock_db.func.now = Mock()
            
            from app.models.suitability import SuitabilityProfile
            
            profile = SuitabilityProfile(**self.profile_data)
            profile.overall_risk_score = 25
            
            assert profile.risk_level_description == "Baixo Risco"
    
    def test_risk_level_description_moderate(self):
        """Test risk level description for moderate profile"""
        with patch('app.models.suitability.db') as mock_db:
            mock_db.Model = Mock()
            mock_db.Column = Mock()
            mock_db.Integer = Mock()
            mock_db.String = Mock()
            mock_db.Float = Mock()
            mock_db.Boolean = Mock()
            mock_db.DateTime = Mock()
            mock_db.ForeignKey = Mock()
            mock_db.relationship = Mock()
            mock_db.func = Mock()
            mock_db.func.now = Mock()
            
            from app.models.suitability import SuitabilityProfile
            
            profile = SuitabilityProfile(**self.profile_data)
            profile.overall_risk_score = 45
            
            assert profile.risk_level_description == "Médio Risco"
    
    def test_risk_level_description_aggressive(self):
        """Test risk level description for aggressive profile"""
        with patch('app.models.suitability.db') as mock_db:
            mock_db.Model = Mock()
            mock_db.Column = Mock()
            mock_db.Integer = Mock()
            mock_db.String = Mock()
            mock_db.Float = Mock()
            mock_db.Boolean = Mock()
            mock_db.DateTime = Mock()
            mock_db.ForeignKey = Mock()
            mock_db.relationship = Mock()
            mock_db.func = Mock()
            mock_db.func.now = Mock()
            
            from app.models.suitability import SuitabilityProfile
            
            profile = SuitabilityProfile(**self.profile_data)
            profile.overall_risk_score = 75
            
            assert profile.risk_level_description == "Alto Risco"
    
    def test_recommended_asset_allocation_conservative(self):
        """Test recommended asset allocation for conservative profile"""
        with patch('app.models.suitability.db') as mock_db:
            mock_db.Model = Mock()
            mock_db.Column = Mock()
            mock_db.Integer = Mock()
            mock_db.String = Mock()
            mock_db.Float = Mock()
            mock_db.Boolean = Mock()
            mock_db.DateTime = Mock()
            mock_db.ForeignKey = Mock()
            mock_db.relationship = Mock()
            mock_db.func = Mock()
            mock_db.func.now = Mock()
            
            from app.models.suitability import SuitabilityProfile
            
            profile = SuitabilityProfile(**self.profile_data)
            profile.risk_tolerance = 'conservative'
            
            allocation = profile.recommended_asset_allocation
            
            assert allocation['renda_fixa'] == 70
            assert allocation['renda_variavel'] == 20
            assert allocation['fundo_imobiliario'] == 10
    
    def test_recommended_asset_allocation_moderate(self):
        """Test recommended asset allocation for moderate profile"""
        with patch('app.models.suitability.db') as mock_db:
            mock_db.Model = Mock()
            mock_db.Column = Mock()
            mock_db.Integer = Mock()
            mock_db.String = Mock()
            mock_db.Float = Mock()
            mock_db.DateTime = Mock()
            mock_db.ForeignKey = Mock()
            mock_db.relationship = Mock()
            mock_db.func = Mock()
            mock_db.func.now = Mock()
            
            from app.models.suitability import SuitabilityProfile
            
            profile = SuitabilityProfile(**self.profile_data)
            profile.risk_tolerance = 'moderate'
            
            allocation = profile.recommended_asset_allocation
            
            assert allocation['renda_fixa'] == 50
            assert allocation['renda_variavel'] == 40
            assert allocation['fundo_imobiliario'] == 10
    
    def test_recommended_asset_allocation_aggressive(self):
        """Test recommended asset allocation for aggressive profile"""
        with patch('app.models.suitability.db') as mock_db:
            mock_db.Model = Mock()
            mock_db.Column = Mock()
            mock_db.Integer = Mock()
            mock_db.String = Mock()
            mock_db.Float = Mock()
            mock_db.Boolean = Mock()
            mock_db.DateTime = Mock()
            mock_db.ForeignKey = Mock()
            mock_db.relationship = Mock()
            mock_db.func = Mock()
            mock_db.func.now = Mock()
            
            from app.models.suitability import SuitabilityProfile
            
            profile = SuitabilityProfile(**self.profile_data)
            profile.risk_tolerance = 'aggressive'
            
            allocation = profile.recommended_asset_allocation
            
            assert allocation['renda_fixa'] == 30
            assert allocation['renda_variavel'] == 60
            assert allocation['fundo_imobiliario'] == 10
    
    def test_get_compatibility_score_perfect_match(self):
        """Test compatibility score calculation for perfect match"""
        with patch('app.models.suitability.db') as mock_db:
            mock_db.Model = Mock()
            mock_db.Column = Mock()
            mock_db.Integer = Mock()
            mock_db.String = Mock()
            mock_db.Float = Mock()
            mock_db.Boolean = Mock()
            mock_db.DateTime = Mock()
            mock_db.ForeignKey = Mock()
            mock_db.relationship = Mock()
            mock_db.func = Mock()
            mock_db.func.now = Mock()
            
            from app.models.suitability import SuitabilityProfile
            
            profile = SuitabilityProfile(**self.profile_data)
            profile.risk_tolerance = 'moderate'
            
            current_allocation = {
                'renda_fixa': 50,
                'renda_variavel': 40,
                'fundo_imobiliario': 10
            }
            
            score = profile.get_compatibility_score(current_allocation)
            
            assert score == 100.0  # Perfect match
    
    def test_get_compatibility_score_partial_match(self):
        """Test compatibility score calculation for partial match"""
        with patch('app.models.suitability.db') as mock_db:
            mock_db.Model = Mock()
            mock_db.Column = Mock()
            mock_db.Integer = Mock()
            mock_db.String = Mock()
            mock_db.Float = Mock()
            mock_db.DateTime = Mock()
            mock_db.ForeignKey = Mock()
            mock_db.relationship = Mock()
            mock_db.func = Mock()
            mock_db.func.now = Mock()
            
            from app.models.suitability import SuitabilityProfile
            
            profile = SuitabilityProfile(**self.profile_data)
            profile.risk_tolerance = 'moderate'
            
            current_allocation = {
                'renda_fixa': 60,  # 10% difference
                'renda_variavel': 35,  # 5% difference
                'fundo_imobiliario': 5  # 5% difference
            }
            
            score = profile.get_compatibility_score(current_allocation)
            
            # Weighted average: (90*50 + 95*40 + 95*10) / 100 = 91.5
            assert score == 91.5
    
    def test_get_compatibility_score_no_match(self):
        """Test compatibility score calculation for no match"""
        with patch('app.models.suitability.db') as mock_db:
            mock_db.Model = Mock()
            mock_db.Column = Mock()
            mock_db.Integer = Mock()
            mock_db.String = Mock()
            mock_db.Float = Mock()
            mock_db.DateTime = Mock()
            mock_db.ForeignKey = Mock()
            mock_db.relationship = Mock()
            mock_db.func = Mock()
            mock_db.func.now = Mock()
            
            from app.models.suitability import SuitabilityProfile
            
            profile = SuitabilityProfile(**self.profile_data)
            profile.risk_tolerance = 'conservative'
            
            current_allocation = {
                'renda_fixa': 30,  # 40% difference
                'renda_variavel': 60,  # 40% difference
                'fundo_imobiliario': 10  # 0% difference
            }
            
            score = profile.get_compatibility_score(current_allocation)
            
            # Weighted average: (60*70 + 60*20 + 100*10) / 100 = 64.0
            assert score == 64.0
    
    def test_get_compatibility_score_empty_allocation(self):
        """Test compatibility score calculation for empty allocation"""
        with patch('app.models.suitability.db') as mock_db:
            mock_db.Model = Mock()
            mock_db.Column = Mock()
            mock_db.Integer = Mock()
            mock_db.String = Mock()
            mock_db.Float = Mock()
            mock_db.Boolean = Mock()
            mock_db.DateTime = Mock()
            mock_db.ForeignKey = Mock()
            mock_db.relationship = Mock()
            mock_db.func = Mock()
            mock_db.func.now = Mock()
            
            from app.models.suitability import SuitabilityProfile
            
            profile = SuitabilityProfile(**self.profile_data)
            
            score = profile.get_compatibility_score({})
            
            assert score == 0.0
    
    def test_to_dict(self):
        """Test converting profile to dictionary"""
        with patch('app.models.suitability.db') as mock_db:
            mock_db.Model = Mock()
            mock_db.Column = Mock()
            mock_db.Integer = Mock()
            mock_db.String = Mock()
            mock_db.Float = Mock()
            mock_db.Boolean = Mock()
            mock_db.DateTime = Mock()
            mock_db.ForeignKey = Mock()
            mock_db.relationship = Mock()
            mock_db.func = Mock()
            mock_db.func.now = Mock()
            
            from app.models.suitability import SuitabilityProfile
            
            profile = SuitabilityProfile(**self.profile_data)
            profile.overall_risk_score = 50
            
            profile_dict = profile.to_dict()
            
            assert profile_dict['user_id'] == 1
            assert profile_dict['family_id'] == 1
            assert profile_dict['risk_tolerance'] == 'moderate'
            assert profile_dict['overall_risk_score'] == 50
            assert profile_dict['risk_level_description'] == "Médio Risco"
            assert 'recommended_asset_allocation' in profile_dict
            assert profile_dict['is_active'] is True
    
    def test_repr(self):
        """Test string representation of profile"""
        with patch('app.models.suitability.db') as mock_db:
            mock_db.Model = Mock()
            mock_db.Column = Mock()
            mock_db.Integer = Mock()
            mock_db.String = Mock()
            mock_db.Float = Mock()
            mock_db.Boolean = Mock()
            mock_db.DateTime = Mock()
            mock_db.ForeignKey = Mock()
            mock_db.relationship = Mock()
            mock_db.func = Mock()
            mock_db.func.now = Mock()
            
            from app.models.suitability import SuitabilityProfile
            
            profile = SuitabilityProfile(**self.profile_data)
            
            repr_str = repr(profile)
            
            assert "SuitabilityProfile" in repr_str
            assert "user_id=1" in repr_str
            assert "family_id=1" in repr_str
            assert "risk_tolerance=moderate" in repr_str
