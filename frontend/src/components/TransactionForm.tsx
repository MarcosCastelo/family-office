import React, { useState, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { X, DollarSign, Calendar, FileText, TrendingUp, TrendingDown } from 'lucide-react';
import { type Transaction } from '../services/transactions';
import { type Asset } from '../services/assets';
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

  // Prevenir scroll do body quando modal está aberta
  useEffect(() => {
    document.body.style.overflow = 'hidden';
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, []);

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
        asset_id: asset.id!,
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

  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onCancel();
    }
  };

  const modalContent = (
    <div 
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'rgba(0, 0, 0, 0.6)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 9999,
        padding: '20px'
      }}
      onClick={handleBackdropClick}
    >
      <div 
        style={{
          background: 'white',
          borderRadius: '16px',
          padding: '32px',
          maxWidth: '500px',
          width: '100%',
          maxHeight: '90vh',
          overflow: 'auto',
          boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
          position: 'relative',
          transform: 'scale(1)',
          transition: 'all 0.3s ease-out'
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'flex-start',
          marginBottom: '24px',
          gap: '16px'
        }}>
          <div style={{ flex: 1, minWidth: 0 }}>
            <h2 style={{ 
              margin: 0, 
              color: '#222', 
              fontSize: '24px', 
              fontWeight: 600,
              wordBreak: 'break-word'
            }}>
              {transaction ? 'Editar Transação' : 'Nova Transação'}
            </h2>
            <p style={{ 
              margin: '8px 0 0 0', 
              color: '#666', 
              fontSize: '16px',
              wordBreak: 'break-word'
            }}>
              Ativo: {asset.name}
            </p>
          </div>
          <button
            onClick={onCancel}
            style={{
              border: 'none',
              background: 'transparent',
              cursor: 'pointer',
              padding: '8px',
              borderRadius: '8px',
              color: '#666',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transition: 'all 0.2s ease'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = '#f3f4f6';
              e.currentTarget.style.color = '#374151';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'transparent';
              e.currentTarget.style.color = '#666';
            }}
          >
            <X size={24} />
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          {/* Tipo de Transação */}
          <div style={{ marginBottom: '24px' }}>
            <label style={{ display: 'block', marginBottom: '12px', fontWeight: 600, color: '#333', fontSize: '16px' }}>
              Tipo de Transação
            </label>
            <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
              <button
                type="button"
                onClick={() => setFormData({ ...formData, transaction_type: 'buy' })}
                style={{
                  flex: 1,
                  minWidth: '140px',
                  padding: '16px 20px',
                  border: `2px solid ${formData.transaction_type === 'buy' ? '#22c55e' : '#e5e7eb'}`,
                  background: formData.transaction_type === 'buy' ? '#f0fdf4' : 'white',
                  color: formData.transaction_type === 'buy' ? '#22c55e' : '#666',
                  borderRadius: '12px',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '8px',
                  fontWeight: 600,
                  fontSize: '16px',
                  transition: 'all 0.2s ease',
                  boxSizing: 'border-box'
                }}
              >
                <TrendingUp size={20} />
                Compra
              </button>
              <button
                type="button"
                onClick={() => setFormData({ ...formData, transaction_type: 'sell' })}
                style={{
                  flex: 1,
                  minWidth: '140px',
                  padding: '16px 20px',
                  border: `2px solid ${formData.transaction_type === 'sell' ? '#ef4444' : '#e5e7eb'}`,
                  background: formData.transaction_type === 'sell' ? '#fef2f2' : 'white',
                  color: formData.transaction_type === 'sell' ? '#ef4444' : '#666',
                  borderRadius: '12px',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '8px',
                  fontWeight: 600,
                  fontSize: '16px',
                  transition: 'all 0.2s ease',
                  boxSizing: 'border-box'
                }}
              >
                <TrendingDown size={20} />
                Venda
              </button>
            </div>
          </div>

          {/* Quantidade */}
          <div style={{ marginBottom: '24px' }}>
            <label style={{ display: 'block', marginBottom: '12px', fontWeight: 600, color: '#333', fontSize: '16px' }}>
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
                padding: '16px 20px',
                border: '2px solid #e5e7eb',
                borderRadius: '12px',
                fontSize: '16px',
                transition: 'all 0.2s ease',
                boxSizing: 'border-box',
                background: 'white'
              }}
              onFocus={e => {
                e.target.style.borderColor = '#667eea';
                e.target.style.boxShadow = '0 0 0 3px rgba(102, 126, 234, 0.1)';
              }}
              onBlur={e => {
                e.target.style.borderColor = '#e5e7eb';
                e.target.style.boxShadow = 'none';
              }}
            />
            {formData.transaction_type === 'sell' && asset.current_quantity !== undefined && (
              <p style={{ margin: '8px 0 0 0', fontSize: '14px', color: '#666' }}>
                Quantidade disponível: <strong>{asset.current_quantity}</strong>
              </p>
            )}
          </div>

          {/* Preço Unitário */}
          <div style={{ marginBottom: '24px' }}>
            <label style={{ display: 'block', marginBottom: '12px', fontWeight: 600, color: '#333', fontSize: '16px' }}>
              Preço Unitário
            </label>
            <div style={{ position: 'relative' }}>
              <DollarSign 
                size={20} 
                style={{ 
                  position: 'absolute', 
                  left: '16px', 
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
                  padding: '16px 20px 16px 48px',
                  border: '2px solid #e5e7eb',
                  borderRadius: '12px',
                  fontSize: '16px',
                  transition: 'all 0.2s ease',
                  boxSizing: 'border-box',
                  background: 'white'
                }}
                onFocus={e => {
                  e.target.style.borderColor = '#667eea';
                  e.target.style.boxShadow = '0 0 0 3px rgba(102, 126, 234, 0.1)';
                }}
                onBlur={e => {
                  e.target.style.borderColor = '#e5e7eb';
                  e.target.style.boxShadow = 'none';
                }}
              />
            </div>
          </div>

          {/* Valor Total */}
          {totalValue > 0 && (
            <div style={{
              padding: '20px',
              background: '#f8fafc',
              borderRadius: '12px',
              marginBottom: '24px',
              border: '2px solid #e2e8f0'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ color: '#666', fontSize: '16px', fontWeight: 500 }}>Valor Total:</span>
                <span style={{ 
                  fontWeight: 700, 
                  fontSize: '20px', 
                  color: formData.transaction_type === 'buy' ? '#22c55e' : '#ef4444' 
                }}>
                  {formatCurrency(totalValue)}
                </span>
              </div>
            </div>
          )}

          {/* Data da Transação */}
          <div style={{ marginBottom: '24px' }}>
            <label style={{ display: 'block', marginBottom: '12px', fontWeight: 600, color: '#333', fontSize: '16px' }}>
              Data da Transação
            </label>
            <div style={{ position: 'relative' }}>
              <Calendar 
                size={20} 
                style={{ 
                  position: 'absolute', 
                  left: '16px', 
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
                  padding: '16px 20px 16px 48px',
                  border: '2px solid #e5e7eb',
                  borderRadius: '12px',
                  fontSize: '16px',
                  transition: 'all 0.2s ease',
                  boxSizing: 'border-box',
                  background: 'white'
                }}
                onFocus={e => {
                  e.target.style.borderColor = '#667eea';
                  e.target.style.boxShadow = '0 0 0 3px rgba(102, 126, 234, 0.1)';
                }}
                onBlur={e => {
                  e.target.style.borderColor = '#e5e7eb';
                  e.target.style.boxShadow = 'none';
                }}
              />
            </div>
          </div>

          {/* Descrição */}
          <div style={{ marginBottom: '32px' }}>
            <label style={{ display: 'block', marginBottom: '12px', fontWeight: 600, color: '#333', fontSize: '16px' }}>
              Descrição (opcional)
            </label>
            <div style={{ position: 'relative' }}>
              <FileText 
                size={20} 
                style={{ 
                  position: 'absolute', 
                  left: '16px', 
                  top: '20px', 
                  color: '#666' 
                }} 
              />
              <textarea
                value={formData.description}
                onChange={e => setFormData({ ...formData, description: e.target.value })}
                placeholder="Adicione uma descrição..."
                style={{
                  width: '100%',
                  padding: '16px 20px 16px 48px',
                  border: '2px solid #e5e7eb',
                  borderRadius: '12px',
                  fontSize: '16px',
                  minHeight: '100px',
                  resize: 'vertical',
                  fontFamily: 'inherit',
                  transition: 'all 0.2s ease',
                  boxSizing: 'border-box',
                  background: 'white'
                }}
                onFocus={e => {
                  e.target.style.borderColor = '#667eea';
                  e.target.style.boxShadow = '0 0 0 3px rgba(102, 126, 234, 0.1)';
                }}
                onBlur={e => {
                  e.target.style.borderColor = '#e5e7eb';
                  e.target.style.boxShadow = 'none';
                }}
              />
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div style={{
              padding: '16px',
              background: '#fef2f2',
              border: '2px solid #fecaca',
              borderRadius: '12px',
              color: '#dc2626',
              marginBottom: '24px',
              fontSize: '16px',
              fontWeight: 500
            }}>
              {error}
            </div>
          )}

          {/* Buttons */}
          <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
            <button
              type="button"
              onClick={onCancel}
              disabled={loading}
              style={{
                flex: 1,
                minWidth: '120px',
                padding: '16px 24px',
                border: '2px solid #e5e7eb',
                background: 'white',
                color: '#666',
                borderRadius: '12px',
                cursor: loading ? 'not-allowed' : 'pointer',
                fontWeight: 600,
                fontSize: '16px',
                transition: 'all 0.2s ease',
                boxSizing: 'border-box'
              }}
              onMouseEnter={(e) => {
                if (!loading) {
                  e.currentTarget.style.background = '#f8f9fa';
                  e.currentTarget.style.borderColor = '#d1d5db';
                }
              }}
              onMouseLeave={(e) => {
                if (!loading) {
                  e.currentTarget.style.background = 'white';
                  e.currentTarget.style.borderColor = '#e5e7eb';
                }
              }}
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={loading}
              style={{
                flex: 2,
                minWidth: '180px',
                padding: '16px 24px',
                border: 'none',
                background: loading ? '#94a3b8' : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                borderRadius: '12px',
                cursor: loading ? 'not-allowed' : 'pointer',
                fontWeight: 600,
                fontSize: '16px',
                transition: 'all 0.2s ease',
                boxSizing: 'border-box'
              }}
              onMouseEnter={(e) => {
                if (!loading) {
                  e.currentTarget.style.transform = 'translateY(-1px)';
                  e.currentTarget.style.boxShadow = '0 10px 25px rgba(102, 126, 234, 0.3)';
                }
              }}
              onMouseLeave={(e) => {
                if (!loading) {
                  e.currentTarget.style.transform = 'translateY(0)';
                  e.currentTarget.style.boxShadow = 'none';
                }
              }}
            >
              {loading ? 'Salvando...' : (transaction ? 'Atualizar' : 'Criar Transação')}
            </button>
          </div>
        </form>
      </div>
    </div>
  );

  // Renderizar no body usando createPortal
  return createPortal(modalContent, document.body);
}