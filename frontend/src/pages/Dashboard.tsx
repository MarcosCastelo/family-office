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
  Percent,
  ArrowUpRight,
  ArrowDownRight,
  Eye,
  Download,
  RefreshCw,
  Plus,
  Upload
} from 'lucide-react';
import { getDashboardData } from '../services/dashboard';
import { useFamily } from '../contexts/FamilyContext';
import PieChartComponent from '../components/PieChart';
import BarChartComponent from '../components/BarChart';

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
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null);

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
      setLastUpdate(new Date());
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

  const formatPercentage = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'percent',
      minimumFractionDigits: 1,
      maximumFractionDigits: 1
    }).format(value / 100);
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

  const getRiskIcon = (score: number) => {
    if (score <= 25) return <TrendingUp size={20} color="#388e3c" />;
    if (score <= 50) return <Activity size={20} color="#fbc02d" />;
    if (score <= 75) return <AlertTriangle size={20} color="#f57c00" />;
    return <AlertTriangle size={20} color="#d32f2f" />;
  };

  const getPerformanceIndicator = (current: number, previous: number) => {
    if (current > previous) {
      return (
        <div style={{ display: 'flex', alignItems: 'center', gap: 4, color: '#22c55e' }}>
          <ArrowUpRight size={16} />
          <span style={{ fontSize: 12, fontWeight: 600 }}>
            {formatPercentage(current - previous)}
          </span>
        </div>
      );
    } else if (current < previous) {
      return (
        <div style={{ display: 'flex', alignItems: 'center', gap: 4, color: '#ef4444' }}>
          <ArrowDownRight size={16} />
          <span style={{ fontSize: 12, fontWeight: 600 }}>
            {formatPercentage(previous - current)}
          </span>
        </div>
      );
    }
    return null;
  };

  // Preparar dados para os gráficos
  const pieChartData = dashboardData?.distribuicao_classes.map(item => ({
    label: getAssetTypeLabel(item.classe),
    value: item.valor,
    color: getAssetTypeColor(item.classe)
  })) || [];

  const barChartData = dashboardData?.top_ativos.slice(0, 6).map(ativo => ({
    label: ativo.name.length > 12 ? ativo.name.substring(0, 12) + '...' : ativo.name,
    value: ativo.value,
    color: getAssetTypeColor(ativo.asset_type),
    secondaryValue: ativo.average_cost * ativo.quantity
  })) || [];

  if (loading) {
    return (
      <div style={{ padding: 24, textAlign: 'center', color: '#666' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 12 }}>
          <RefreshCw size={24} className="animate-spin" />
          Carregando dashboard...
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: 24, textAlign: 'center', color: '#d32f2f' }}>
        <AlertTriangle size={48} style={{ marginBottom: 16 }} />
        <h3>Erro ao carregar dados</h3>
        <p>{error}</p>
        <button 
          onClick={loadDashboardData}
          style={{
            background: '#3b82f6',
            color: 'white',
            border: 'none',
            padding: '12px 24px',
            borderRadius: 8,
            cursor: 'pointer',
            marginTop: 16
          }}
        >
          Tentar novamente
        </button>
      </div>
    );
  }

  if (!dashboardData) {
    return (
      <div style={{ padding: 24, textAlign: 'center', color: '#666' }}>
        <PieChart size={48} style={{ marginBottom: 16 }} />
        <h3>Nenhum dado disponível</h3>
        <p>Selecione uma família para visualizar o dashboard</p>
      </div>
    );
  }

  return (
    <div>
      {/* Header com Atualização */}
      <div style={{ marginBottom: 32 }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 16 }}>
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
          <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
            {lastUpdate && (
              <div style={{ textAlign: 'right', fontSize: 12, color: '#666' }}>
                <div>Última atualização:</div>
                <div>{lastUpdate.toLocaleTimeString('pt-BR')}</div>
              </div>
            )}
            <button
              onClick={loadDashboardData}
              style={{
                background: '#f8fafc',
                border: '1px solid #e2e8f0',
                borderRadius: 8,
                padding: '8px',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
              title="Atualizar dados"
            >
              <RefreshCw size={16} />
            </button>
          </div>
        </div>
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
              <span style={{ fontSize: 14, opacity: 0.9 }}>Patrimônio Total</span>
            </div>
            <Eye size={20} style={{ opacity: 0.7 }} />
          </div>
          <div style={{ fontSize: 28, fontWeight: 700, marginBottom: 8 }}>
            {formatCurrency(dashboardData.patrimonio_total)}
          </div>
          <div style={{ fontSize: 14, opacity: 0.9 }}>
            {dashboardData.num_ativos} ativos • {formatPercentage(dashboardData.percentual_investido)} investido
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
              <span style={{ fontSize: 14, opacity: 0.9 }}>Investido</span>
            </div>
            <PiggyBank size={20} style={{ opacity: 0.7 }} />
          </div>
          <div style={{ fontSize: 28, fontWeight: 700, marginBottom: 8 }}>
            {formatCurrency(dashboardData.patrimonio_investido)}
          </div>
          <div style={{ fontSize: 14, opacity: 0.9 }}>
            {formatPercentage(dashboardData.percentual_investido)} do patrimônio
          </div>
        </div>

        {/* Caixa */}
        <div style={{
          background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
          color: 'white',
          padding: 24,
          borderRadius: 16,
          boxShadow: '0 8px 32px rgba(245, 158, 11, 0.3)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 16 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
              <Wallet size={24} />
              <span style={{ fontSize: 14, opacity: 0.9 }}>Caixa</span>
            </div>
            <Percent size={20} style={{ opacity: 0.7 }} />
          </div>
          <div style={{ fontSize: 28, fontWeight: 700, marginBottom: 8 }}>
            {formatCurrency(dashboardData.patrimonio_nao_investido)}
          </div>
          <div style={{ fontSize: 14, opacity: 0.9 }}>
            {formatPercentage(100 - dashboardData.percentual_investido)} disponível
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
              <Activity size={24} />
              <span style={{ fontSize: 14, opacity: 0.9 }}>Score de Risco</span>
            </div>
            {getRiskIcon(dashboardData.score_risco.score_global)}
          </div>
          <div style={{ fontSize: 28, fontWeight: 700, marginBottom: 8 }}>
            {dashboardData.score_risco.score_global}
          </div>
          <div style={{ fontSize: 14, opacity: 0.9 }}>
            {dashboardData.score_risco.classificacao_final}
          </div>
        </div>
      </div>

      {/* Gráficos e Análises */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', 
        gap: 24, 
        marginBottom: 32 
      }}>
        {/* Distribuição por Classe de Ativo */}
        <div style={{
          background: 'white',
          padding: 24,
          borderRadius: 16,
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.05)',
          border: '1px solid #e2e8f0'
        }}>
          <h3 style={{ margin: '0 0 20px 0', color: '#222', fontSize: 18, fontWeight: 600 }}>
            <PieChart size={20} style={{ marginRight: 8, verticalAlign: 'middle' }} />
            Distribuição por Classe
          </h3>
          <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 20 }}>
            <PieChartComponent
              data={pieChartData}
              size={250}
              showLabels={true}
              showValues={true}
              onSliceClick={(data, index) => {
                console.log('Clique no slice:', data, index);
              }}
            />
          </div>
          <div style={{ marginTop: 20 }}>
            {dashboardData.distribuicao_classes.map((classe, index) => (
              <div key={index} style={{ 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'space-between',
                padding: '8px 0',
                borderBottom: index < dashboardData.distribuicao_classes.length - 1 ? '1px solid #f1f5f9' : 'none'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <div style={{
                    width: 12,
                    height: 12,
                    borderRadius: '50%',
                    background: getAssetTypeColor(classe.classe)
                  }} />
                  <span style={{ fontSize: 14, color: '#666' }}>
                    {getAssetTypeLabel(classe.classe)}
                  </span>
                </div>
                <div style={{ fontSize: 14, fontWeight: 600, color: '#222' }}>
                  {formatCurrency(classe.valor)}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Top Ativos - Gráfico de Barras */}
        <div style={{
          background: 'white',
          padding: 24,
          borderRadius: 16,
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.05)',
          border: '1px solid #e2e8f0'
        }}>
          <h3 style={{ margin: '0 0 20px 0', color: '#222', fontSize: 18, fontWeight: 600 }}>
            <BarChart3 size={20} style={{ marginRight: 8, verticalAlign: 'middle' }} />
            Top Ativos por Valor
          </h3>
          <div style={{ display: 'flex', justifyContent: 'center' }}>
            <BarChartComponent
              data={barChartData}
              width={400}
              height={300}
              showValues={true}
              showGrid={true}
              animate={true}
              onBarClick={(data, index) => {
                console.log('Clique na barra:', data, index);
              }}
            />
          </div>
          <div style={{ marginTop: 20 }}>
            <div style={{ fontSize: 12, color: '#666', textAlign: 'center' }}>
              <span style={{ color: '#666' }}>●</span> Valor atual • 
              <span style={{ color: '#666', opacity: 0.3 }}>●</span> Custo médio
            </div>
          </div>
        </div>
      </div>

      {/* Alertas Recentes */}
      <div style={{
        background: 'white',
        padding: 24,
        borderRadius: 16,
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.05)',
        border: '1px solid #e2e8f0',
        marginBottom: 32
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 20 }}>
          <h3 style={{ margin: 0, color: '#222', fontSize: 18, fontWeight: 600 }}>
            <AlertTriangle size={20} style={{ marginRight: 8, verticalAlign: 'middle' }} />
            Alertas Recentes
          </h3>
          <span style={{ fontSize: 14, color: '#666' }}>
            {dashboardData.alertas_recentes.length} alertas
          </span>
        </div>
        
        {dashboardData.alertas_recentes.length === 0 ? (
          <div style={{ 
            textAlign: 'center', 
            padding: '40px 20px', 
            color: '#666',
            background: '#f8fafc',
            borderRadius: 8
          }}>
            <Target size={48} style={{ marginBottom: 16, opacity: 0.5 }} />
            <div style={{ fontSize: 16, fontWeight: 500, marginBottom: 8 }}>
              Nenhum alerta ativo
            </div>
            <div style={{ fontSize: 14 }}>
              Sua carteira está em conformidade com os parâmetros de risco
            </div>
          </div>
        ) : (
          <div style={{ display: 'grid', gap: 16 }}>
            {dashboardData.alertas_recentes.map((alerta, index) => (
              <div key={index} style={{
                display: 'flex',
                alignItems: 'flex-start',
                gap: 12,
                padding: 16,
                background: '#f8fafc',
                borderRadius: 8,
                border: `1px solid ${getSeverityColor(alerta.severidade)}20`
              }}>
                <div style={{
                  width: 8,
                  height: 8,
                  borderRadius: '50%',
                  background: getSeverityColor(alerta.severidade),
                  marginTop: 6
                }} />
                <div style={{ flex: 1 }}>
                  <div style={{ 
                    display: 'flex', 
                    alignItems: 'center', 
                    gap: 8, 
                    marginBottom: 4 
                  }}>
                    <span style={{ 
                      fontSize: 12, 
                      fontWeight: 600, 
                      color: getSeverityColor(alerta.severidade),
                      textTransform: 'uppercase',
                      letterSpacing: '0.5px'
                    }}>
                      {alerta.tipo}
                    </span>
                    <span style={{ 
                      fontSize: 12, 
                      color: '#666',
                      background: '#e2e8f0',
                      padding: '2px 8px',
                      borderRadius: 4
                    }}>
                      {alerta.severidade}
                    </span>
                  </div>
                  <div style={{ fontSize: 14, color: '#222', marginBottom: 4 }}>
                    {alerta.mensagem}
                  </div>
                  <div style={{ fontSize: 12, color: '#666' }}>
                    {new Date(alerta.criado_em).toLocaleString('pt-BR')}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Ações Rápidas */}
      <div style={{
        background: 'white',
        padding: 24,
        borderRadius: 16,
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.05)',
        border: '1px solid #e2e8f0'
      }}>
        <h3 style={{ margin: '0 0 20px 0', color: '#222', fontSize: 18, fontWeight: 600 }}>
          Ações Rápidas
        </h3>
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
          gap: 16 
        }}>
          <button style={{
            display: 'flex',
            alignItems: 'center',
            gap: 12,
            padding: '16px 20px',
            background: '#f8fafc',
            border: '1px solid #e2e8f0',
            borderRadius: 8,
            cursor: 'pointer',
            transition: 'all 0.2s',
            width: '100%'
          }}>
            <Plus size={20} color="#3b82f6" />
            <span style={{ color: '#222', fontWeight: 500 }}>Novo Ativo</span>
          </button>
          
          <button style={{
            display: 'flex',
            alignItems: 'center',
            gap: 12,
            padding: '16px 20px',
            background: '#f8fafc',
            border: '1px solid #e2e8f0',
            borderRadius: 8,
            cursor: 'pointer',
            transition: 'all 0.2s',
            width: '100%'
          }}>
            <Upload size={20} color="#22c55e" />
            <span style={{ color: '#222', fontWeight: 500 }}>Upload de Arquivo</span>
          </button>
          
          <button style={{
            display: 'flex',
            alignItems: 'center',
            gap: 12,
            padding: '16px 20px',
            background: '#f8fafc',
            border: '1px solid #e2e8f0',
            borderRadius: 8,
            cursor: 'pointer',
            transition: 'all 0.2s',
            width: '100%'
          }}>
            <Download size={20} color="#f59e0b" />
            <span style={{ color: '#222', fontWeight: 500 }}>Relatório PDF</span>
          </button>
          
          <button style={{
            display: 'flex',
            alignItems: 'center',
            gap: 12,
            padding: '16px 20px',
            background: '#f8fafc',
            border: '1px solid #e2e8f0',
            borderRadius: 8,
            cursor: 'pointer',
            transition: 'all 0.2s',
            width: '100%'
          }}>
            <Activity size={20} color="#ef4444" />
            <span style={{ color: '#222', fontWeight: 500 }}>Análise de Risco</span>
          </button>
        </div>
      </div>
    </div>
  );
} 