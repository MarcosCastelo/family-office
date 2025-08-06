import React, { useState, useEffect } from 'react';
import { 
  Plus, 
  Search, 
  Activity, 
  BarChart3,
  ArrowLeft,
  RefreshCw,
  AlertCircle
} from 'lucide-react';
import { useFamily } from '../contexts/FamilyContext';
import { useToast } from '../components/Toast';
import { getAssets, Asset } from '../services/assets';
import { 
  getTransactions, 
  createTransaction, 
  updateTransaction, 
  deleteTransaction,
  getTransactionSummary,
  Transaction,
  TransactionSummary as TSummary
} from '../services/transactions';
import TransactionForm from '../components/TransactionForm';
import TransactionsList from '../components/TransactionsList';
import TransactionSummary from '../components/TransactionSummary';

interface TransactionsProps {
  selectedAssetId?: number | null;
}

export default function Transactions({ selectedAssetId: initialAssetId }: TransactionsProps) {
  const { selectedFamilyId } = useFamily();
  const { showToast } = useToast();
  const [assets, setAssets] = useState<Asset[]>([]);
  const [selectedAsset, setSelectedAsset] = useState<Asset | null>(null);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [summary, setSummary] = useState<TSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // Form states
  const [showForm, setShowForm] = useState(false);
  const [editingTransaction, setEditingTransaction] = useState<Transaction | null>(null);

  // Load assets on family change
  useEffect(() => {
    if (selectedFamilyId) {
      loadAssets();
    }
  }, [selectedFamilyId]);

  // Auto-select asset if provided via prop
  useEffect(() => {
    if (initialAssetId && assets.length > 0) {
      const asset = assets.find(a => a.id === initialAssetId);
      if (asset && !selectedAsset) {
        setSelectedAsset(asset);
      }
    }
  }, [initialAssetId, assets, selectedAsset]);

  // Load transactions when asset is selected
  useEffect(() => {
    if (selectedAsset) {
      loadTransactions();
      loadSummary();
    }
  }, [selectedAsset]);

  const loadAssets = async () => {
    if (!selectedFamilyId) return;
    
    try {
      setLoading(true);
      setError(null);
      const assetsData = await getAssets(selectedFamilyId);
      setAssets(assetsData);
    } catch (err: any) {
      console.error('Erro ao carregar ativos:', err);
      setError(err.response?.data?.error || 'Erro ao carregar ativos');
    } finally {
      setLoading(false);
    }
  };

  const loadTransactions = async () => {
    if (!selectedAsset) return;
    
    try {
      setLoading(true);
      setError(null);
      const transactionsData = await getTransactions(selectedAsset.id);
      setTransactions(transactionsData);
    } catch (err: any) {
      console.error('Erro ao carregar transações:', err);
      setError(err.response?.data?.error || 'Erro ao carregar transações');
    } finally {
      setLoading(false);
    }
  };

  const loadSummary = async () => {
    if (!selectedAsset) return;
    
    try {
      const summaryData = await getTransactionSummary(selectedAsset.id);
      setSummary(summaryData);
    } catch (err: any) {
      console.error('Erro ao carregar resumo:', err);
      // Don't set error for summary - it's optional
    }
  };

  const handleCreateTransaction = async (transactionData: Omit<Transaction, 'id' | 'total_value' | 'created_at' | 'updated_at'>) => {
    try {
      setSubmitting(true);
      await createTransaction(transactionData);
      showToast('Transação criada com sucesso!', 'success');
      setShowForm(false);
      loadTransactions();
      loadSummary();
    } catch (err: any) {
      throw err; // Let the form handle the error
    } finally {
      setSubmitting(false);
    }
  };

  const handleUpdateTransaction = async (transactionData: Omit<Transaction, 'id' | 'total_value' | 'created_at' | 'updated_at'>) => {
    if (!editingTransaction) return;
    
    try {
      setSubmitting(true);
      await updateTransaction(editingTransaction.id!, transactionData);
      showToast('Transação atualizada com sucesso!', 'success');
      setShowForm(false);
      setEditingTransaction(null);
      loadTransactions();
      loadSummary();
    } catch (err: any) {
      throw err; // Let the form handle the error
    } finally {
      setSubmitting(false);
    }
  };

  const handleDeleteTransaction = async (transactionId: number) => {
    if (!confirm('Tem certeza que deseja excluir esta transação?')) return;
    
    try {
      setLoading(true);
      await deleteTransaction(transactionId);
      showToast('Transação excluída com sucesso!', 'success');
      loadTransactions();
      loadSummary();
    } catch (err: any) {
      showToast(err.response?.data?.error || 'Erro ao excluir transação', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleEditTransaction = (transaction: Transaction) => {
    setEditingTransaction(transaction);
    setShowForm(true);
  };

  const handleRefresh = () => {
    if (selectedAsset) {
      loadTransactions();
      loadSummary();
    } else {
      loadAssets();
    }
  };

  const clearMessages = () => {
    setError(null);
    setSuccess(null);
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  // Clear messages after 5 seconds
  useEffect(() => {
    if (success || error) {
      const timer = setTimeout(clearMessages, 5000);
      return () => clearTimeout(timer);
    }
  }, [success, error]);

  if (!selectedFamilyId) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '400px',
        color: '#666',
        textAlign: 'center'
      }}>
        <div>
          <AlertCircle size={48} style={{ marginBottom: 16, opacity: 0.6 }} />
          <p style={{ margin: 0, fontSize: 16 }}>
            Selecione uma família para gerenciar transações
          </p>
        </div>
      </div>
    );
  }

  return (
    <div>
      {/* Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 24
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
          {selectedAsset && (
            <button
              onClick={() => {
                setSelectedAsset(null);
                setTransactions([]);
                setSummary(null);
              }}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 8,
                padding: '8px 12px',
                border: '1px solid #e2e8f0',
                background: 'white',
                color: '#667eea',
                borderRadius: 8,
                cursor: 'pointer',
                fontSize: 14,
                fontWeight: 500
              }}
            >
              <ArrowLeft size={16} />
              Voltar aos Ativos
            </button>
          )}
          
          <div>
            <h1 style={{ 
              margin: 0, 
              color: '#222', 
              fontSize: 28, 
              fontWeight: 700,
              display: 'flex',
              alignItems: 'center',
              gap: 12
            }}>
              <Activity size={32} color="#667eea" />
              {selectedAsset ? `Transações - ${selectedAsset.name}` : 'Transações'}
            </h1>
            <p style={{ margin: '4px 0 0 44px', color: '#666', fontSize: 16 }}>
              {selectedAsset 
                ? 'Gerencie as transações deste ativo'
                : 'Selecione um ativo para gerenciar suas transações'
              }
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', gap: 12 }}>
          <button
            onClick={handleRefresh}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 8,
              padding: '12px 16px',
              border: '1px solid #e2e8f0',
              background: 'white',
              color: '#667eea',
              borderRadius: 8,
              cursor: 'pointer',
              fontSize: 14,
              fontWeight: 500
            }}
          >
            <RefreshCw size={16} />
            Atualizar
          </button>

          {selectedAsset && (
            <button
              onClick={() => setShowForm(true)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 8,
                padding: '12px 20px',
                border: 'none',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                borderRadius: 8,
                cursor: 'pointer',
                fontSize: 14,
                fontWeight: 600,
                boxShadow: '0 4px 12px rgba(102, 126, 234, 0.3)'
              }}
            >
              <Plus size={18} />
              Nova Transação
            </button>
          )}
        </div>
      </div>

      {/* Messages */}
      {(error || success) && (
        <div style={{
          padding: 16,
          borderRadius: 8,
          marginBottom: 24,
          background: error ? '#fef2f2' : '#f0fdf4',
          border: `1px solid ${error ? '#fecaca' : '#bbf7d0'}`,
          color: error ? '#dc2626' : '#16a34a',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <span>{error || success}</span>
          <button
            onClick={clearMessages}
            style={{
              border: 'none',
              background: 'transparent',
              cursor: 'pointer',
              padding: 4,
              borderRadius: 4,
              color: 'inherit'
            }}
          >
            ×
          </button>
        </div>
      )}

      {/* Content */}
      {!selectedAsset ? (
        /* Asset Selection */
        <div>
          <div style={{
            background: 'white',
            borderRadius: 16,
            padding: 24,
            boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
          }}>
            <h3 style={{ 
              margin: '0 0 16px 0', 
              color: '#222', 
              fontSize: 20, 
              fontWeight: 600 
            }}>
              Selecione um Ativo
            </h3>
            <p style={{ margin: '0 0 20px 0', color: '#666' }}>
              Escolha um ativo para visualizar e gerenciar suas transações
            </p>

            {loading ? (
              <div style={{ textAlign: 'center', padding: 40, color: '#666' }}>
                Carregando ativos...
              </div>
            ) : assets.length === 0 ? (
              <div style={{
                textAlign: 'center',
                padding: 40,
                color: '#666',
                background: '#f8fafc',
                borderRadius: 12,
                border: '2px dashed #e2e8f0'
              }}>
                <BarChart3 size={48} style={{ marginBottom: 16, opacity: 0.5 }} />
                <p style={{ margin: 0, fontSize: 16 }}>
                  Nenhum ativo encontrado
                </p>
              </div>
            ) : (
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
                gap: 16
              }}>
                {assets.map(asset => (
                  <div
                    key={asset.id}
                    onClick={() => setSelectedAsset(asset)}
                    style={{
                      padding: 20,
                      border: '1px solid #e2e8f0',
                      borderRadius: 12,
                      cursor: 'pointer',
                      transition: 'all 0.2s ease',
                      background: 'white'
                    }}
                    onMouseEnter={e => {
                      e.currentTarget.style.boxShadow = '0 8px 24px rgba(0,0,0,0.1)';
                      e.currentTarget.style.transform = 'translateY(-2px)';
                      e.currentTarget.style.borderColor = '#667eea';
                    }}
                    onMouseLeave={e => {
                      e.currentTarget.style.boxShadow = 'none';
                      e.currentTarget.style.transform = 'translateY(0)';
                      e.currentTarget.style.borderColor = '#e2e8f0';
                    }}
                  >
                    <div style={{ marginBottom: 12 }}>
                      <h4 style={{ 
                        margin: 0, 
                        color: '#222', 
                        fontSize: 16, 
                        fontWeight: 600 
                      }}>
                        {asset.name}
                      </h4>
                      <p style={{ 
                        margin: '4px 0 0 0', 
                        color: '#666', 
                        fontSize: 14,
                        textTransform: 'capitalize'
                      }}>
                        {asset.asset_type.replace('_', ' ')}
                      </p>
                    </div>
                    
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <div>
                        {asset.current_value !== undefined ? (
                          <div>
                            <div style={{ fontSize: 12, color: '#666' }}>Valor Atual</div>
                            <div style={{ fontWeight: 600, color: '#22c55e' }}>
                              {formatCurrency(asset.current_value)}
                            </div>
                          </div>
                        ) : asset.value !== undefined ? (
                          <div>
                            <div style={{ fontSize: 12, color: '#666' }}>Valor</div>
                            <div style={{ fontWeight: 600, color: '#667eea' }}>
                              {formatCurrency(asset.value)}
                            </div>
                          </div>
                        ) : null}
                      </div>
                      
                      {asset.current_quantity !== undefined && (
                        <div style={{ textAlign: 'right' }}>
                          <div style={{ fontSize: 12, color: '#666' }}>Quantidade</div>
                          <div style={{ fontWeight: 600, color: '#222' }}>
                            {asset.current_quantity}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      ) : (
        /* Transactions View */
        <div>
          {/* Summary */}
          {summary && (
            <TransactionSummary 
              summary={summary}
              assetName={selectedAsset.name}
              loading={false}
            />
          )}

          {/* Transactions List */}
          <div style={{
            background: 'white',
            borderRadius: 16,
            padding: 24,
            boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
          }}>
            <h3 style={{ 
              margin: '0 0 20px 0', 
              color: '#222', 
              fontSize: 20, 
              fontWeight: 600 
            }}>
              Histórico de Transações
            </h3>

            <TransactionsList
              transactions={transactions}
              onEdit={handleEditTransaction}
              onDelete={handleDeleteTransaction}
              loading={loading}
            />
          </div>
        </div>
      )}

      {/* Transaction Form Modal */}
      {showForm && selectedAsset && (
        <TransactionForm
          asset={selectedAsset}
          transaction={editingTransaction || undefined}
          onSubmit={editingTransaction ? handleUpdateTransaction : handleCreateTransaction}
          onCancel={() => {
            setShowForm(false);
            setEditingTransaction(null);
          }}
          loading={submitting}
        />
      )}
    </div>
  );
}