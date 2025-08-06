"""Tests for Transaction schema validation following TDD approach"""
import pytest
from datetime import date
from marshmallow import ValidationError

from app.schema.transaction_schema import TransactionSchema


class TestTransactionSchema:
    """Test Transaction schema validation"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.schema = TransactionSchema()
        self.valid_data = {
            "asset_id": 1,
            "transaction_type": "buy",
            "quantity": 100.0,
            "unit_price": 10.50,
            "transaction_date": "2024-01-15",
            "description": "Initial purchase"
        }
    
    def test_valid_transaction_data_validates(self):
        """Test valid transaction data passes validation"""
        # Act
        result = self.schema.load(self.valid_data)
        
        # Assert
        assert result["asset_id"] == 1
        assert result["transaction_type"] == "buy"
        assert result["quantity"] == 100.0
        assert result["unit_price"] == 10.50
        assert result["transaction_date"] == date(2024, 1, 15)
        assert result["description"] == "Initial purchase"
    
    def test_transaction_type_validation(self):
        """Test transaction_type must be 'buy' or 'sell'"""
        # Valid types
        valid_types = ["buy", "sell"]
        for transaction_type in valid_types:
            data = self.valid_data.copy()
            data["transaction_type"] = transaction_type
            result = self.schema.load(data)
            assert result["transaction_type"] == transaction_type
        
        # Invalid type
        data = self.valid_data.copy()
        data["transaction_type"] = "invalid"
        with pytest.raises(ValidationError) as exc_info:
            self.schema.load(data)
        assert "transaction_type" in exc_info.value.messages
    
    def test_quantity_validation(self):
        """Test quantity must be positive number"""
        # Valid positive quantity
        data = self.valid_data.copy()
        data["quantity"] = 50.5
        result = self.schema.load(data)
        assert result["quantity"] == 50.5
        
        # Invalid zero quantity
        data = self.valid_data.copy()
        data["quantity"] = 0
        with pytest.raises(ValidationError) as exc_info:
            self.schema.load(data)
        assert "quantity" in exc_info.value.messages
        
        # Invalid negative quantity
        data = self.valid_data.copy()
        data["quantity"] = -10.0
        with pytest.raises(ValidationError) as exc_info:
            self.schema.load(data)
        assert "quantity" in exc_info.value.messages
    
    def test_unit_price_validation(self):
        """Test unit_price must be positive number"""
        # Valid positive price
        data = self.valid_data.copy()
        data["unit_price"] = 25.75
        result = self.schema.load(data)
        assert result["unit_price"] == 25.75
        
        # Invalid zero price
        data = self.valid_data.copy()
        data["unit_price"] = 0
        with pytest.raises(ValidationError) as exc_info:
            self.schema.load(data)
        assert "unit_price" in exc_info.value.messages
        
        # Invalid negative price
        data = self.valid_data.copy()
        data["unit_price"] = -5.0
        with pytest.raises(ValidationError) as exc_info:
            self.schema.load(data)
        assert "unit_price" in exc_info.value.messages
    
    def test_required_fields_validation(self):
        """Test all required fields are validated"""
        required_fields = ["asset_id", "transaction_type", "quantity", "unit_price"]
        
        for field in required_fields:
            data = self.valid_data.copy()
            del data[field]
            
            with pytest.raises(ValidationError) as exc_info:
                self.schema.load(data)
            assert field in exc_info.value.messages
    
    def test_asset_id_validation(self):
        """Test asset_id must be positive integer"""
        # Valid asset_id
        data = self.valid_data.copy()
        data["asset_id"] = 5
        result = self.schema.load(data)
        assert result["asset_id"] == 5
        
        # Invalid zero asset_id
        data = self.valid_data.copy()
        data["asset_id"] = 0
        with pytest.raises(ValidationError) as exc_info:
            self.schema.load(data)
        assert "asset_id" in exc_info.value.messages
        
        # Invalid negative asset_id
        data = self.valid_data.copy()
        data["asset_id"] = -1
        with pytest.raises(ValidationError) as exc_info:
            self.schema.load(data)
        assert "asset_id" in exc_info.value.messages
    
    def test_transaction_date_validation(self):
        """Test transaction_date validation"""
        # Valid date string
        data = self.valid_data.copy()
        data["transaction_date"] = "2023-12-25"
        result = self.schema.load(data)
        assert result["transaction_date"] == date(2023, 12, 25)
        
        # Invalid date format
        data = self.valid_data.copy()
        data["transaction_date"] = "invalid-date"
        with pytest.raises(ValidationError) as exc_info:
            self.schema.load(data)
        assert "transaction_date" in exc_info.value.messages
        
        # Future date (should be allowed)
        data = self.valid_data.copy()
        data["transaction_date"] = "2025-01-01"
        result = self.schema.load(data)
        assert result["transaction_date"] == date(2025, 1, 1)
    
    def test_optional_fields(self):
        """Test optional fields behavior"""
        # Description is optional
        data = self.valid_data.copy()
        del data["description"]
        result = self.schema.load(data)
        assert "description" not in result
        
        # Transaction date defaults to today if not provided
        data = self.valid_data.copy()
        del data["transaction_date"]
        result = self.schema.load(data)
        assert result["transaction_date"] == date.today()
    
    def test_schema_dump_transaction(self):
        """Test schema can serialize transaction data"""
        from datetime import datetime
        
        # Arrange
        transaction_data = {
            "id": 1,
            "asset_id": 1,
            "transaction_type": "buy",
            "quantity": 100.0,
            "unit_price": 10.50,
            "total_value": 1050.0,
            "transaction_date": date(2024, 1, 15),
            "description": "Initial purchase",
            "created_at": datetime(2024, 1, 15, 10, 30, 0)  # Use datetime object
        }
        
        # Act
        result = self.schema.dump(transaction_data)
        
        # Assert
        assert result["id"] == 1
        assert result["asset_id"] == 1
        assert result["transaction_type"] == "buy"
        assert result["quantity"] == 100.0
        assert result["unit_price"] == 10.50
        assert result["total_value"] == 1050.0
        assert result["transaction_date"] == "2024-01-15"
        assert result["description"] == "Initial purchase"