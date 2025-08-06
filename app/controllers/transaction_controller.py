"""Transaction controller for handling transaction operations"""
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from marshmallow import ValidationError

from app.models.transaction import Transaction
from app.models.asset import Asset
from app.models.user import User
from app.schema.transaction_schema import TransactionSchema, TransactionSummarySchema
from app.config.extensions import db


transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)
transaction_summary_schema = TransactionSummarySchema()


def create_transaction_controller(req):
    """Create a new transaction"""
    try:
        data = req.get_json()
        if not data:
            return jsonify({"error": "Request data is required"}), 400
        
        # Validate transaction data
        try:
            validated_data = transaction_schema.load(data)
        except ValidationError as err:
            return jsonify(err.messages), 400
        
        # Check if asset exists and user has access
        asset = db.session.get(Asset, validated_data['asset_id'])
        if not asset:
            return jsonify({"error": "Asset not found"}), 404
        
        # Verify user has access to the asset's family
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        if not user or not any(f.id == asset.family_id for f in user.families):
            return jsonify({"error": "Access denied to this asset"}), 403
        
        # Additional validation for sell transactions
        if validated_data['transaction_type'] == 'sell':
            try:
                Transaction.validate_sell_quantity(asset.id, validated_data['quantity'])
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
        
        # Create transaction
        transaction = Transaction(**validated_data)
        db.session.add(transaction)
        db.session.commit()
        
        # Manually serialize to avoid issues with @post_load removal
        response_data = {
            "id": transaction.id,
            "asset_id": transaction.asset_id,
            "transaction_type": transaction.transaction_type,
            "quantity": transaction.quantity,
            "unit_price": transaction.unit_price,
            "total_value": transaction.total_value,
            "transaction_date": transaction.transaction_date.isoformat() if transaction.transaction_date else None,
            "description": transaction.description,
            "created_at": transaction.created_at.isoformat() if transaction.created_at else None,
            "updated_at": transaction.updated_at.isoformat() if transaction.updated_at else None
        }
        return jsonify(response_data), 201
        
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


def list_transactions_controller(req):
    """List transactions with optional filtering"""
    try:
        # Get query parameters
        asset_id = req.args.get('asset_id', type=int)
        family_id = req.args.get('family_id', type=int)
        transaction_type = req.args.get('transaction_type')
        limit = req.args.get('limit', default=100, type=int)
        offset = req.args.get('offset', default=0, type=int)
        
        # Verify user access
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Build query
        query = Transaction.query.join(Asset)
        
        # Filter by user's families
        user_family_ids = [f.id for f in user.families]
        query = query.filter(Asset.family_id.in_(user_family_ids))
        
        # Apply filters
        if asset_id:
            # Verify user has access to this specific asset
            asset = db.session.get(Asset, asset_id)
            if not asset or asset.family_id not in user_family_ids:
                return jsonify({"error": "Access denied to this asset"}), 403
            query = query.filter(Transaction.asset_id == asset_id)
        
        if family_id:
            if family_id not in user_family_ids:
                return jsonify({"error": "Access denied to this family"}), 403
            query = query.filter(Asset.family_id == family_id)
        
        if transaction_type:
            if transaction_type not in ['buy', 'sell']:
                return jsonify({"error": "Invalid transaction type"}), 400
            query = query.filter(Transaction.transaction_type == transaction_type)
        
        # Order by most recent first
        query = query.order_by(Transaction.created_at.desc())
        
        # Apply pagination
        transactions = query.offset(offset).limit(limit).all()
        
        # Manually serialize transactions list
        response_data = []
        for t in transactions:
            transaction_data = {
                "id": t.id,
                "asset_id": t.asset_id,
                "transaction_type": t.transaction_type,
                "quantity": t.quantity,
                "unit_price": t.unit_price,
                "total_value": t.total_value,
                "transaction_date": t.transaction_date.isoformat() if t.transaction_date else None,
                "description": t.description,
                "created_at": t.created_at.isoformat() if t.created_at else None,
                "updated_at": t.updated_at.isoformat() if t.updated_at else None
            }
            response_data.append(transaction_data)
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


