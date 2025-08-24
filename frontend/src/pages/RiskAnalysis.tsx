import React, { useState, useEffect } from 'react';
import { 
  BarChart3, 
  AlertTriangle, 
  TrendingUp, 
  Shield, 
  RefreshCw,
  Eye,
  Activity,
  PieChart,
  DollarSign,
  Users,
  Clock
} from 'lucide-react';
import { 
  getPortfolioRiskAnalysis, 
  getAssetRiskMetrics, 
  updateAssetQuotes,
  getMarketOverview,
  getRiskAlerts,
  type PortfolioRiskAnalysis,
  type RiskMetrics,
  type MarketOverview,
  type RiskAlert,
  calculateRiskColor,
  getRiskLabel,
  formatCurrency,
  formatPercentage,
  formatNumber
} from '../services/riskAnalysis';
import { useFamily } from '../contexts/FamilyContext';
import { useToast } from '../components/Toast';

export default function RiskAnalysis() {
  const { selectedFamilyId } = useFamily();
  const { showToast } = useToast();
  
  const [portfolioRisk, setPortfolioRisk] = useState<PortfolioRiskAnalysis | null>(null);
  const [marketOverview, setMarketOverview] = useState<MarketOverview | null>(null);
  const [riskAlerts, setRiskAlerts] = useState<RiskAlert[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [updatingQuotes, setUpdatingQuotes] = useState(false);
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null);

  useEffect(() => {
    if (selectedFamilyId) {
      loadRiskData();
    }
  }, [selectedFamilyId]);

  const loadRiskData = async () => {
    if (!selectedFamilyId) return;
    
    try {
      setLoading(true);
      setError(null);
      
      // Carregar dados em paralelo
      const [riskData, overviewData, alertsData] = await Promise.all([
        getPortfolioRiskAnalysis(selectedFamilyId),
        getMarketOverview(selectedFamilyId),
        getRiskAlerts(selectedFamilyId)
      ]);
      
      setPortfolioRisk(riskData);
      setMarketOverview(overviewData);
      setRiskAlerts(alertsData);
      setLastUpdate(new Date());
      
    } catch (err: any) {
      console.error('Erro ao carregar dados de risco:', err);
      setError(err.response?.data?.error || 'Erro ao carregar dados de risco');
      showToast('Erro ao carregar análise de risco', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateQuotes = async () => {
    if (!selectedFamilyId) return;
    
    try {
      setUpdatingQuotes(true);
      const result = await updateAssetQuotes(selectedFamilyId);
      
      showToast(result.message, 'success');
      
      // Recarregar dados após atualização
      await loadRiskData();
      
    } catch (err: any) {
      console.error('Erro ao atualizar cotações:', err);
      showToast('Erro ao atualizar cotações', 'error');
    } finally {
      setUpdatingQuotes(false);
    }
  };

  const getRiskIcon = (riskScore: number) => {
    if (riskScore <= 25) return <Shield size={20} color="#10b981" />;
    if (riskScore <= 50) return <AlertTriangle size={20} color="#f59e0b" />;
    if (riskScore <= 75) return <TrendingUp size={20} color="#f97316" />;
    return <AlertTriangle size={20} color="#ef4444" />;
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high': return '#ef4444';
      case 'medium': return '#f97316';
      case 'low': return '#f59e0b';
      default: return '#666';
    }
  };

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
          <div>Selecione uma família para analisar o risco.</div>
        </div>
      </div>
    );
  }

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
          <RefreshCw size={48} style={{ marginBottom: 16, opacity: 0.6 }} className="animate-spin" />
          <div>Carregando análise de risco...</div>
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
        color: '#ef4444'
      }}>
        <div style={{ textAlign: 'center' }}>
          <AlertTriangle size={48} style={{ marginBottom: 16 }} />
          <div>Erro: {error}</div>
          <button 
            onClick={loadRiskData}
            style={{
              marginTop: 16,
              padding: '8px 16px',
              background: '#ef4444',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer'
            }}
          >
            Tentar Novamente
          </button>
        </div>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto' }}>
      {/* Header */}
      <div style={{ marginBottom: 32 }}>
        <div style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center',
          marginBottom: 16
        }}>
          <h1 style={{ 
            color: '#222', 
            marginBottom: 16, 
            fontSize: '28px',
            fontWeight: 600,
            display: 'flex',
            alignItems: 'center',
            gap: 12
          }}>
            <Shield size={28} />
            Análise de Risco
          </h1>
          
          <button
            onClick={handleUpdateQuotes}
            disabled={updatingQuotes}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 8,
              padding: '10px 16px',
              background: '#667eea',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              cursor: updatingQuotes ? 'not-allowed' : 'pointer',
              opacity: updatingQuotes ? 0.6 : 1
            }}
          >
            <RefreshCw size={16} className={updatingQuotes ? 'animate-spin' : ''} />
            {updatingQuotes ? 'Atualizando...' : 'Atualizar Cotações'}
          </button>
        </div>
        
        {lastUpdate && (
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: 8, 
            color: '#666',
            fontSize: '14px'
          }}>
            <Clock size={16} />
            Última atualização: {lastUpdate.toLocaleString('pt-BR')}
          </div>
        )}
      </div>

      {/* Resumo de Risco da Carteira */}
      {portfolioRisk && (
        <div style={{ marginBottom: 32 }}>
          <h2 style={{ 
            color: '#333', 
            marginBottom: 16, 
            fontSize: '20px',
            fontWeight: 600
          }}>
            Resumo de Risco da Carteira
          </h2>
          
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
            gap: 16
          }}>
            <div style={{
              padding: '20px',
              background: 'white',
              borderRadius: '12px',
              border: '1px solid #e2e8f0',
              textAlign: 'center'
            }}>
              <div style={{ fontSize: '24px', fontWeight: '700', color: '#222' }}>
                {formatCurrency(portfolioRisk.total_portfolio_value)}
              </div>
              <div style={{ color: '#666', fontSize: '14px' }}>Valor Total</div>
            </div>
            
            <div style={{
              padding: '20px',
              background: 'white',
              borderRadius: '12px',
              border: '1px solid #e2e8f0',
              textAlign: 'center'
            }}>
              <div style={{ fontSize: '24px', fontWeight: '700', color: '#222' }}>
                {portfolioRisk.number_of_assets}
              </div>
              <div style={{ color: '#666', fontSize: '14px' }}>Total de Ativos</div>
            </div>
            
            <div style={{
              padding: '20px',
              background: 'white',
              borderRadius: '12px',
              border: '1px solid #e2e8f0',
              textAlign: 'center'
            }}>
              <div style={{ 
                fontSize: '24px', 
                fontWeight: '700', 
                color: calculateRiskColor(portfolioRisk.weighted_risk_score)
              }}>
                {portfolioRisk.weighted_risk_score.toFixed(1)}
              </div>
              <div style={{ color: '#666', fontSize: '14px' }}>Score de Risco</div>
            </div>
            
            <div style={{
              padding: '20px',
              background: 'white',
              borderRadius: '12px',
              border: '1px solid #e2e8f0',
              textAlign: 'center'
            }}>
              <div style={{ 
                fontSize: '24px', 
                fontWeight: '700', 
                color: calculateRiskColor(portfolioRisk.weighted_risk_score)
              }}>
                {portfolioRisk.risk_classification}
              </div>
              <div style={{ color: '#666', fontSize: '14px' }}>Classificação</div>
            </div>
          </div>
        </div>
      )}

      {/* Visão Geral do Mercado */}
      {marketOverview && (
        <div style={{ marginBottom: 32 }}>
          <h2 style={{ 
            color: '#333', 
            marginBottom: 16, 
            fontSize: '20px',
            fontWeight: 600
          }}>
            Visão Geral do Mercado
          </h2>
          
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
            gap: 16
          }}>
            {/* Distribuição por Tipo de Ativo */}
            <div style={{
              padding: '20px',
              background: 'white',
              borderRadius: '12px',
              border: '1px solid #e2e8f0'
            }}>
              <h3 style={{ 
                color: '#333', 
                marginBottom: 16, 
                fontSize: '16px',
                fontWeight: 600
              }}>
                Distribuição por Tipo
              </h3>
              
              {Object.entries(marketOverview.asset_types).map(([type, data]) => (
                <div key={type} style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '8px 0',
                  borderBottom: '1px solid #f1f5f9'
                }}>
                  <span style={{ color: '#666', textTransform: 'capitalize' }}>
                    {type.replace('_', ' ')}
                  </span>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontWeight: '600', color: '#222' }}>
                      {formatCurrency(data.total_value)}
                    </div>
                    <div style={{ fontSize: '12px', color: '#666' }}>
                      {data.percentage.toFixed(1)}%
                    </div>
                  </div>
                </div>
              ))}
            </div>
            
            {/* Análise de Concentração */}
            <div style={{
              padding: '20px',
              background: 'white',
              borderRadius: '12px',
              border: '1px solid #e2e8f0'
            }}>
              <h3 style={{ 
                color: '#333', 
                marginBottom: 16, 
                fontSize: '16px',
                fontWeight: 600
              }}>
                Análise de Concentração
              </h3>
              
              <div style={{ marginBottom: 16 }}>
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  marginBottom: 8
                }}>
                  <span style={{ color: '#10b981' }}>Bem Diversificada</span>
                  <span style={{ fontWeight: '600' }}>{marketOverview.concentration_analysis.well_diversified}</span>
                </div>
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  marginBottom: 8
                }}>
                  <span style={{ color: '#f59e0b' }}>Moderadamente Concentrada</span>
                  <span style={{ fontWeight: '600' }}>{marketOverview.concentration_analysis.moderately_concentrated}</span>
                </div>
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center'
                }}>
                  <span style={{ color: '#ef4444' }}>Altamente Concentrada</span>
                  <span style={{ fontWeight: '600' }}>{marketOverview.concentration_analysis.highly_concentrated}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Alertas de Risco */}
      {riskAlerts.length > 0 && (
        <div style={{ marginBottom: 32 }}>
          <h2 style={{ 
            color: '#333', 
            marginBottom: 16, 
            fontSize: '20px',
            fontWeight: 600,
            display: 'flex',
            alignItems: 'center',
            gap: 8
          }}>
            <AlertTriangle size={20} color="#ef4444" />
            Alertas de Risco ({riskAlerts.length})
          </h2>
          
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))',
            gap: 16
          }}>
            {riskAlerts.map((alert, index) => (
              <div key={index} style={{
                padding: '16px',
                background: 'white',
                borderRadius: '12px',
                border: `2px solid ${getSeverityColor(alert.severity)}`,
                borderLeft: `6px solid ${getSeverityColor(alert.severity)}`
              }}>
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'flex-start',
                  marginBottom: 8
                }}>
                  <div style={{ fontWeight: '600', color: '#222' }}>
                    {alert.asset_name}
                  </div>
                  <span style={{
                    padding: '4px 8px',
                    background: `${getSeverityColor(alert.severity)}20`,
                    color: getSeverityColor(alert.severity),
                    borderRadius: '4px',
                    fontSize: '12px',
                    fontWeight: '600',
                    textTransform: 'uppercase'
                  }}>
                    {alert.severity}
                  </span>
                </div>
                
                <div style={{ color: '#666', marginBottom: 8 }}>
                  {alert.message}
                </div>
                
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  fontSize: '12px',
                  color: '#666'
                }}>
                  <span>Tipo: {alert.type}</span>
                  <span>Valor: {alert.value.toFixed(1)}% (Limite: {alert.limit}%)</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Análise Detalhada por Ativo */}
      {portfolioRisk && portfolioRisk.asset_risks.length > 0 && (
        <div>
          <h2 style={{ 
            color: '#333', 
            marginBottom: 16, 
            fontSize: '20px',
            fontWeight: 600
          }}>
            Análise Detalhada por Ativo
          </h2>
          
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))',
            gap: 16
          }}>
            {portfolioRisk.asset_risks.map((assetRisk) => (
              <div key={assetRisk.asset_id} style={{
                padding: '20px',
                background: 'white',
                borderRadius: '12px',
                border: '1px solid #e2e8f0'
              }}>
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'flex-start',
                  marginBottom: 16
                }}>
                  <div>
                    <h3 style={{ 
                      color: '#222', 
                      marginBottom: 4, 
                      fontSize: '16px',
                      fontWeight: '600'
                    }}>
                      {assetRisk.name}
                    </h3>
                    <div style={{ 
                      color: '#666', 
                      fontSize: '12px',
                      textTransform: 'capitalize'
                    }}>
                      {assetRisk.asset_type.replace('_', ' ')}
                    </div>
                  </div>
                  
                  {getRiskIcon(assetRisk.risk_metrics.volatility)}
                </div>
                
                <div style={{ marginBottom: 16 }}>
                  <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    marginBottom: 8
                  }}>
                    <span style={{ color: '#666' }}>Valor Atual:</span>
                    <span style={{ fontWeight: '600' }}>
                      {formatCurrency(assetRisk.current_value)}
                    </span>
                  </div>
                  
                  <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    marginBottom: 8
                  }}>
                    <span style={{ color: '#666' }}>Preço Atual:</span>
                    <span style={{ fontWeight: '600' }}>
                      {formatCurrency(assetRisk.risk_metrics.current_price)}
                    </span>
                  </div>
                  
                  <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    marginBottom: 8
                  }}>
                    <span style={{ color: '#666' }}>Variação 24h:</span>
                    <span style={{ 
                      fontWeight: '600',
                      color: assetRisk.risk_metrics.price_change_24h >= 0 ? '#10b981' : '#ef4444'
                    }}>
                      {formatPercentage(assetRisk.risk_metrics.price_change_24h)}
                    </span>
                  </div>
                </div>
                
                {/* Métricas de Risco */}
                <div style={{
                  display: 'grid',
                  gridTemplateColumns: '1fr 1fr',
                  gap: 12
                }}>
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ 
                      fontSize: '18px', 
                      fontWeight: '700',
                      color: calculateRiskColor(assetRisk.risk_metrics.volatility)
                    }}>
                      {assetRisk.risk_metrics.volatility.toFixed(1)}
                    </div>
                    <div style={{ fontSize: '11px', color: '#666' }}>Volatilidade</div>
                  </div>
                  
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ 
                      fontSize: '18px', 
                      fontWeight: '700',
                      color: calculateRiskColor(assetRisk.risk_metrics.liquidity_score)
                    }}>
                      {assetRisk.risk_metrics.liquidity_score.toFixed(0)}
                    </div>
                    <div style={{ fontSize: '11px', color: '#666' }}>Liquidez</div>
                  </div>
                  
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ 
                      fontSize: '18px', 
                      fontWeight: '700',
                      color: calculateRiskColor(assetRisk.risk_metrics.concentration_risk)
                    }}>
                      {assetRisk.risk_metrics.concentration_risk.toFixed(0)}
                    </div>
                    <div style={{ fontSize: '11px', color: '#666' }}>Concentração</div>
                  </div>
                  
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ 
                      fontSize: '18px', 
                      fontWeight: '700',
                      color: calculateRiskColor(assetRisk.risk_metrics.market_risk)
                    }}>
                      {assetRisk.risk_metrics.market_risk.toFixed(0)}
                    </div>
                    <div style={{ fontSize: '11px', color: '#666' }}>Mercado</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
} 