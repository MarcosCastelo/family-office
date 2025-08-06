import axios from 'axios';

const API_URL = 'http://localhost:5000';

export interface RiskSummary {
  family_id: number;
  score_global: number;
  concentracao: number;
  volatilidade: number;
  liquidez_aggregada: number;
  exposicao_cambial: number;
  risco_fiscal_regulatorio: number;
  classificacao_final: string;
}

export interface AssetRisk {
  id: number;
  name: string;
  risco_mercado: string;
  risco_liquidez: string;
  risco_concentracao: string;
  risco_credito: string;
  risco_cambial: string;
  risco_juridico_fiscal: string;
  score_governanca: number;
  classificacao_final: string;
}

export async function getFamilyRiskSummary(familyId: number): Promise<RiskSummary> {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Token de acesso não encontrado');
  }

  const response = await axios.get(`${API_URL}/families/${familyId}/risk/summary`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  return response.data;
}

export async function getAssetRisk(assetId: number, familyId: number): Promise<AssetRisk> {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Token de acesso não encontrado');
  }

  const response = await axios.get(`${API_URL}/assets/${assetId}/risk`, {
    headers: {
      'Authorization': `Bearer ${token}`
    },
    params: {
      family_id: familyId
    }
  });
  
  return response.data;
}

export async function triggerRiskRecalculation(familyId: number): Promise<void> {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Token de acesso não encontrado');
  }

  await axios.post(`${API_URL}/families/${familyId}/risk/trigger`, {}, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
} 