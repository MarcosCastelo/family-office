"""Testes para as melhorias na entidade Asset"""
import pytest
from datetime import datetime, date
from decimal import Decimal
from app.models.asset import Asset
from app.services.cache_service import asset_cache
from app.services.asset_validation_service import AssetValidationService


class TestAssetImprovements:
    """Testes para as melhorias implementadas na entidade Asset"""
    
    def test_asset_specific_properties(self, db_session, sample_family):
        """Testa as propriedades específicas por tipo de ativo"""
        # Teste para renda variável
        stock_asset = Asset(
            name="Petrobras PN",
            asset_type="renda_variavel",
            family_id=sample_family.id,
            details={"ticker": "PETR4.SA"}
        )
        db_session.add(stock_asset)
        db_session.commit()
        
        assert stock_asset.ticker == "PETR4.SA"
        assert stock_asset.indexador is None
        assert stock_asset.vencimento is None
        assert stock_asset.asset_class == "Variable Income"
        
        # Teste para renda fixa
        fixed_asset = Asset(
            name="Tesouro IPCA 2026",
            asset_type="renda_fixa",
            family_id=sample_family.id,
            details={
                "indexador": "IPCA",
                "vencimento": "2026-01-01"
            }
        )
        db_session.add(fixed_asset)
        db_session.commit()
        
        assert fixed_asset.indexador == "IPCA"
        assert fixed_asset.vencimento == "2026-01-01"
        assert fixed_asset.ticker is None
        assert fixed_asset.asset_class == "Fixed Income"
        
        # Teste para criptomoeda
        crypto_asset = Asset(
            name="Bitcoin",
            asset_type="criptomoeda",
            family_id=sample_family.id,
            details={"coin_id": "bitcoin"}
        )
        db_session.add(crypto_asset)
        db_session.commit()
        
        assert crypto_asset.coin_id == "bitcoin"
        assert crypto_asset.asset_class == "Alternative"
    
    def test_risk_metrics_calculation(self, db_session, sample_family):
        """Testa o cálculo de métricas de risco"""
        asset = Asset(
            name="Test Asset",
            asset_type="renda_variavel",
            family_id=sample_family.id,
            details={"ticker": "TEST4.SA"}
        )
        db_session.add(asset)
        db_session.commit()
        
        # Sem histórico de cotações, deve retornar dict vazio
        risk_metrics = asset.get_risk_metrics()
        assert isinstance(risk_metrics, dict)
        assert len(risk_metrics) == 0
    
    def test_cache_decorator(self, db_session, sample_family):
        """Testa o decorator de cache"""
        # Limpar cache antes do teste
        asset_cache.clear()
        
        asset = Asset(
            name="Cached Asset",
            asset_type="renda_variavel",
            family_id=sample_family.id,
            details={"ticker": "CACH4.SA"}
        )
        db_session.add(asset)
        db_session.commit()
        
        # Primeira chamada - deve calcular
        quantity1 = asset.current_quantity
        assert quantity1 == 0.0
        
        # Segunda chamada - deve usar cache
        quantity2 = asset.current_quantity
        assert quantity2 == 0.0
        
        # Verificar se está no cache
        cache_stats = asset_cache.get_stats()
        assert cache_stats['active_keys'] > 0
    
    def test_asset_validation_service(self):
        """Testa o serviço de validação de ativos"""
        # Validação de ticker brasileiro
        is_valid, message = AssetValidationService.validate_ticker("PETR4.SA", "renda_variavel", "B3")
        assert is_valid is True
        assert message == ""
        
        # Validação de ticker inválido
        is_valid, message = AssetValidationService.validate_ticker("INVALID", "renda_variavel", "B3")
        assert is_valid is False
        assert "formato" in message
        
        # Validação de criptomoeda
        is_valid, message = AssetValidationService.validate_ticker("bitcoin", "criptomoeda")
        assert is_valid is True
        
        # Validação de moeda estrangeira
        is_valid, message = AssetValidationService.validate_ticker("USD", "moeda_estrangeira")
        assert is_valid is True
    
    def test_ticker_normalization(self):
        """Testa a normalização de tickers"""
        # Brasileiro sem .SA
        normalized = AssetValidationService.normalize_ticker("PETR4", "renda_variavel", "B3")
        assert normalized == "PETR4.SA"
        
        # Brasileiro com .SA
        normalized = AssetValidationService.normalize_ticker("VALE3.SA", "renda_variavel", "B3")
        assert normalized == "VALE3.SA"
        
        # Americano com .SA (deve remover)
        normalized = AssetValidationService.normalize_ticker("AAPL.SA", "renda_variavel", "NYSE")
        assert normalized == "AAPL"
        
        # Criptomoeda
        normalized = AssetValidationService.normalize_ticker("BTC", "criptomoeda")
        assert normalized == "bitcoin"
    
    def test_fixed_income_validation(self):
        """Testa validação de campos de renda fixa"""
        # Válido
        is_valid, message = AssetValidationService.validate_fixed_income_fields({
            "indexador": "CDI",
            "vencimento": "2026-01-01"
        })
        assert is_valid is True
        
        # Sem indexador
        is_valid, message = AssetValidationService.validate_fixed_income_fields({
            "vencimento": "2026-01-01"
        })
        assert is_valid is False
        assert "indexador" in message
        
        # Vencimento passado
        past_date = (datetime.now().date() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        is_valid, message = AssetValidationService.validate_fixed_income_fields({
            "indexador": "CDI",
            "vencimento": past_date
        })
        assert is_valid is False
        assert "futura" in message
    
    def test_asset_name_validation(self):
        """Testa validação de nomes de ativos"""
        # Nome válido
        is_valid, message = AssetValidationService.validate_asset_name("Petrobras PN")
        assert is_valid is True
        
        # Nome muito curto
        is_valid, message = AssetValidationService.validate_asset_name("A")
        assert is_valid is False
        assert "2 caracteres" in message
        
        # Nome com caracteres inválidos
        is_valid, message = AssetValidationService.validate_asset_name("Asset<Test>")
        assert is_valid is False
        assert "caracteres inválidos" in message
    
    def test_suggested_tickers(self):
        """Testa sugestões de tickers"""
        # Brasileiros
        suggestions = AssetValidationService.get_suggested_tickers("renda_variavel", "B3")
        assert "PETR4.SA" in suggestions
        assert "VALE3.SA" in suggestions
        
        # Americanos
        suggestions = AssetValidationService.get_suggested_tickers("renda_variavel", "NYSE")
        assert "AAPL" in suggestions
        assert "GOOGL" in suggestions
        
        # Criptomoedas
        suggestions = AssetValidationService.get_suggested_tickers("criptomoeda")
        assert "bitcoin" in suggestions
        assert "ethereum" in suggestions


@pytest.fixture
def sample_family(db_session):
    """Fixture para criar uma família de teste"""
    from app.models.family import Family
    family = Family(name="Test Family")
    db_session.add(family)
    db_session.commit()
    return family
