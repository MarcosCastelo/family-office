import React from 'react';
import { 
  TrendingUp, 
  TrendingDown, 
  DollarSign, 
  Target, 
  Activity,
  BarChart3,
  Percent
} from 'lucide-react';
import { TransactionSummary as TSummary } from '../services/transactions';

interface TransactionSummaryProps {
  summary: TSummary;
  assetName: string;
  loading: boolean;
}

export default function TransactionSummary({ summary, assetName, loading }: TransactionSummaryProps) {
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  const formatNumber = (value: number, decimals: number = 2) => {
    return new Intl.NumberFormat('pt-BR', {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals
    }).format(value);
  };

  const getGainLossColor = (value: number) => {
    if (value > 0) return '#22c55e';
    if (value < 0) return '#ef4444';
    return '#666';
  };

  const getGainLossIcon = (value: number) => {
    if (value > 0) return <TrendingUp size={20} />;
    if (value < 0) return <TrendingDown size={20} />;
    return <Target size={20} />;
  };

  if (loading) {
    return (
      <div style={{
        background: 'white',
        borderRadius: 16,
        padding: 24,
        boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: 200
      }}>
        <div style={{ color: '#666', textAlign: 'center' }}>
          <Activity size={32} style={{ marginBottom: 8, opacity: 0.6 }} />
          <div>Carregando resumo...</div>
        </div>
      </div>
    );
  }

  const metrics = [
    {
      label: 'Quantidade Atual',
      value: formatNumber(summary.current_quantity, 6),
      icon: <BarChart3 size={20} />,
      color: '#667eea',
      background: '#f0f4ff'
    },
    {
      label: 'Valor Atual',
      value: formatCurrency(summary.current_value),
      icon: <DollarSign size={20} />,
      color: '#667eea',
      background: '#f0f4ff'
    },
    {
      label: 'Custo Médio',
      value: formatCurrency(summary.average_cost),
      icon: <Target size={20} />,
      color: '#8b5cf6',
      background: '#faf5ff'
    },
    {
      label: 'Total Investido',
      value: formatCurrency(summary.total_invested),
      icon: <TrendingUp size={20} />,
      color: '#22c55e',
      background: '#f0fdf4'
    },
    {
      label: 'Total Desinvestido',
      value: formatCurrency(summary.total_divested),
      icon: <TrendingDown size={20} />,
      color: '#f59e0b',
      background: '#fffbeb'
    },
    {
      label: 'Ganho/Perda Realizado',
      value: formatCurrency(summary.realized_gain_loss),
      icon: getGainLossIcon(summary.realized_gain_loss),
      color: getGainLossColor(summary.realized_gain_loss),
      background: summary.realized_gain_loss > 0 ? '#f0fdf4' : summary.realized_gain_loss < 0 ? '#fef2f2' : '#f8fafc'
    },
    {
      label: 'Ganho/Perda Não Realizado',
      value: formatCurrency(summary.unrealized_gain_loss),
      icon: getGainLossIcon(summary.unrealized_gain_loss),
      color: getGainLossColor(summary.unrealized_gain_loss),
      background: summary.unrealized_gain_loss > 0 ? '#f0fdf4' : summary.unrealized_gain_loss < 0 ? '#fef2f2' : '#f8fafc'
    },
    {
      label: 'Total de Transações',
      value: summary.transaction_count.toString(),
      icon: <Activity size={20} />,
      color: '#64748b',
      background: '#f8fafc'
    }
  ];

  return (
    <div style={{
      background: 'white',
      borderRadius: 16,
      padding: 24,
      boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
      marginBottom: 24
    }}>
      {/* Header */}
      <div style={{ marginBottom: 24 }}>
        <h3 style={{ 
          margin: 0, 
          color: '#222', 
          fontSize: 20, 
          fontWeight: 600,
          display: 'flex',
          alignItems: 'center',
          gap: 12
        }}>
          <div style={{
            width: 40,
            height: 40,
            borderRadius: '50%',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'white'
          }}>
            <BarChart3 size={20} />
          </div>
          Resumo de Transações - {assetName}
        </h3>
        <p style={{ margin: '8px 0 0 52px', color: '#666', fontSize: 14 }}>
          Análise consolidada das transações deste ativo
        </p>
      </div>

      {/* Métricas */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
        gap: 16
      }}>
        {metrics.map((metric, index) => (
          <div
            key={index}
            style={{
              padding: 20,
              background: metric.background,
              borderRadius: 12,
              border: `1px solid ${metric.color}20`,
              transition: 'all 0.2s ease'
            }}
            onMouseEnter={e => {
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.boxShadow = '0 8px 24px rgba(0,0,0,0.1)';
            }}
            onMouseLeave={e => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = 'none';
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div style={{ flex: 1 }}>
                <div style={{ 
                  fontSize: 12, 
                  color: '#64748b', 
                  fontWeight: 500, 
                  marginBottom: 8,
                  textTransform: 'uppercase',
                  letterSpacing: '0.5px'
                }}>
                  {metric.label}
                </div>
                <div style={{ 
                  fontSize: 18, 
                  fontWeight: 700, 
                  color: metric.color 
                }}>
                  {metric.value}
                </div>
              </div>
              <div style={{
                width: 48,
                height: 48,
                borderRadius: '50%',
                background: `${metric.color}15`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: metric.color
              }}>
                {metric.icon}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Rentabilidade */}
      {summary.current_value > 0 && summary.total_invested > 0 && (
        <div style={{
          marginTop: 24,
          padding: 20,
          background: 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)',
          borderRadius: 12,
          border: '1px solid #e2e8f0'
        }}>
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'space-between',
            flexWrap: 'wrap',
            gap: 16
          }}>
            <div>
              <div style={{ 
                fontSize: 14, 
                color: '#64748b', 
                fontWeight: 500, 
                marginBottom: 4 
              }}>
                Rentabilidade Total
              </div>
              <div style={{ fontSize: 16, color: '#475569' }}>
                Baseada no valor atual vs. investimento total
              </div>
            </div>
            <div style={{ 
              display: 'flex', 
              alignItems: 'center', 
              gap: 12,
              padding: '12px 20px',
              background: 'white',
              borderRadius: 8,
              boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
            }}>
              <Percent size={20} color="#667eea" />
              <div>
                <div style={{ 
                  fontSize: 20, 
                  fontWeight: 700, 
                  color: getGainLossColor(summary.current_value - summary.total_invested)
                }}>
                  {formatNumber(((summary.current_value / summary.total_invested) - 1) * 100, 2)}%
                </div>
                <div style={{ fontSize: 12, color: '#64748b' }}>
                  ({formatCurrency(summary.current_value - summary.total_invested)})
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}