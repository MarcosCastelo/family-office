"""Tests for Transaction controller following TDD approach"""
import pytest
import json
from datetime import date
from flask_jwt_extended import create_access_token

from app.models.user import User
from app.models.family import Family
from app.models.asset import Asset
from app.models.transaction import Transaction
from app.config.extensions import db


class TestTransactionController:
    """Test Transaction controller endpoints"""
    
    def setup_test_data(self, db):
        """Setup test data for each test method"""
        # Create test user
        self.user = User(email="test@example.com")
        self.user.set_password("password123")
        db.session.add(self.user)
        
        # Create test family
        self.family = Family(name="Test Family")
        db.session.add(self.family)
        
        # Associate user with family
        self.user.families.append(self.family)
        
        db.session.commit()
        
        # Create test asset
        self.asset = Asset(
            name="Test Asset",
            asset_type="renda_fixa",
            value=0.0,  # Temporary value for backward compatibility
            family_id=self.family.id
        )
        db.session.add(self.asset)
        db.session.commit()
        
        # Create access token
        self.access_token = create_access_token(identity=str(self.user.id))
        self.headers = {"Authorization": f"Bearer {self.access_token}"}
    
    def test_create_transaction_success(self, client, db):
        """Test successful transaction creation"""
        # Arrange
        self.setup_test_data(db)
        
        transaction_data = {
            "asset_id": self.asset.id,
            "transaction_type": "buy",
            "quantity": 100.0,
            "unit_price": 10.50,
            "transaction_date": "2024-01-15",
            "description": "Initial purchase"
        }
        
        # Act
        response = client.post(
            "/transactions",
            data=json.dumps(transaction_data),
            headers=self.headers,
            content_type="application/json"
        )
        
        # Assert
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["asset_id"] == self.asset.id
        assert data["transaction_type"] == "buy"
        assert data["quantity"] == 100.0
        assert data["unit_price"] == 10.50
        assert data["total_value"] == 1050.0
        
        # Verify transaction was saved to database
        transaction = Transaction.query.first()
        assert transaction is not None
        assert transaction.asset_id == self.asset.id
    
    def test_create_transaction_invalid_data(self, client, db):
        """Test transaction creation with invalid data"""
        # Arrange
        self.setup_test_data(db)
        
        invalid_data = {
            "asset_id": self.asset.id,
            "transaction_type": "invalid_type",
            "quantity": -10.0,  # Invalid negative quantity
            "unit_price": 0.0   # Invalid zero price
        }
        
        # Act
        response = client.post(
            "/transactions",
            data=json.dumps(invalid_data),
            headers=self.headers,
            content_type="application/json"
        )
        
        # Assert
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "quantity" in data or "unit_price" in data or "transaction_type" in data
    
    def test_create_transaction_asset_not_found(self, client, db):
        """Test transaction creation with non-existent asset"""
        # Arrange
        self.setup_test_data(db)
        
        transaction_data = {
            "asset_id": 999,  # Non-existent asset
            "transaction_type": "buy",
            "quantity": 100.0,
            "unit_price": 10.50
        }
        
        # Act
        response = client.post(
            "/transactions",
            data=json.dumps(transaction_data),
            headers=self.headers,
            content_type="application/json"
        )
        
        # Assert
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "error" in data
    
    def test_create_transaction_asset_access_denied(self, client, db):
        """Test transaction creation with asset from different family"""
        # Arrange
        self.setup_test_data(db)
        
        # Create another family and asset
        other_family = Family(name="Other Family")
        db.session.add(other_family)
        db.session.commit()
        
        other_asset = Asset(
            name="Other Asset",
            asset_type="renda_fixa",
            value=0.0,  # Temporary value for backward compatibility
            family_id=other_family.id
        )
        db.session.add(other_asset)
        db.session.commit()
        
        transaction_data = {
            "asset_id": other_asset.id,
            "transaction_type": "buy",
            "quantity": 100.0,
            "unit_price": 10.50
        }
        
        # Act
        response = client.post(
            "/transactions",
            data=json.dumps(transaction_data),
            headers=self.headers,
            content_type="application/json"
        )
        
        # Assert
        assert response.status_code == 403
        data = json.loads(response.data)
        assert "error" in data
    
    def test_list_transactions_by_asset(self, client, db):
        """Test listing transactions for a specific asset"""
        # Arrange
        self.setup_test_data(db)
        
        # Create transactions
        transaction1 = Transaction(
            asset_id=self.asset.id,
            transaction_type="buy",
            quantity=100.0,
            unit_price=10.0
        )
        transaction2 = Transaction(
            asset_id=self.asset.id,
            transaction_type="sell",
            quantity=50.0,
            unit_price=12.0
        )
        db.session.add_all([transaction1, transaction2])
        db.session.commit()
        
        # Act
        response = client.get(
            f"/transactions?asset_id={self.asset.id}",
            headers=self.headers
        )
        
        # Assert
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2
        assert data[0]["transaction_type"] in ["buy", "sell"]
        assert data[1]["transaction_type"] in ["buy", "sell"]
    
    def test_get_transaction_by_id(self, client, db):
        """Test getting specific transaction by ID"""
        # Arrange
        self.setup_test_data(db)
        
        transaction = Transaction(
            asset_id=self.asset.id,
            transaction_type="buy",
            quantity=100.0,
            unit_price=10.0
        )
        db.session.add(transaction)
        db.session.commit()
        
        # Act
        response = client.get(
            f"/transactions/{transaction.id}",
            headers=self.headers
        )
        
        # Assert
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["id"] == transaction.id
        assert data["asset_id"] == self.asset.id
        assert data["transaction_type"] == "buy"
    
    def test_update_transaction(self, client, db):
        """Test updating a transaction"""
        # Arrange
        self.setup_test_data(db)
        
        transaction = Transaction(
            asset_id=self.asset.id,
            transaction_type="buy",
            quantity=100.0,
            unit_price=10.0
        )
        db.session.add(transaction)
        db.session.commit()
        
        update_data = {
            "quantity": 150.0,
            "unit_price": 12.0,
            "description": "Updated transaction"
        }
        
        # Act
        response = client.put(
            f"/transactions/{transaction.id}",
            data=json.dumps(update_data),
            headers=self.headers,
            content_type="application/json"
        )
        
        # Assert
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["quantity"] == 150.0
        assert data["unit_price"] == 12.0
        assert data["description"] == "Updated transaction"
        assert data["total_value"] == 1800.0
    
    def test_delete_transaction(self, client, db):
        """Test deleting a transaction"""
        # Arrange
        self.setup_test_data(db)
        
        transaction = Transaction(
            asset_id=self.asset.id,
            transaction_type="buy",
            quantity=100.0,
            unit_price=10.0
        )
        db.session.add(transaction)
        db.session.commit()
        
        transaction_id = transaction.id
        
        # Act
        response = client.delete(
            f"/transactions/{transaction_id}",
            headers=self.headers
        )
        
        # Assert
        assert response.status_code == 204
        
        # Verify transaction was deleted
        from app.config.extensions import db
        deleted_transaction = db.session.get(Transaction, transaction_id)
        assert deleted_transaction is None
    
    def test_prevent_sell_more_than_owned(self, client, db):
        """Test validation prevents selling more than owned"""
        # Arrange
        self.setup_test_data(db)
        
        # Buy 100 shares first
        buy_transaction = Transaction(
            asset_id=self.asset.id,
            transaction_type="buy",
            quantity=100.0,
            unit_price=10.0
        )
        db.session.add(buy_transaction)
        db.session.commit()
        
        # Try to sell 150 shares (more than owned)
        sell_data = {
            "asset_id": self.asset.id,
            "transaction_type": "sell",
            "quantity": 150.0,
            "unit_price": 12.0
        }
        
        # Act
        response = client.post(
            "/transactions",
            data=json.dumps(sell_data),
            headers=self.headers,
            content_type="application/json"
        )
        
        # Assert
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "Cannot sell more than current quantity" in data["error"]
    
    def test_unauthorized_access(self, client, db):
        """Test unauthorized access returns 401"""
        # Act
        response = client.get("/transactions")
        
        # Assert
        assert response.status_code == 401