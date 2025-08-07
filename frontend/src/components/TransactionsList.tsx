import React, { useState } from 'react';
import { 
  Edit, 
  Trash2, 
  TrendingUp, 
  TrendingDown, 
  Calendar, 
  DollarSign,
  FileText,
  MoreHorizontal,
  Filter,
  Search
} from 'lucide-react';
import { type Transaction } from '../services/transactions';

interface TransactionsListProps {
  transactions: Transaction[];
  onEdit: (transaction: Transaction) => void;
  onDelete: (transactionId: number) => void;
  loading: boolean;
}

export default function TransactionsList({ transactions, onEdit, onDelete, loading }: TransactionsListProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState<'all' | 'buy' | 'sell'>('all');
  const [sortBy, setSortBy] = useState<'date' | 'value' | 'quantity'>('date');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR');
  };

  const formatDateTime = (dateString: string) => {
    return new Date(dateString).toLocaleString('pt-BR');
  };

  // Filtrar e ordenar transações
  const filteredTransactions = transactions
    .filter(transaction => {
      const matchesSearch = !searchTerm || 
        transaction.description?.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesType = filterType === 'all' || transaction.transaction_type === filterType;
      return matchesSearch && matchesType;
    })
    .sort((a, b) => {
      let aValue: any, bValue: any;
      
      switch (sortBy) {
        case 'date':
          aValue = new Date(a.transaction_date);
          bValue = new Date(b.transaction_date);
          break;
        case 'value':
          aValue = a.total_value || (a.quantity * a.unit_price);
          bValue = b.total_value || (b.quantity * b.unit_price);
          break;
        case 'quantity':
          aValue = a.quantity;
          bValue = b.quantity;
          break;
        default:
          return 0;
      }

      if (sortOrder === 'asc') {
        return aValue > bValue ? 1 : -1;
      } else {
        return aValue < bValue ? 1 : -1;
      }
    });

  if (loading) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        padding: 40,
        color: '#666'
      }}>
        Carregando transações...
      </div>
    );
  }

  return (
    <div>
      {/* Filtros */}
      <div style={{
        display: 'flex',
        gap: 16,
        marginBottom: 24,
        padding: 16,
        background: '#f8fafc',
        borderRadius: 12,
      }}>
        {/* Busca */}
        <div style={{ position: 'relative', minWidth: 200, marginRight: 64 }}>
          <Search size={18} style={{
            position: 'absolute',
            left: 12,
            top: '50%',
            transform: 'translateY(-50%)',
            color: '#666'
          }} />
          <input
            type="text"
            placeholder="Buscar por descrição..."
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
            style={{
              width: '100%',
              padding: '8px 12px 8px 40px',
              border: '1px solid #e2e8f0',
              borderRadius: 8,
              fontSize: 14
            }}
          />
        </div>

        {/* Filtro por tipo */}
        <select
          value={filterType}
          onChange={e => setFilterType(e.target.value as 'all' | 'buy' | 'sell')}
          style={{
            padding: '8px 12px',
            border: '1px solid #e2e8f0',
            borderRadius: 8,
            fontSize: 14,
            background: 'white'
          }}
        >
          <option value="all">Todos os tipos</option>
          <option value="buy">Compras</option>
          <option value="sell">Vendas</option>
        </select>

        {/* Ordenação */}
        <select
          value={`${sortBy}-${sortOrder}`}
          onChange={e => {
            const [newSortBy, newSortOrder] = e.target.value.split('-');
            setSortBy(newSortBy as 'date' | 'value' | 'quantity');
            setSortOrder(newSortOrder as 'asc' | 'desc');
          }}
          style={{
            padding: '8px 12px',
            border: '1px solid #e2e8f0',
            borderRadius: 8,
            fontSize: 14,
            background: 'white'
          }}
        >
          <option value="date-desc">Data (mais recente)</option>
          <option value="date-asc">Data (mais antiga)</option>
          <option value="value-desc">Valor (maior)</option>
          <option value="value-asc">Valor (menor)</option>
          <option value="quantity-desc">Quantidade (maior)</option>
          <option value="quantity-asc">Quantidade (menor)</option>
        </select>
      </div>

      {/* Lista de Transações */}
      {filteredTransactions.length === 0 ? (
        <div style={{
          textAlign: 'center',
          padding: 40,
          color: '#666',
          background: '#f8fafc',
          borderRadius: 12,
          border: '2px dashed #e2e8f0'
        }}>
          <MoreHorizontal size={48} style={{ marginBottom: 16, opacity: 0.5 }} />
          <p style={{ margin: 0, fontSize: 16 }}>
            {transactions.length === 0 
              ? 'Nenhuma transação encontrada'
              : 'Nenhuma transação corresponde aos filtros aplicados'
            }
          </p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
          {filteredTransactions.map(transaction => (
            <div
              key={transaction.id}
              style={{
                background: 'white',
                border: '1px solid #e2e8f0',
                borderRadius: 12,
                padding: 20,
                transition: 'all 0.2s ease',
                boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
              }}
              onMouseEnter={e => {
                e.currentTarget.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
                e.currentTarget.style.transform = 'translateY(-1px)';
              }}
              onMouseLeave={e => {
                e.currentTarget.style.boxShadow = '0 1px 3px rgba(0,0,0,0.1)';
                e.currentTarget.style.transform = 'translateY(0)';
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                {/* Informações principais */}
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 8 }}>
                    {/* Ícone do tipo */}
                    <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      width: 40,
                      height: 40,
                      borderRadius: '50%',
                      background: transaction.transaction_type === 'buy' 
                        ? 'linear-gradient(135deg, #10b981 0%, #22c55e 100%)'
                        : 'linear-gradient(135deg, #ef4444 0%, #f87171 100%)',
                      color: 'white'
                    }}>
                      {transaction.transaction_type === 'buy' ? 
                        <TrendingUp size={20} /> : 
                        <TrendingDown size={20} />
                      }
                    </div>

                    {/* Tipo e quantidade */}
                    <div>
                      <div style={{ 
                        fontWeight: 600, 
                        fontSize: 16, 
                        color: '#222',
                        marginBottom: 2
                      }}>
                        {transaction.transaction_type === 'buy' ? 'Compra' : 'Venda'} - {transaction.quantity}
                      </div>
                      <div style={{ fontSize: 14, color: '#666' }}>
                        {formatCurrency(transaction.unit_price)} por unidade
                      </div>
                    </div>
                  </div>

                  {/* Detalhes adicionais */}
                  <div style={{ 
                    display: 'grid', 
                    gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
                    gap: 16,
                    marginTop: 12
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                      <DollarSign size={16} color="#666" />
                      <div>
                        <div style={{ fontSize: 12, color: '#666' }}>Valor Total</div>
                        <div style={{ fontWeight: 600, color: '#222' }}>
                          {formatCurrency(transaction.total_value || (transaction.quantity * transaction.unit_price))}
                        </div>
                      </div>
                    </div>

                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                      <Calendar size={16} color="#666" />
                      <div>
                        <div style={{ fontSize: 12, color: '#666' }}>Data</div>
                        <div style={{ fontWeight: 500, color: '#222' }}>
                          {formatDate(transaction.transaction_date)}
                        </div>
                      </div>
                    </div>

                    {transaction.description && (
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        <FileText size={16} color="#666" />
                        <div>
                          <div style={{ fontSize: 12, color: '#666' }}>Descrição</div>
                          <div style={{ fontWeight: 500, color: '#222' }}>
                            {transaction.description}
                          </div>
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Data de criação */}
                  {transaction.created_at && (
                    <div style={{ 
                      fontSize: 12, 
                      color: '#94a3b8', 
                      marginTop: 12,
                      paddingTop: 12,
                      borderTop: '1px solid #f1f5f9'
                    }}>
                      Criado em {formatDateTime(transaction.created_at)}
                    </div>
                  )}
                </div>

                {/* Ações */}
                <div style={{ display: 'flex', gap: 8, marginLeft: 16 }}>
                  <button
                    onClick={() => onEdit(transaction)}
                    style={{
                      padding: '8px 12px',
                      border: '1px solid #e2e8f0',
                      background: 'white',
                      color: '#667eea',
                      borderRadius: 8,
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      gap: 6,
                      fontSize: 14,
                      fontWeight: 500,
                      transition: 'all 0.2s ease'
                    }}
                    onMouseEnter={e => {
                      e.currentTarget.style.background = '#667eea';
                      e.currentTarget.style.color = 'white';
                    }}
                    onMouseLeave={e => {
                      e.currentTarget.style.background = 'white';
                      e.currentTarget.style.color = '#667eea';
                    }}
                    title="Editar transação"
                  >
                    <Edit size={16} />
                    Editar
                  </button>

                  <button
                    onClick={() => transaction.id && onDelete(transaction.id)}
                    style={{
                      padding: '8px 12px',
                      border: '1px solid #fecaca',
                      background: 'white',
                      color: '#ef4444',
                      borderRadius: 8,
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      gap: 6,
                      fontSize: 14,
                      fontWeight: 500,
                      transition: 'all 0.2s ease'
                    }}
                    onMouseEnter={e => {
                      e.currentTarget.style.background = '#ef4444';
                      e.currentTarget.style.color = 'white';
                    }}
                    onMouseLeave={e => {
                      e.currentTarget.style.background = 'white';
                      e.currentTarget.style.color = '#ef4444';
                    }}
                    title="Excluir transação"
                  >
                    <Trash2 size={16} />
                    Excluir
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}