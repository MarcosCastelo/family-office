import axios from 'axios';

const API_URL = 'http://localhost:5000';

export interface RiskMetrics {
  current_price: number;
  price_change_24h: number;
  volatility: number;
  liquidity_score: number;
  concentration_risk: number;
  market_risk: number;
  beta_risk: number;
  last_updated: string;
}

export interface AssetRisk {
  asset_id: number;
  name: string;
  asset_type: string;
  current_value: number;
  risk_metrics: RiskMetrics;
}

export interface PortfolioRiskAnalysis {
  total_portfolio_value: number;
  number_of_assets: number;
  weighted_risk_score: number;
  risk_classification: string;
  asset_risks: AssetRisk[];
  risk_breakdown: {
    volatility_weight: number;
    liquidity_weight: number;
    concentration_weight: number;
    market_weight: number;
  };
  analysis_timestamp: string;
}

export interface MarketOverview {
  total_assets: number;
  asset_types: Record<string, {
    count: number;
    total_value: number;
    percentage: number;
  }>;
  total_portfolio_value: number;
  concentration_analysis: {
    well_diversified: number;
    moderately_concentrated: number;
    highly_concentrated: number;
  };
  analysis_timestamp: string;
}

export interface RiskAlert {
  type: 'concentration' | 'liquidity' | 'volatility' | 'market';
  severity: 'low' | 'medium' | 'high';
  asset_id: number;
  asset_name: string;
  message: string;
  value: number;
  limit: number;
}

export interface RiskAlertsResponse {
  alerts: RiskAlert[];
  total_alerts: number;
  high_severity: number;
  medium_severity: number;
  low_severity: number;
  timestamp: string;
}

// ROTAS TEMPORÁRIAS SEM PERMISSÕES PARA TESTE
export async function getPortfolioRiskAnalysis(familyId: number): Promise<PortfolioRiskAnalysis> {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Token de acesso não encontrado');
  }

  const response = await axios.get(`${API_URL}/risk/portfolio/risk`, {
    headers: {
      'Authorization': `Bearer ${token}`
    },
    params: {
      family_id: familyId
    }
  });
  
  return response.data;
}

export async function getAssetRiskMetrics(assetId: number, familyId: number): Promise<{
  asset_id: number;
  asset_name: string;
  asset_type: string;
  risk_metrics: RiskMetrics;
}> {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Token de acesso não encontrado');
  }

  const response = await axios.get(`${API_URL}/risk/assets/${assetId}/risk`, {
    headers: {
      'Authorization': `Bearer ${token}`
    },
    params: {
      family_id: familyId
    }
  });
  
  return response.data;
}

export async function updateAssetQuotes(familyId: number): Promise<{
  message: string;
  result: {
    updated_assets: number;
    total_assets: number;
    errors: string[];
    timestamp: string;
  };
}> {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Token de acesso não encontrado');
  }

  const response = await axios.post(`${API_URL}/risk/quotes/update`, {}, {
    headers: {
      'Authorization': `Bearer ${token}`
    },
    params: {
      family_id: familyId
    }
  });
  
  return response.data;
}

export async function getMarketOverview(familyId: number): Promise<MarketOverview> {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Token de acesso não encontrado');
  }

  const response = await axios.get(`${API_URL}/risk/market/overview`, {
    headers: {
      'Authorization': `Bearer ${token}`
    },
    params: {
      family_id: familyId
    }
  });
  
  return response.data;
}

export async function getRiskAlerts(familyId: number): Promise<RiskAlertsResponse> {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Token de acesso não encontrado');
  }

  const response = await axios.get(`${API_URL}/risk/alerts`, {
    headers: {
      'Authorization': `Bearer ${token}`
    },
    params: {
      family_id: familyId
    }
  });
  
  return response.data;
}

// Funções auxiliares para análise de risco
export function calculateRiskColor(riskScore: number): string {
  if (riskScore <= 25) return '#10b981'; // Verde - Baixo risco
  if (riskScore <= 50) return '#f59e0b'; // Amarelo - Moderado
  if (riskScore <= 75) return '#f97316'; // Laranja - Alto
  return '#ef4444'; // Vermelho - Muito alto
}

export function getRiskLabel(riskScore: number): string {
  if (riskScore <= 25) return 'Baixo';
  if (riskScore <= 50) return 'Moderado';
  if (riskScore <= 75) return 'Alto';
  return 'Muito Alto';
}

export function formatCurrency(value: number): string {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value);
}

export function formatPercentage(value: number): string {
  return `${value.toFixed(2)}%`;
}

export function formatNumber(value: number): string {
  return new Intl.NumberFormat('pt-BR').format(value);
}
