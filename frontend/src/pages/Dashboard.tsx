import React, { useState, useEffect } from 'react';
import { 
  TrendingUp, 
  DollarSign, 
  PieChart, 
  AlertTriangle, 
  Target,
  Activity,
  Users,
  BarChart3,
  LayoutDashboard
} from 'lucide-react';
import { getDashboardData } from '../services/dashboard';
import { useFamily } from '../contexts/FamilyContext';

interface DashboardData {
  valor_total: number;
  num_ativos: number;
  distribuicao_classes: Array<{ classe: string; valor: number }>;
  top_ativos: Array<{ 
    id: number; 
    name: string; 
    value?: number; // Legacy field
    current_value?: number; // New dynamic field
    current_quantity?: number;
    transaction_count?: number;
    asset_type: string 
  }>;
  alertas_recentes: Array<{ tipo: string; mensagem: string; severidade: string; criado_em: string }>;
  score_risco: { score_global: number; classificacao_final: string };
  // New transaction-related fields
  total_invested?: number;
  total_divested?: number;
  total_transactions?: number;
  recent_transactions?: Array<{
    id: number;
    asset_name: string;
    transaction_type: string;
    quantity: number;
    unit_price: number;
    total_value: number;
    transaction_date: string;
  }>;
}

export default function Dashboard() {
  const { selectedFamilyId } = useFamily();
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (selectedFamilyId) {
      loadDashboardData();
    }
  }, [selectedFamilyId]);

  const loadDashboardData = async () => {
    if (!selectedFamilyId) return;
    
    try {
      setLoading(true);
      setError(null);
      const data = await getDashboardData(selectedFamilyId);
      setDashboardData(data);
    } catch (err: any) {
      console.error('Erro ao carregar dados do dashboard:', err);
      setError(err.response?.data?.error || 'Erro ao carregar dados do dashboard');
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  const getRiskColor = (classification: string) => {
    switch (classification.toLowerCase()) {
      case 'crítico':
        return '#d32f2f';
      case 'alto':
        return '#f57c00';
      case 'médio':
        return '#fbc02d';
      case 'baixo':
        return '#388e3c';
      default:
        return '#666';
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'crítico':
        return '#d32f2f';
      case 'alto':
        return '#f57c00';
      case 'médio':
        return '#fbc02d';
      case 'baixo':
        return '#388e3c';
      default:
        return '#666';
    }
  };

  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '400px',
        color: '#666'
      }}>
        <div style={{ textAlign: 'center' }}>
          <Activity size={48} style={{ marginBottom: 16, opacity: 0.6 }} />
          <div>Carregando dados...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '400px',
        color: '#d32f2f'
      }}>
        <div style={{ textAlign: 'center' }}>
          <AlertTriangle size={48} style={{ marginBottom: 16 }} />
          <div>Erro: {error}</div>
        </div>
      </div>
    );
  }

  if (!selectedFamilyId) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '400px',
        color: '#666'
      }}>
        <div style={{ textAlign: 'center' }}>
          <Users size={48} style={{ marginBottom: 16, opacity: 0.6 }} />
          <div>Selecione uma família para visualizar o dashboard.</div>
        </div>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto' }}>
      <div style={{ marginBottom: 32 }}>
        <h1 style={{ 
          color: '#222', 
          marginBottom: 16, 
          fontSize: '28px',
          fontWeight: 600,
          display: 'flex',
          alignItems: 'center',
          gap: 12
        }}>
          <LayoutDashboard size={28} />
          Dashboard
        </h1>
      </div>

      {dashboardData && (
        <div style={{ display: 'grid', gap: 24 }}>
          {/* Cards de Resumo */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: 20 }}>
            {/* Valor Total */}
            <div style={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              padding: 24,
              borderRadius: 16,
              boxShadow: '0 8px 32px rgba(102, 126, 234, 0.3)'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 8 }}>
                <DollarSign size={24} />
                <span style={{ fontSize: 14, opacity: 0.9 }}>Valor Total</span>
              </div>
              <div style={{ fontSize: '28px', fontWeight: 700 }}>
                {formatCurrency(dashboardData.valor_total)}
              </div>
            </div>

            {/* Número de Ativos */}
            <div style={{
              background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
              color: 'white',
              padding: 24,
              borderRadius: 16,
              boxShadow: '0 8px 32px rgba(240, 147, 251, 0.3)'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 8 }}>
                <PieChart size={24} />
                <span style={{ fontSize: 14, opacity: 0.9 }}>Total de Ativos</span>
              </div>
              <div style={{ fontSize: '28px', fontWeight: 700 }}>
                {dashboardData.num_ativos}
              </div>
            </div>

            {/* Score de Risco */}
            <div style={{
              background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
              color: 'white',
              padding: 24,
              borderRadius: 16,
              boxShadow: '0 8px 32px rgba(79, 172, 254, 0.3)'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 8 }}>
                <Target size={24} />
                <span style={{ fontSize: 14, opacity: 0.9 }}>Score de Risco</span>
              </div>
              <div style={{ fontSize: '28px', fontWeight: 700 }}>
                {dashboardData.score_risco.score_global}
              </div>
              <div style={{ fontSize: 14, opacity: 0.9, textTransform: 'capitalize' }}>
                {dashboardData.score_risco.classificacao_final}
              </div>
            </div>

            {/* Alertas */}
            <div style={{
              background: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
              color: 'white',
              padding: 24,
              borderRadius: 16,
              boxShadow: '0 8px 32px rgba(250, 112, 154, 0.3)'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 8 }}>
                <AlertTriangle size={24} />
                <span style={{ fontSize: 14, opacity: 0.9 }}>Alertas Ativos</span>
              </div>
              <div style={{ fontSize: '28px', fontWeight: 700 }}>
                {dashboardData.alertas_recentes.length}
              </div>
            </div>
          </div>

          {/* Gráficos e Tabelas */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24 }}>
            {/* Top Ativos */}
            <div style={{
              background: '#fff',
              borderRadius: 16,
              padding: 24,
              boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
              border: '1px solid #e9ecef'
            }}>
              <h3 style={{ 
                color: '#222', 
                marginBottom: 20, 
                fontSize: 18,
                fontWeight: 600,
                display: 'flex',
                alignItems: 'center',
                gap: 8
              }}>
                <TrendingUp size={20} />
                Top Ativos
              </h3>
              
              <div style={{ display: 'grid', gap: 12 }}>
                {dashboardData.top_ativos.map((ativo, index) => (
                  <div key={ativo.id} style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    padding: '12px 16px',
                    background: '#f8f9fa',
                    borderRadius: 8,
                    border: '1px solid #e9ecef'
                  }}>
                    <div style={{ flex: 1 }}>
                      <div style={{ fontWeight: 500, color: '#222' }}>
                        {ativo.name}
                      </div>
                      <div style={{ fontSize: 12, color: '#666', textTransform: 'capitalize' }}>
                        {ativo.asset_type.replace('_', ' ')}
                        {ativo.transaction_count !== undefined && (
                          <span style={{ marginLeft: 8, color: '#667eea' }}>
                            • {ativo.transaction_count} transações
                          </span>
                        )}
                      </div>
                      {ativo.current_quantity !== undefined && (
                        <div style={{ fontSize: 12, color: '#8b5cf6', marginTop: 2 }}>
                          Qtd: {ativo.current_quantity.toLocaleString('pt-BR', { maximumFractionDigits: 6 })}
                        </div>
                      )}
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <div style={{ fontWeight: 600, color: ativo.current_value !== undefined ? '#22c55e' : '#667eea' }}>
                        {formatCurrency(ativo.current_value !== undefined ? ativo.current_value : (ativo.value || 0))}
                      </div>
                      {ativo.current_value !== undefined && ativo.value !== undefined && (
                        <div style={{ fontSize: 10, color: '#666' }}>
                          Dinâmico
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Alertas Recentes */}
            <div style={{
              background: '#fff',
              borderRadius: 16,
              padding: 24,
              boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
              border: '1px solid #e9ecef'
            }}>
              <h3 style={{ 
                color: '#222', 
                marginBottom: 20, 
                fontSize: 18,
                fontWeight: 600,
                display: 'flex',
                alignItems: 'center',
                gap: 8
              }}>
                <AlertTriangle size={20} />
                Alertas Recentes
              </h3>
              
              <div style={{ display: 'grid', gap: 12 }}>
                {dashboardData.alertas_recentes.map((alerta, index) => (
                  <div key={index} style={{
                    padding: '12px 16px',
                    background: '#f8f9fa',
                    borderRadius: 8,
                    border: '1px solid #e9ecef',
                    borderLeft: `4px solid ${getSeverityColor(alerta.severidade)}`
                  }}>
                    <div style={{ 
                      fontWeight: 500, 
                      color: '#222',
                      marginBottom: 4
                    }}>
                      {alerta.tipo}
                    </div>
                    <div style={{ 
                      fontSize: 12, 
                      color: '#666',
                      marginBottom: 4
                    }}>
                      {alerta.mensagem}
                    </div>
                    <div style={{ 
                      fontSize: 10, 
                      color: getSeverityColor(alerta.severidade),
                      fontWeight: 600,
                      textTransform: 'uppercase'
                    }}>
                      {alerta.severidade}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Distribuição por Classe */}
          <div style={{
            background: '#fff',
            borderRadius: 16,
            padding: 24,
            boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
            border: '1px solid #e9ecef'
          }}>
            <h3 style={{ 
              color: '#222', 
              marginBottom: 20, 
              fontSize: 18,
              fontWeight: 600,
              display: 'flex',
              alignItems: 'center',
              gap: 8
            }}>
              <BarChart3 size={20} />
              Distribuição por Classe
            </h3>
            
            <div style={{ display: 'grid', gap: 12 }}>
              {dashboardData.distribuicao_classes.map((classe, index) => (
                <div key={index} style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '12px 16px',
                  background: '#f8f9fa',
                  borderRadius: 8,
                  border: '1px solid #e9ecef'
                }}>
                  <div style={{ 
                    fontWeight: 500, 
                    color: '#222',
                    textTransform: 'capitalize'
                  }}>
                    {classe.classe.replace('_', ' ')}
                  </div>
                  <div style={{ fontWeight: 600, color: '#667eea' }}>
                    {formatCurrency(classe.valor)}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Transações Recentes */}
          {dashboardData.recent_transactions && dashboardData.recent_transactions.length > 0 && (
            <div style={{
              background: '#fff',
              borderRadius: 16,
              padding: 24,
              boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
              border: '1px solid #e9ecef'
            }}>
              <h3 style={{ 
                color: '#222', 
                marginBottom: 20, 
                fontWeight: 600,
                display: 'flex',
                alignItems: 'center',
                gap: 8
              }}>
                <Activity size={20} />
                Transações Recentes
              </h3>
              
              <div style={{ display: 'grid', gap: 12 }}>
                {dashboardData.recent_transactions.slice(0, 5).map((transaction) => (
                  <div key={transaction.id} style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    padding: '12px 16px',
                    background: '#f8f9fa',
                    borderRadius: 8,
                    border: '1px solid #e9ecef'
                  }}>
                    <div style={{ flex: 1 }}>
                      <div style={{ fontWeight: 500, color: '#222' }}>
                        {transaction.asset_name}
                      </div>
                      <div style={{ fontSize: 12, color: '#666' }}>
                        {transaction.transaction_type === 'buy' ? 'Compra' : 'Venda'} de {transaction.quantity} unidades
                        <span style={{ marginLeft: 8, color: '#8b5cf6' }}>
                          • {new Date(transaction.transaction_date).toLocaleDateString('pt-BR')}
                        </span>
                      </div>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <div style={{ 
                        fontWeight: 600, 
                        color: transaction.transaction_type === 'buy' ? '#22c55e' : '#ef4444' 
                      }}>
                        {formatCurrency(transaction.total_value)}
                      </div>
                      <div style={{ fontSize: 10, color: '#666' }}>
                        {formatCurrency(transaction.unit_price)}/unidade
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
} 