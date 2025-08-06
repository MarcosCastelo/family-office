import React, { useState, useEffect } from 'react';
import { X, DollarSign, Calendar, FileText, TrendingUp, TrendingDown } from 'lucide-react';
import { Transaction } from '../services/transactions';
import { Asset } from '../services/assets';
import { useToast } from './Toast';

interface TransactionFormProps {
  asset: Asset;
  transaction?: Transaction;
  onSubmit: (transaction: Omit<Transaction, 'id' | 'total_value' | 'created_at' | 'updated_at'>) => Promise<void>;
  onCancel: () => void;
  loading: boolean;
}

export default function TransactionForm({ asset, transaction, onSubmit, onCancel, loading }: TransactionFormProps) {
  const { showToast } = useToast();
  const [formData, setFormData] = useState({
    transaction_type: transaction?.transaction_type || 'buy' as 'buy' | 'sell',
    quantity: transaction?.quantity?.toString() || '',
    unit_price: transaction?.unit_price?.toString() || '',
    transaction_date: transaction?.transaction_date || new Date().toISOString().split('T')[0],
    description: transaction?.description || ''
  });

  const [totalValue, setTotalValue] = useState(0);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const quantity = parseFloat(formData.quantity) || 0;
    const unitPrice = parseFloat(formData.unit_price) || 0;
    setTotalValue(quantity * unitPrice);
  }, [formData.quantity, formData.unit_price]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // Validações
    const quantity = parseFloat(formData.quantity);
    const unitPrice = parseFloat(formData.unit_price);

    if (quantity <= 0) {
      setError('Quantidade deve ser maior que zero');
      return;
    }

    if (unitPrice <= 0) {
      setError('Preço unitário deve ser maior que zero');
      return;
    }

    if (formData.transaction_type === 'sell' && asset.current_quantity !== undefined && quantity > asset.current_quantity) {
      const errorMsg = `Não é possível vender mais que a quantidade atual (${asset.current_quantity})`;
      setError(errorMsg);
      showToast(errorMsg, 'warning');
      return;
    }

    try {
      await onSubmit({
        asset_id: asset.id,
        transaction_type: formData.transaction_type,
        quantity,
        unit_price: unitPrice,
        transaction_date: formData.transaction_date,
        description: formData.description || undefined
      });
    } catch (err: any) {
      setError(err.response?.data?.error || 'Erro ao salvar transação');
    }
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(0,0,0,0.5)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000
    }}>
      <div style={{
        background: 'white',
        borderRadius: 16,
        padding: 32,
        maxWidth: 500,
        width: '100%',
        margin: 16,
        maxHeight: '90vh',
        overflow: 'auto',
        boxShadow: '0 20px 60px rgba(0,0,0,0.2)'
      }}>
        {/* Header */}
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: 24
        }}>
          <div>
            <h2 style={{ margin: 0, color: '#222', fontSize: 24, fontWeight: 600 }}>
              {transaction ? 'Editar Transação' : 'Nova Transação'}
            </h2>
            <p style={{ margin: '4px 0 0 0', color: '#666', fontSize: 14 }}>
              Ativo: {asset.name}
            </p>
          </div>
          <button
            onClick={onCancel}
            style={{
              border: 'none',
              background: 'transparent',
              cursor: 'pointer',
              padding: 8,
              borderRadius: 8,
              color: '#666'
            }}
          >
            <X size={24} />
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          {/* Tipo de Transação */}
          <div style={{ marginBottom: 20 }}>
            <label style={{ display: 'block', marginBottom: 8, fontWeight: 500, color: '#333' }}>
              Tipo de Transação
            </label>
            <div style={{ display: 'flex', gap: 12 }}>
              <button
                type="button"
                onClick={() => setFormData({ ...formData, transaction_type: 'buy' })}
                style={{
                  flex: 1,
                  padding: '12px 16px',
                  border: `2px solid ${formData.transaction_type === 'buy' ? '#22c55e' : '#e5e7eb'}`,
                  background: formData.transaction_type === 'buy' ? '#f0fdf4' : 'white',
                  color: formData.transaction_type === 'buy' ? '#22c55e' : '#666',
                  borderRadius: 8,
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: 8,
                  fontWeight: 500,
                  transition: 'all 0.2s ease'
                }}
              >
                <TrendingUp size={18} />
                Compra
              </button>
              <button
                type="button"
                onClick={() => setFormData({ ...formData, transaction_type: 'sell' })}
                style={{
                  flex: 1,
                  padding: '12px 16px',
                  border: `2px solid ${formData.transaction_type === 'sell' ? '#ef4444' : '#e5e7eb'}`,
                  background: formData.transaction_type === 'sell' ? '#fef2f2' : 'white',
                  color: formData.transaction_type === 'sell' ? '#ef4444' : '#666',
                  borderRadius: 8,
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: 8,
                  fontWeight: 500,
                  transition: 'all 0.2s ease'
                }}
              >
                <TrendingDown size={18} />
                Venda
              </button>
            </div>
          </div>

          {/* Quantidade */}
          <div style={{ marginBottom: 20 }}>
            <label style={{ display: 'block', marginBottom: 8, fontWeight: 500, color: '#333' }}>
              Quantidade
            </label>
            <input
              type="number"
              step="0.000001"
              min="0"
              value={formData.quantity}
              onChange={e => setFormData({ ...formData, quantity: e.target.value })}
              required
              style={{
                width: '100%',
                padding: '12px 16px',
                border: '2px solid #e5e7eb',
                borderRadius: 8,
                fontSize: 14,
                transition: 'border-color 0.2s ease'
              }}
              onFocus={e => e.target.style.borderColor = '#667eea'}
              onBlur={e => e.target.style.borderColor = '#e5e7eb'}
            />
            {formData.transaction_type === 'sell' && asset.current_quantity !== undefined && (
              <p style={{ margin: '4px 0 0 0', fontSize: 12, color: '#666' }}>
                Quantidade disponível: {asset.current_quantity}
              </p>
            )}
          </div>

          {/* Preço Unitário */}
          <div style={{ marginBottom: 20 }}>
            <label style={{ display: 'block', marginBottom: 8, fontWeight: 500, color: '#333' }}>
              Preço Unitário
            </label>
            <div style={{ position: 'relative' }}>
              <DollarSign 
                size={18} 
                style={{ 
                  position: 'absolute', 
                  left: 12, 
                  top: '50%', 
                  transform: 'translateY(-50%)', 
                  color: '#666' 
                }} 
              />
              <input
                type="number"
                step="0.01"
                min="0"
                value={formData.unit_price}
                onChange={e => setFormData({ ...formData, unit_price: e.target.value })}
                required
                style={{
                  width: '100%',
                  padding: '12px 16px 12px 40px',
                  border: '2px solid #e5e7eb',
                  borderRadius: 8,
                  fontSize: 14,
                  transition: 'border-color 0.2s ease'
                }}
                onFocus={e => e.target.style.borderColor = '#667eea'}
                onBlur={e => e.target.style.borderColor = '#e5e7eb'}
              />
            </div>
          </div>

          {/* Valor Total */}
          {totalValue > 0 && (
            <div style={{
              padding: 12,
              background: '#f8fafc',
              borderRadius: 8,
              marginBottom: 20,
              border: '1px solid #e2e8f0'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ color: '#666', fontSize: 14 }}>Valor Total:</span>
                <span style={{ 
                  fontWeight: 600, 
                  fontSize: 16, 
                  color: formData.transaction_type === 'buy' ? '#22c55e' : '#ef4444' 
                }}>
                  {formatCurrency(totalValue)}
                </span>
              </div>
            </div>
          )}

          {/* Data da Transação */}
          <div style={{ marginBottom: 20 }}>
            <label style={{ display: 'block', marginBottom: 8, fontWeight: 500, color: '#333' }}>
              Data da Transação
            </label>
            <div style={{ position: 'relative' }}>
              <Calendar 
                size={18} 
                style={{ 
                  position: 'absolute', 
                  left: 12, 
                  top: '50%', 
                  transform: 'translateY(-50%)', 
                  color: '#666' 
                }} 
              />
              <input
                type="date"
                value={formData.transaction_date}
                onChange={e => setFormData({ ...formData, transaction_date: e.target.value })}
                required
                style={{
                  width: '100%',
                  padding: '12px 16px 12px 40px',
                  border: '2px solid #e5e7eb',
                  borderRadius: 8,
                  fontSize: 14,
                  transition: 'border-color 0.2s ease'
                }}
                onFocus={e => e.target.style.borderColor = '#667eea'}
                onBlur={e => e.target.style.borderColor = '#e5e7eb'}
              />
            </div>
          </div>

          {/* Descrição */}
          <div style={{ marginBottom: 24 }}>
            <label style={{ display: 'block', marginBottom: 8, fontWeight: 500, color: '#333' }}>
              Descrição (opcional)
            </label>
            <div style={{ position: 'relative' }}>
              <FileText 
                size={18} 
                style={{ 
                  position: 'absolute', 
                  left: 12, 
                  top: 16, 
                  color: '#666' 
                }} 
              />
              <textarea
                value={formData.description}
                onChange={e => setFormData({ ...formData, description: e.target.value })}
                placeholder="Adicione uma descrição..."
                style={{
                  width: '100%',
                  padding: '12px 16px 12px 40px',
                  border: '2px solid #e5e7eb',
                  borderRadius: 8,
                  fontSize: 14,
                  minHeight: 80,
                  resize: 'vertical',
                  fontFamily: 'inherit',
                  transition: 'border-color 0.2s ease'
                }}
                onFocus={e => e.target.style.borderColor = '#667eea'}
                onBlur={e => e.target.style.borderColor = '#e5e7eb'}
              />
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div style={{
              padding: 12,
              background: '#fef2f2',
              border: '1px solid #fecaca',
              borderRadius: 8,
              color: '#dc2626',
              marginBottom: 20,
              fontSize: 14
            }}>
              {error}
            </div>
          )}

          {/* Buttons */}
          <div style={{ display: 'flex', gap: 12 }}>
            <button
              type="button"
              onClick={onCancel}
              disabled={loading}
              style={{
                flex: 1,
                padding: '12px 16px',
                border: '2px solid #e5e7eb',
                background: 'white',
                color: '#666',
                borderRadius: 8,
                cursor: loading ? 'not-allowed' : 'pointer',
                fontWeight: 500,
                transition: 'all 0.2s ease'
              }}
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={loading}
              style={{
                flex: 2,
                padding: '12px 16px',
                border: 'none',
                background: loading ? '#94a3b8' : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                borderRadius: 8,
                cursor: loading ? 'not-allowed' : 'pointer',
                fontWeight: 600,
                transition: 'all 0.2s ease'
              }}
            >
              {loading ? 'Salvando...' : (transaction ? 'Atualizar' : 'Criar Transação')}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}