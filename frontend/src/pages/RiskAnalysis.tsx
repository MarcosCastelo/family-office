import React, { useState, useEffect } from 'react';
import { getFamilyRiskSummary, getAssetRisk, triggerRiskRecalculation } from '../services/risk';
import { getAssets } from '../services/assets';
import { getUserFamilies } from '../services/family';
import type { RiskSummary, AssetRisk } from '../services/risk';
import type { Asset } from '../services/assets';

interface Family {
  id: number;
  name: string;
}

export default function RiskAnalysis() {
  const [families, setFamilies] = useState<Family[]>([]);
  const [selectedFamilyId, setSelectedFamilyId] = useState<number | null>(null);
  const [riskSummary, setRiskSummary] = useState<RiskSummary | null>(null);
  const [assets, setAssets] = useState<Asset[]>([]);
  const [assetRisks, setAssetRisks] = useState<AssetRisk[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [recalculating, setRecalculating] = useState(false);

  useEffect(() => {
    loadFamilies();
  }, []);

  useEffect(() => {
    if (selectedFamilyId) {
      loadRiskData();
    }
  }, [selectedFamilyId]);

  const loadFamilies = async () => {
    try {
      setLoading(true);
      setError(null);
      const familiesData = await getUserFamilies();
      setFamilies(familiesData);
      
      if (familiesData.length > 0) {
        setSelectedFamilyId(familiesData[0].id);
      }
    } catch (err: any) {
      console.error('Erro ao carregar famílias:', err);
      setError(err.response?.data?.error || 'Erro ao carregar famílias');
    } finally {
      setLoading(false);
    }
  };

  const loadRiskData = async () => {
    if (!selectedFamilyId) return;
    
    try {
      setLoading(true);
      setError(null);
      
      // Carregar resumo de risco e ativos em paralelo
      const [riskData, assetsData] = await Promise.all([
        getFamilyRiskSummary(selectedFamilyId),
        getAssets(selectedFamilyId)
      ]);
      
      setRiskSummary(riskData);
      setAssets(assetsData);
      
      // Carregar risco individual de cada ativo
      const assetRiskPromises = assetsData.map((asset: Asset) => 
        getAssetRisk(asset.id!, selectedFamilyId)
      );
      const assetRisksData = await Promise.all(assetRiskPromises);
      setAssetRisks(assetRisksData);
      
    } catch (err: any) {
      console.error('Erro ao carregar dados de risco:', err);
      setError(err.response?.data?.error || 'Erro ao carregar dados de risco');
    } finally {
      setLoading(false);
    }
  };

  const handleRecalculateRisk = async () => {
    if (!selectedFamilyId) return;
    
    try {
      setRecalculating(true);
      await triggerRiskRecalculation(selectedFamilyId);
      await loadRiskData(); // Recarrega os dados após recálculo
      alert('Análise de risco recalculada com sucesso!');
    } catch (err: any) {
      console.error('Erro ao recalculcar risco:', err);
      alert(err.response?.data?.error || 'Erro ao recalculcar risco');
    } finally {
      setRecalculating(false);
    }
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

  const getRiskLabel = (classification: string) => {
    switch (classification.toLowerCase()) {
      case 'crítico':
        return 'Crítico';
      case 'alto':
        return 'Alto';
      case 'médio':
        return 'Médio';
      case 'baixo':
        return 'Baixo';
      default:
        return classification;
    }
  };

  if (loading && !selectedFamilyId) {
    return (
      <div style={{ padding: 24, textAlign: 'center', color: '#666' }}>
        Carregando famílias...
      </div>
    );
  }

  if (error && !selectedFamilyId) {
    return (
      <div style={{ padding: 24, textAlign: 'center', color: '#d32f2f' }}>
        Erro: {error}
      </div>
    );
  }

  if (families.length === 0) {
    return (
      <div style={{ padding: 24, textAlign: 'center', color: '#666' }}>
        Você não tem acesso a nenhuma família.
      </div>
    );
  }

  return (
    <div style={{ padding: 24, maxWidth: 1200, margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <h1 style={{ color: '#222', margin: 0 }}>Análise de Risco</h1>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          {/* Seletor de Família */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <label style={{ color: '#666', fontSize: 14 }}>Família:</label>
            <select 
              value={selectedFamilyId || ''} 
              onChange={(e) => setSelectedFamilyId(Number(e.target.value))}
              style={{
                padding: '8px 12px',
                borderRadius: 8,
                border: '1px solid #ccc',
                fontSize: 14,
                background: '#fff'
              }}
            >
              {families.map((family) => (
                <option key={family.id} value={family.id}>
                  {family.name}
                </option>
              ))}
            </select>
          </div>

          {/* Botão Recalcular */}
          <button
            onClick={handleRecalculateRisk}
            disabled={recalculating}
            style={{
              padding: '8px 16px',
              borderRadius: 8,
              background: recalculating ? '#ccc' : 'linear-gradient(90deg, #4caf50 0%, #45a049 100%)',
              color: '#fff',
              border: 'none',
              cursor: recalculating ? 'not-allowed' : 'pointer',
              fontSize: 14,
              fontWeight: 500
            }}
          >
            {recalculating ? 'Recalculando...' : 'Recalcular Risco'}
          </button>
        </div>
      </div>

      {loading && selectedFamilyId ? (
        <div style={{ padding: 24, textAlign: 'center', color: '#666' }}>
          Carregando análise de risco...
        </div>
      ) : error && selectedFamilyId ? (
        <div style={{ padding: 24, textAlign: 'center', color: '#d32f2f' }}>
          Erro: {error}
        </div>
      ) : riskSummary ? (
        <>
          {/* Resumo de Risco */}
          <div style={{
            background: '#fff',
            borderRadius: 16,
            padding: 24,
            marginBottom: 24,
            boxShadow: '0 4px 24px rgba(0,0,0,0.08)'
          }}>
            <h2 style={{ color: '#222', marginBottom: 20 }}>Resumo de Risco da Família</h2>
            
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 20 }}>
              {/* Score Global */}
              <div style={{
                background: `linear-gradient(135deg, ${getRiskColor(riskSummary.classificacao_final)}20 0%, ${getRiskColor(riskSummary.classificacao_final)}10 100%)`,
                borderRadius: 12,
                padding: 20,
                border: `2px solid ${getRiskColor(riskSummary.classificacao_final)}`
              }}>
                <h3 style={{ color: '#222', marginBottom: 8, fontSize: 16 }}>Score Global</h3>
                <div style={{ fontSize: 32, fontWeight: 'bold', color: getRiskColor(riskSummary.classificacao_final) }}>
                  {riskSummary.score_global}
                </div>
                <div style={{ 
                  color: getRiskColor(riskSummary.classificacao_final), 
                  fontWeight: 600,
                  fontSize: 14 
                }}>
                  {getRiskLabel(riskSummary.classificacao_final)}
                </div>
              </div>

              {/* Concentração */}
              <div style={{
                background: '#f5f5f5',
                borderRadius: 12,
                padding: 20
              }}>
                <h3 style={{ color: '#222', marginBottom: 8, fontSize: 16 }}>Concentração</h3>
                <div style={{ fontSize: 24, fontWeight: 'bold', color: '#222' }}>
                  {riskSummary.concentracao}%
                </div>
                <div style={{ color: '#666', fontSize: 12 }}>
                  Maior ativo / Total
                </div>
              </div>

              {/* Volatilidade */}
              <div style={{
                background: '#f5f5f5',
                borderRadius: 12,
                padding: 20
              }}>
                <h3 style={{ color: '#222', marginBottom: 8, fontSize: 16 }}>Volatilidade</h3>
                <div style={{ fontSize: 24, fontWeight: 'bold', color: '#222' }}>
                  {riskSummary.volatilidade}%
                </div>
                <div style={{ color: '#666', fontSize: 12 }}>
                  % Renda Variável
                </div>
              </div>

              {/* Liquidez */}
              <div style={{
                background: '#f5f5f5',
                borderRadius: 12,
                padding: 20
              }}>
                <h3 style={{ color: '#222', marginBottom: 8, fontSize: 16 }}>Liquidez</h3>
                <div style={{ fontSize: 24, fontWeight: 'bold', color: '#222' }}>
                  {riskSummary.liquidez_aggregada}%
                </div>
                <div style={{ color: '#666', fontSize: 12 }}>
                  Ativos Ilíquidos
                </div>
              </div>

              {/* Exposição Cambial */}
              <div style={{
                background: '#f5f5f5',
                borderRadius: 12,
                padding: 20
              }}>
                <h3 style={{ color: '#222', marginBottom: 8, fontSize: 16 }}>Exposição Cambial</h3>
                <div style={{ fontSize: 24, fontWeight: 'bold', color: '#222' }}>
                  {riskSummary.exposicao_cambial}%
                </div>
                <div style={{ color: '#666', fontSize: 12 }}>
                  % Ativos em Moeda Estrangeira
                </div>
              </div>

              {/* Risco Fiscal/Regulatório */}
              <div style={{
                background: '#f5f5f5',
                borderRadius: 12,
                padding: 20
              }}>
                <h3 style={{ color: '#222', marginBottom: 8, fontSize: 16 }}>Risco Fiscal</h3>
                <div style={{ fontSize: 24, fontWeight: 'bold', color: '#222' }}>
                  {riskSummary.risco_fiscal_regulatorio}%
                </div>
                <div style={{ color: '#666', fontSize: 12 }}>
                  Regulatório
                </div>
              </div>
            </div>
          </div>

          {/* Análise Individual por Ativo */}
          <div style={{
            background: '#fff',
            borderRadius: 16,
            padding: 24,
            boxShadow: '0 4px 24px rgba(0,0,0,0.08)'
          }}>
            <h2 style={{ color: '#222', marginBottom: 20 }}>Análise Individual por Ativo</h2>
            
            {assetRisks.length > 0 ? (
              <div style={{ overflowX: 'auto' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                  <thead>
                    <tr style={{ borderBottom: '1px solid #eee' }}>
                      <th style={{ textAlign: 'left', padding: '12px 0', color: '#666', fontWeight: 600 }}>Ativo</th>
                      <th style={{ textAlign: 'center', padding: '12px 0', color: '#666', fontWeight: 600 }}>Risco de Mercado</th>
                      <th style={{ textAlign: 'center', padding: '12px 0', color: '#666', fontWeight: 600 }}>Liquidez</th>
                      <th style={{ textAlign: 'center', padding: '12px 0', color: '#666', fontWeight: 600 }}>Concentração</th>
                      <th style={{ textAlign: 'center', padding: '12px 0', color: '#666', fontWeight: 600 }}>Governança</th>
                      <th style={{ textAlign: 'center', padding: '12px 0', color: '#666', fontWeight: 600 }}>Classificação</th>
                    </tr>
                  </thead>
                  <tbody>
                    {assetRisks.map((assetRisk) => (
                      <tr key={assetRisk.id} style={{ borderBottom: '1px solid #f5f5f5' }}>
                        <td style={{ padding: '12px 0', color: '#222' }}>{assetRisk.name}</td>
                        <td style={{ textAlign: 'center', padding: '12px 0' }}>
                          <span style={{
                            padding: '4px 8px',
                            borderRadius: 4,
                            fontSize: 12,
                            fontWeight: 500,
                            color: getRiskColor(assetRisk.risco_mercado),
                            background: `${getRiskColor(assetRisk.risco_mercado)}20`
                          }}>
                            {getRiskLabel(assetRisk.risco_mercado)}
                          </span>
                        </td>
                        <td style={{ textAlign: 'center', padding: '12px 0' }}>
                          <span style={{
                            padding: '4px 8px',
                            borderRadius: 4,
                            fontSize: 12,
                            fontWeight: 500,
                            color: getRiskColor(assetRisk.risco_liquidez),
                            background: `${getRiskColor(assetRisk.risco_liquidez)}20`
                          }}>
                            {getRiskLabel(assetRisk.risco_liquidez)}
                          </span>
                        </td>
                        <td style={{ textAlign: 'center', padding: '12px 0' }}>
                          <span style={{
                            padding: '4px 8px',
                            borderRadius: 4,
                            fontSize: 12,
                            fontWeight: 500,
                            color: getRiskColor(assetRisk.risco_concentracao),
                            background: `${getRiskColor(assetRisk.risco_concentracao)}20`
                          }}>
                            {getRiskLabel(assetRisk.risco_concentracao)}
                          </span>
                        </td>
                        <td style={{ textAlign: 'center', padding: '12px 0', color: '#222', fontWeight: 500 }}>
                          {assetRisk.score_governanca}
                        </td>
                        <td style={{ textAlign: 'center', padding: '12px 0' }}>
                          <span style={{
                            padding: '6px 12px',
                            borderRadius: 6,
                            fontSize: 12,
                            fontWeight: 600,
                            color: '#fff',
                            background: getRiskColor(assetRisk.classificacao_final)
                          }}>
                            {getRiskLabel(assetRisk.classificacao_final)}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div style={{ textAlign: 'center', padding: '24px 0', color: '#666' }}>
                Nenhum ativo encontrado para análise
              </div>
            )}
          </div>
        </>
      ) : (
        <div style={{ textAlign: 'center', padding: '24px 0', color: '#666' }}>
          Selecione uma família para visualizar a análise de risco
        </div>
      )}
    </div>
  );
} 