def get_transaction_controller(transaction_id):
    """Get a specific transaction by ID"""
    try:
        transaction = db.session.get(Transaction, transaction_id)
        if not transaction:
            return jsonify({"error": "Transaction not found"}), 404
        
        # Verify user has access to the transaction's asset
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        asset = transaction.asset
        if not any(f.id == asset.family_id for f in user.families):
            return jsonify({"error": "Access denied"}), 403
        
        # Manually serialize transaction
        response_data = {
            "id": transaction.id,
            "asset_id": transaction.asset_id,
            "transaction_type": transaction.transaction_type,
            "quantity": transaction.quantity,
            "unit_price": transaction.unit_price,
            "total_value": transaction.total_value,
            "transaction_date": transaction.transaction_date.isoformat() if transaction.transaction_date else None,
            "description": transaction.description,
            "created_at": transaction.created_at.isoformat() if transaction.created_at else None,
            "updated_at": transaction.updated_at.isoformat() if transaction.updated_at else None
        }
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


def update_transaction_controller(transaction_id, req):
    """Update a transaction"""
    try:
        transaction = db.session.get(Transaction, transaction_id)
        if not transaction:
            return jsonify({"error": "Transaction not found"}), 404
        
        # Verify user has access
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        asset = transaction.asset
        if not any(f.id == asset.family_id for f in user.families):
            return jsonify({"error": "Access denied"}), 403
        
        # Get update data
        data = req.get_json()
        if not data:
            return jsonify({"error": "Request data is required"}), 400
        
        # Validate partial update data
        try:
            validated_data = transaction_schema.load(data, partial=True)
        except ValidationError as err:
            return jsonify(err.messages), 400
        
        # Check quantity validation for sell transactions
        if ('transaction_type' in validated_data and validated_data['transaction_type'] == 'sell') or \
           (transaction.transaction_type == 'sell' and 'quantity' in validated_data):
            
            # Calculate available quantity excluding this transaction
            current_quantity = asset.current_quantity
            if transaction.transaction_type == 'sell':
                current_quantity += transaction.quantity  # Add back the current transaction quantity
            elif transaction.transaction_type == 'buy':
                current_quantity -= transaction.quantity  # Remove the current transaction quantity
            
            new_quantity = validated_data.get('quantity', transaction.quantity)
            if current_quantity < new_quantity:
                return jsonify({
                    "error": f"Cannot sell more than available quantity. Available: {current_quantity}"
                }), 400
        
        # Update transaction fields
        for field, value in validated_data.items():
            setattr(transaction, field, value)
        
        # Recalculate total_value if quantity or unit_price changed
        if 'quantity' in validated_data or 'unit_price' in validated_data:
            transaction.total_value = round(transaction.quantity * transaction.unit_price, 2)
        
        db.session.commit()
        
        # Manually serialize updated transaction
        response_data = {
            "id": transaction.id,
            "asset_id": transaction.asset_id,
            "transaction_type": transaction.transaction_type,
            "quantity": transaction.quantity,
            "unit_price": transaction.unit_price,
            "total_value": transaction.total_value,
            "transaction_date": transaction.transaction_date.isoformat() if transaction.transaction_date else None,
            "description": transaction.description,
            "created_at": transaction.created_at.isoformat() if transaction.created_at else None,
            "updated_at": transaction.updated_at.isoformat() if transaction.updated_at else None
        }
        return jsonify(response_data), 200
        
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


def delete_transaction_controller(transaction_id):
    """Delete a transaction"""
    try:
        transaction = db.session.get(Transaction, transaction_id)
        if not transaction:
            return jsonify({"error": "Transaction not found"}), 404
        
        # Verify user has access
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        asset = transaction.asset
        if not any(f.id == asset.family_id for f in user.families):
            return jsonify({"error": "Access denied"}), 403
        
        # Delete transaction
        db.session.delete(transaction)
        db.session.commit()
        
        return "", 204
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


def get_asset_transaction_summary_controller(asset_id):
    """Get transaction summary for a specific asset"""
    try:
        # Verify asset exists and user has access
        asset = db.session.get(Asset, asset_id)
        if not asset:
            return jsonify({"error": "Asset not found"}), 404
        
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        if not user or not any(f.id == asset.family_id for f in user.families):
            return jsonify({"error": "Access denied"}), 403
        
        # Calculate summary data
        buy_transactions = asset.get_transactions_by_type('buy')
        sell_transactions = asset.get_transactions_by_type('sell')
        
        summary = {
            'total_transactions': len(asset.transactions),
            'total_buy_transactions': len(buy_transactions),
            'total_sell_transactions': len(sell_transactions),
            'total_invested': asset.total_invested,
            'total_divested': asset.total_divested,
            'net_investment': asset.total_invested - asset.total_divested,
            'current_quantity': asset.current_quantity,
            'average_cost': asset.average_cost,
            'latest_transaction_date': asset.get_latest_transaction().transaction_date if asset.get_latest_transaction() else None
        }
        
        return jsonify(transaction_summary_schema.dump(summary)), 200
        
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500