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
  LayoutDashboard,
  Wallet,
  PiggyBank,
  Percent
} from 'lucide-react';
import { getDashboardData } from '../services/dashboard';
import { useFamily } from '../contexts/FamilyContext';

interface DashboardData {
  patrimonio_total: number;
  patrimonio_investido: number;
  patrimonio_nao_investido: number;
  percentual_investido: number;
  num_ativos: number;
  distribuicao_classes: Array<{ classe: string; valor: number }>;
  top_ativos: Array<{ 
    id: number; 
    name: string; 
    value: number;
    asset_type: string;
    quantity: number;
    average_cost: number;
  }>;
  alertas_recentes: Array<{ tipo: string; mensagem: string; severidade: string; criado_em: string }>;
  score_risco: { score_global: number; classificacao_final: string };
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

  const formatNumber = (value: number) => {
    return new Intl.NumberFormat('pt-BR').format(value);
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

  const getAssetTypeLabel = (type: string) => {
    const labels: { [key: string]: string } = {
      'renda_fixa': 'Renda Fixa',
      'renda_variavel': 'Renda Variável',
      'multimercado': 'Multimercado',
      'ativos_reais': 'Ativos Reais',
      'estrategicos': 'Estratégicos',
      'internacionais': 'Internacionais',
      'alternativos': 'Alternativos',
      'protecao': 'Proteção'
    };
    return labels[type] || type;
  };

  const getAssetTypeColor = (type: string) => {
    const colors: { [key: string]: string } = {
      'renda_fixa': '#22c55e',
      'renda_variavel': '#3b82f6',
      'multimercado': '#8b5cf6',
      'ativos_reais': '#f59e0b',
      'estrategicos': '#ef4444',
      'internacionais': '#06b6d4',
      'alternativos': '#ec4899',
      'protecao': '#84cc16'
    };
    return colors[type] || '#666';
  };

  if (loading) {
    return (
      <div style={{ padding: 24, textAlign: 'center', color: '#666' }}>
        Carregando dashboard...
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: 24, textAlign: 'center', color: '#d32f2f' }}>
        Erro: {error}
      </div>
    );
  }

  if (!dashboardData) {
    return (
      <div style={{ padding: 24, textAlign: 'center', color: '#666' }}>
        Nenhum dado disponível
      </div>
    );
  }

  return (
    <div>
      {/* Header */}
      <div style={{ marginBottom: 32 }}>
        <h1 style={{ 
          margin: 0, 
          color: '#222', 
          fontSize: 28, 
          fontWeight: 700,
          display: 'flex',
          alignItems: 'center',
          gap: 12
        }}>
          <LayoutDashboard size={32} />
          Dashboard
        </h1>
        <p style={{ 
          margin: '8px 0 0 0', 
          color: '#666', 
          fontSize: 16 
        }}>
          Visão geral do patrimônio e investimentos
        </p>
      </div>

      {/* Métricas Principais */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', 
        gap: 24, 
        marginBottom: 32 
      }}>
        {/* Patrimônio Total */}
        <div style={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          padding: 24,
          borderRadius: 16,
          boxShadow: '0 8px 32px rgba(102, 126, 234, 0.3)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 16 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
              <DollarSign size={24} />
              <span style={{ fontSize: 16, fontWeight: 600 }}>Patrimônio Total</span>
            </div>
          </div>
          <div style={{ fontSize: 32, fontWeight: 700, marginBottom: 8 }}>
            {formatCurrency(dashboardData.patrimonio_total)}
          </div>
          <div style={{ fontSize: 14, opacity: 0.9 }}>
            {dashboardData.num_ativos} ativo{dashboardData.num_ativos !== 1 ? 's' : ''}
          </div>
        </div>

        {/* Patrimônio Investido */}
        <div style={{
          background: 'linear-gradient(135deg, #22c55e 0%, #16a34a 100%)',
          color: 'white',
          padding: 24,
          borderRadius: 16,
          boxShadow: '0 8px 32px rgba(34, 197, 94, 0.3)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 16 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
              <TrendingUp size={24} />
              <span style={{ fontSize: 16, fontWeight: 600 }}>Patrimônio Investido</span>
            </div>
          </div>
          <div style={{ fontSize: 32, fontWeight: 700, marginBottom: 8 }}>
            {formatCurrency(dashboardData.patrimonio_investido)}
          </div>
          <div style={{ fontSize: 14, opacity: 0.9 }}>
            {dashboardData.percentual_investido}% do total
          </div>
        </div>

        {/* Patrimônio Não Investido */}
        <div style={{
          background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
          color: 'white',
          padding: 24,
          borderRadius: 16,
          boxShadow: '0 8px 32px rgba(245, 158, 11, 0.3)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 16 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
              <PiggyBank size={24} />
              <span style={{ fontSize: 16, fontWeight: 600 }}>Saldo Disponível</span>
            </div>
          </div>
          <div style={{ fontSize: 32, fontWeight: 700, marginBottom: 8 }}>
            {formatCurrency(dashboardData.patrimonio_nao_investido)}
          </div>
          <div style={{ fontSize: 14, opacity: 0.9 }}>
            Para novos investimentos
          </div>
        </div>

        {/* Score de Risco */}
        <div style={{
          background: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
          color: 'white',
          padding: 24,
          borderRadius: 16,
          boxShadow: '0 8px 32px rgba(239, 68, 68, 0.3)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 16 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
              <Target size={24} />
              <span style={{ fontSize: 16, fontWeight: 600 }}>Score de Risco</span>
            </div>
          </div>
          <div style={{ fontSize: 32, fontWeight: 700, marginBottom: 8 }}>
            {dashboardData.score_risco.score_global}
          </div>
          <div style={{ 
            fontSize: 14, 
            opacity: 0.9,
            textTransform: 'capitalize'
          }}>
            {dashboardData.score_risco.classificacao_final}
          </div>
        </div>
      </div>

      {/* Conteúdo Principal */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', 
        gap: 24 
      }}>
        {/* Distribuição por Classe */}
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
            fontWeight: 600,
            display: 'flex',
            alignItems: 'center',
            gap: 8
          }}>
            <PieChart size={20} />
            Distribuição por Classe
          </h3>
          
          {dashboardData.distribuicao_classes.length > 0 ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              {dashboardData.distribuicao_classes.map((item, index) => {
                const percentage = dashboardData.patrimonio_investido > 0 
                  ? (item.valor / dashboardData.patrimonio_investido * 100) 
                  : 0;
                
                return (
                  <div key={index} style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                    <div style={{
                      width: 12,
                      height: 12,
                      borderRadius: '50%',
                      background: getAssetTypeColor(item.classe),
                      flexShrink: 0
                    }} />
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{ 
                        display: 'flex', 
                        justifyContent: 'space-between', 
                        alignItems: 'center',
                        marginBottom: 4
                      }}>
                        <span style={{ 
                          fontSize: 14, 
                          fontWeight: 500, 
                          color: '#333',
                          whiteSpace: 'nowrap',
                          overflow: 'hidden',
                          textOverflow: 'ellipsis'
                        }}>
                          {getAssetTypeLabel(item.classe)}
                        </span>
                        <span style={{ 
                          fontSize: 14, 
                          fontWeight: 600, 
                          color: '#222',
                          marginLeft: 8
                        }}>
                          {formatCurrency(item.valor)}
                        </span>
                      </div>
                      <div style={{
                        width: '100%',
                        height: 6,
                        background: '#f1f5f9',
                        borderRadius: 3,
                        overflow: 'hidden'
                      }}>
                        <div style={{
                          width: `${percentage}%`,
                          height: '100%',
                          background: getAssetTypeColor(item.classe),
                          borderRadius: 3,
                          transition: 'width 0.3s ease'
                        }} />
                      </div>
                      <div style={{ 
                        fontSize: 12, 
                        color: '#666', 
                        marginTop: 4,
                        textAlign: 'right'
                      }}>
                        {percentage.toFixed(1)}%
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div style={{ textAlign: 'center', color: '#666', padding: 20 }}>
              Nenhum ativo encontrado
            </div>
          )}
        </div>

        {/* Top Ativos */}
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
            fontWeight: 600,
            display: 'flex',
            alignItems: 'center',
            gap: 8
          }}>
            <TrendingUp size={20} />
            Top Ativos
          </h3>
          
          {dashboardData.top_ativos.length > 0 ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
              {dashboardData.top_ativos.map((ativo, index) => (
                <div key={ativo.id} style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 12,
                  padding: 16,
                  background: '#f8fafc',
                  borderRadius: 12,
                  border: '1px solid #e2e8f0'
                }}>
                  <div style={{
                    width: 40,
                    height: 40,
                    borderRadius: '50%',
                    background: getAssetTypeColor(ativo.asset_type),
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                    fontWeight: 600,
                    fontSize: 14
                  }}>
                    {index + 1}
                  </div>
                  
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ 
                      fontSize: 16, 
                      fontWeight: 600, 
                      color: '#222',
                      marginBottom: 4,
                      whiteSpace: 'nowrap',
                      overflow: 'hidden',
                      textOverflow: 'ellipsis'
                    }}>
                      {ativo.name}
                    </div>
                    <div style={{ 
                      fontSize: 12, 
                      color: '#666',
                      textTransform: 'capitalize'
                    }}>
                      {getAssetTypeLabel(ativo.asset_type)}
                    </div>
                  </div>
                  
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ 
                      fontSize: 16, 
                      fontWeight: 600, 
                      color: '#22c55e',
                      marginBottom: 2
                    }}>
                      {formatCurrency(ativo.value)}
                    </div>
                    <div style={{ 
                      fontSize: 12, 
                      color: '#666'
                    }}>
                      {formatNumber(ativo.quantity)} unid.
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div style={{ textAlign: 'center', color: '#666', padding: 20 }}>
              Nenhum ativo encontrado
            </div>
          )}
        </div>

        {/* Alertas Recentes */}
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
            fontWeight: 600,
            display: 'flex',
            alignItems: 'center',
            gap: 8
          }}>
            <AlertTriangle size={20} />
            Alertas Recentes
          </h3>
          
          {dashboardData.alertas_recentes.length > 0 ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              {dashboardData.alertas_recentes.map((alerta, index) => (
                <div key={index} style={{
                  padding: 16,
                  background: '#fef2f2',
                  border: `1px solid ${getSeverityColor(alerta.severidade)}20`,
                  borderRadius: 12,
                  borderLeft: `4px solid ${getSeverityColor(alerta.severidade)}`
                }}>
                  <div style={{ 
                    display: 'flex', 
                    alignItems: 'center', 
                    gap: 8,
                    marginBottom: 8
                  }}>
                    <div style={{
                      width: 8,
                      height: 8,
                      borderRadius: '50%',
                      background: getSeverityColor(alerta.severidade)
                    }} />
                    <span style={{ 
                      fontSize: 12, 
                      fontWeight: 600, 
                      color: getSeverityColor(alerta.severidade),
                      textTransform: 'uppercase'
                    }}>
                      {alerta.severidade}
                    </span>
                    <span style={{ 
                      fontSize: 12, 
                      color: '#666'
                    }}>
                      {new Date(alerta.criado_em).toLocaleDateString('pt-BR')}
                    </span>
                  </div>
                  <div style={{ 
                    fontSize: 14, 
                    color: '#333',
                    lineHeight: 1.4
                  }}>
                    {alerta.mensagem}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div style={{ textAlign: 'center', color: '#666', padding: 20 }}>
              Nenhum alerta recente
            </div>
          )}
        </div>
      </div>
    </div>
  );
} 