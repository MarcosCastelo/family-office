import React, { useState, useEffect } from 'react';
import { 
  Plus, 
  Search, 
  Edit, 
  Trash2, 
  Download, 
  Upload as UploadIcon,
  Filter,
  MoreHorizontal,
  Eye,
  PieChart,
  Activity,
  Users
} from 'lucide-react';
import { getAssets, createAsset, updateAsset, deleteAsset, type Asset } from '../services/assets';
import { useFamily } from '../contexts/FamilyContext';

// Asset interface now imported from services

export default function Assets() {
  const { selectedFamilyId } = useFamily();
  const [assets, setAssets] = useState<Asset[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [editingAsset, setEditingAsset] = useState<Asset | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');

  const [formData, setFormData] = useState({
    name: '',
    asset_type: 'renda_fixa',
    value: '',
    acquisition_date: '',
    details: {},
    ticker: ''
  });

  useEffect(() => {
    if (selectedFamilyId) {
      loadAssets();
    }
  }, [selectedFamilyId]);

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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedFamilyId) {
      setError('Selecione uma família');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const assetData = {
        ...formData,
        value: parseFloat(formData.value),
        family_id: selectedFamilyId,
        details: {
          ...formData.details,
          ...(formData.asset_type === 'renda_variavel' && formData.ticker ? { ticker: formData.ticker } : {})
        }
      };

      if (editingAsset) {
        await updateAsset(editingAsset.id, assetData, selectedFamilyId);
      } else {
        await createAsset(assetData);
      }

      setShowForm(false);
      setEditingAsset(null);
      resetForm();
      loadAssets();
    } catch (err: any) {
      console.error('Erro ao salvar ativo:', err);
      setError(err.response?.data?.error || 'Erro ao salvar ativo');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (assetId: number) => {
    if (!selectedFamilyId) return;
    
    if (!window.confirm('Tem certeza que deseja excluir este ativo?')) {
      return;
    }

    try {
      setLoading(true);
      setError(null);
      await deleteAsset(assetId, selectedFamilyId);
      loadAssets();
    } catch (err: any) {
      console.error('Erro ao excluir ativo:', err);
      setError(err.response?.data?.error || 'Erro ao excluir ativo');
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (asset: Asset) => {
    setEditingAsset(asset);
    setFormData({
      name: asset.name,
      asset_type: asset.asset_type,
      value: asset.value.toString(),
      acquisition_date: asset.acquisition_date,
      details: asset.details,
      ticker: asset.details?.ticker || ''
    });
    setShowForm(true);
  };

  const resetForm = () => {
    setFormData({
      name: '',
      asset_type: 'renda_fixa',
      value: '',
      acquisition_date: '',
      details: {},
      ticker: ''
    });
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR');
  };

  const getAssetTypeLabel = (type: string) => {
    const labels: { [key: string]: string } = {
      renda_fixa: 'Renda Fixa',
      renda_variavel: 'Renda Variável',
      multimercado: 'Multimercado',
      ativo_real: 'Ativo Real',
      estrategico: 'Estratégico',
      internacional: 'Internacional',
      alternativo: 'Alternativo',
      protecao: 'Proteção'
    };
    return labels[type] || type;
  };

  const filteredAssets = assets.filter(asset => {
    const matchesSearch = asset.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterType === 'all' || asset.asset_type === filterType;
    return matchesSearch && matchesFilter;
  });

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
          <div>Selecione uma família para gerenciar os ativos.</div>
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
          <PieChart size={28} />
          Gestão de Ativos
        </h1>
      </div>

      {/* Controles */}
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        marginBottom: 24,
        gap: 16
      }}>
        <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
          {/* Busca */}
          <div style={{ position: 'relative' }}>
            <Search size={16} style={{ 
              position: 'absolute', 
              left: 12, 
              top: '50%', 
              transform: 'translateY(-50%)',
              color: '#666'
            }} />
            <input
              type="text"
              placeholder="Buscar ativos..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{
                padding: '8px 12px 8px 36px',
                borderRadius: 8,
                border: '1px solid #ddd',
                fontSize: 14,
                minWidth: 200
              }}
            />
          </div>

          {/* Filtro por tipo */}
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            style={{
              padding: '8px 12px',
              borderRadius: 8,
              border: '1px solid #ddd',
              fontSize: 14,
              background: '#fff'
            }}
          >
            <option value="all">Todos os tipos</option>
            <option value="renda_fixa">Renda Fixa</option>
            <option value="renda_variavel">Renda Variável</option>
            <option value="multimercado">Multimercado</option>
            <option value="ativo_real">Ativo Real</option>
            <option value="estrategico">Estratégico</option>
            <option value="internacional">Internacional</option>
            <option value="alternativo">Alternativo</option>
            <option value="protecao">Proteção</option>
          </select>
        </div>

        <button
          onClick={() => {
            setShowForm(true);
            setEditingAsset(null);
            resetForm();
          }}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 8,
            padding: '10px 20px',
            borderRadius: 8,
            border: 'none',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            cursor: 'pointer',
            fontSize: 14,
            fontWeight: 500,
            transition: 'all 0.2s ease'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = 'translateY(-1px)';
            e.currentTarget.style.boxShadow = '0 4px 12px rgba(102, 126, 234, 0.3)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'translateY(0)';
            e.currentTarget.style.boxShadow = 'none';
          }}
        >
          <Plus size={16} />
          Novo Ativo
        </button>
      </div>

      {/* Formulário */}
      {showForm && (
        <div style={{
          background: '#f8f9fa',
          borderRadius: 12,
          padding: 24,
          marginBottom: 24,
          border: '1px solid #e9ecef'
        }}>
          <h3 style={{ 
            color: '#222', 
            marginBottom: 20, 
            fontSize: 18,
            fontWeight: 600
          }}>
            {editingAsset ? 'Editar Ativo' : 'Novo Ativo'}
          </h3>
          
          <form onSubmit={handleSubmit} style={{ display: 'grid', gap: 16 }}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
              <div>
                <label style={{ display: 'block', marginBottom: 4, color: '#666', fontSize: 14 }}>
                  Nome do Ativo *
                </label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  required
                  style={{
                    width: '100%',
                    padding: '10px 12px',
                    borderRadius: 8,
                    border: '1px solid #ddd',
                    fontSize: 14
                  }}
                />
              </div>

              <div>
                <label style={{ display: 'block', marginBottom: 4, color: '#666', fontSize: 14 }}>
                  Tipo de Ativo *
                </label>
                <select
                  value={formData.asset_type}
                  onChange={(e) => setFormData({...formData, asset_type: e.target.value})}
                  required
                  style={{
                    width: '100%',
                    padding: '10px 12px',
                    borderRadius: 8,
                    border: '1px solid #ddd',
                    fontSize: 14
                  }}
                >
                  <option value="renda_fixa">Renda Fixa</option>
                  <option value="renda_variavel">Renda Variável</option>
                  <option value="multimercado">Multimercado</option>
                  <option value="ativo_real">Ativo Real</option>
                  <option value="estrategico">Estratégico</option>
                  <option value="internacional">Internacional</option>
                  <option value="alternativo">Alternativo</option>
                  <option value="protecao">Proteção</option>
                </select>
              </div>

              <div>
                <label style={{ display: 'block', marginBottom: 4, color: '#666', fontSize: 14 }}>
                  Valor (R$) *
                </label>
                <input
                  type="number"
                  step="0.01"
                  value={formData.value}
                  onChange={(e) => setFormData({...formData, value: e.target.value})}
                  required
                  style={{
                    width: '100%',
                    padding: '10px 12px',
                    borderRadius: 8,
                    border: '1px solid #ddd',
                    fontSize: 14
                  }}
                />
              </div>

              <div>
                <label style={{ display: 'block', marginBottom: 4, color: '#666', fontSize: 14 }}>
                  Data de Aquisição *
                </label>
                <input
                  type="date"
                  value={formData.acquisition_date}
                  onChange={(e) => setFormData({...formData, acquisition_date: e.target.value})}
                  required
                  style={{
                    width: '100%',
                    padding: '10px 12px',
                    borderRadius: 8,
                    border: '1px solid #ddd',
                    fontSize: 14
                  }}
                />
              </div>

              {formData.asset_type === 'renda_variavel' && (
                <div>
                  <label style={{ display: 'block', marginBottom: 4, color: '#666', fontSize: 14 }}>
                    Ticker *
                  </label>
                  <input
                    type="text"
                    value={formData.ticker}
                    onChange={(e) => setFormData({...formData, ticker: e.target.value})}
                    required
                    style={{
                      width: '100%',
                      padding: '10px 12px',
                      borderRadius: 8,
                      border: '1px solid #ddd',
                      fontSize: 14
                    }}
                  />
                </div>
              )}
            </div>

            <div style={{ display: 'flex', gap: 12, justifyContent: 'flex-end' }}>
              <button
                type="button"
                onClick={() => {
                  setShowForm(false);
                  setEditingAsset(null);
                  resetForm();
                }}
                style={{
                  padding: '10px 20px',
                  borderRadius: 8,
                  border: '1px solid #ddd',
                  background: '#fff',
                  color: '#666',
                  cursor: 'pointer',
                  fontSize: 14
                }}
              >
                Cancelar
              </button>
              <button
                type="submit"
                disabled={loading}
                style={{
                  padding: '10px 20px',
                  borderRadius: 8,
                  border: 'none',
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  color: 'white',
                  cursor: 'pointer',
                  fontSize: 14,
                  fontWeight: 500,
                  opacity: loading ? 0.6 : 1
                }}
              >
                {loading ? 'Salvando...' : (editingAsset ? 'Atualizar' : 'Criar')}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Lista de Ativos */}
      {loading ? (
        <div style={{ 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center', 
          height: '200px',
          color: '#666'
        }}>
          <div style={{ textAlign: 'center' }}>
            <Activity size={32} style={{ marginBottom: 8, opacity: 0.6 }} />
            <div>Carregando ativos...</div>
          </div>
        </div>
      ) : error ? (
        <div style={{ 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center', 
          height: '200px',
          color: '#d32f2f'
        }}>
          <div style={{ textAlign: 'center' }}>
            <div>Erro: {error}</div>
          </div>
        </div>
      ) : filteredAssets.length === 0 ? (
        <div style={{ 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center', 
          height: '200px',
          color: '#666'
        }}>
          <div style={{ textAlign: 'center' }}>
            <PieChart size={48} style={{ marginBottom: 16, opacity: 0.6 }} />
            <div>Nenhum ativo encontrado</div>
          </div>
        </div>
      ) : (
        <div style={{ display: 'grid', gap: 12 }}>
          {filteredAssets.map((asset) => (
            <div key={asset.id} style={{
              background: '#fff',
              borderRadius: 12,
              padding: 20,
              border: '1px solid #e9ecef',
              boxShadow: '0 2px 8px rgba(0,0,0,0.04)',
              transition: 'all 0.2s ease'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.boxShadow = '0 4px 16px rgba(0,0,0,0.08)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 2px 8px rgba(0,0,0,0.04)';
            }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                    <h3 style={{ 
                      color: '#222', 
                      margin: 0, 
                      fontSize: 16,
                      fontWeight: 600
                    }}>
                      {asset.name}
                    </h3>
                    <span style={{
                      background: '#667eea',
                      color: 'white',
                      padding: '2px 8px',
                      borderRadius: 12,
                      fontSize: 11,
                      fontWeight: 500,
                      textTransform: 'uppercase'
                    }}>
                      {getAssetTypeLabel(asset.asset_type)}
                    </span>
                  </div>
                  
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, fontSize: 14 }}>
                    {/* Valor Atual (de transações) ou Valor Legacy */}
                    <div>
                      <span style={{ color: '#666' }}>
                        {asset.current_value !== undefined ? 'Valor Atual: ' : 'Valor: '}
                      </span>
                      <span style={{ fontWeight: 600, color: asset.current_value !== undefined ? '#22c55e' : '#667eea' }}>
                        {asset.current_value !== undefined 
                          ? formatCurrency(asset.current_value)
                          : formatCurrency(asset.value || 0)
                        }
                      </span>
                    </div>
                    
                    {/* Quantidade Atual */}
                    {asset.current_quantity !== undefined && (
                      <div>
                        <span style={{ color: '#666' }}>Quantidade: </span>
                        <span style={{ fontWeight: 600, color: '#8b5cf6' }}>
                          {asset.current_quantity.toLocaleString('pt-BR', { maximumFractionDigits: 6 })}
                        </span>
                      </div>
                    )}
                    
                    {/* Custo Médio */}
                    {asset.average_cost !== undefined && (
                      <div>
                        <span style={{ color: '#666' }}>Custo Médio: </span>
                        <span style={{ fontWeight: 600, color: '#f59e0b' }}>
                          {formatCurrency(asset.average_cost)}
                        </span>
                      </div>
                    )}
                    
                    {/* Total Investido */}
                    {asset.total_invested !== undefined && (
                      <div>
                        <span style={{ color: '#666' }}>Investido: </span>
                        <span style={{ fontWeight: 600, color: '#10b981' }}>
                          {formatCurrency(asset.total_invested)}
                        </span>
                      </div>
                    )}
                    
                    {/* Ganho/Perda Não Realizado */}
                    {asset.unrealized_gain_loss !== undefined && (
                      <div>
                        <span style={{ color: '#666' }}>G/P Não Real.: </span>
                        <span style={{ 
                          fontWeight: 600, 
                          color: asset.unrealized_gain_loss > 0 ? '#22c55e' : asset.unrealized_gain_loss < 0 ? '#ef4444' : '#666'
                        }}>
                          {formatCurrency(asset.unrealized_gain_loss)}
                        </span>
                      </div>
                    )}
                    
                    {/* Número de Transações */}
                    {asset.transaction_count !== undefined && (
                      <div>
                        <span style={{ color: '#666' }}>Transações: </span>
                        <span style={{ fontWeight: 600, color: '#667eea' }}>
                          {asset.transaction_count}
                        </span>
                      </div>
                    )}
                    
                    {/* Data de Aquisição (se disponível) */}
                    {asset.acquisition_date && (
                      <div>
                        <span style={{ color: '#666' }}>Aquisição: </span>
                        <span style={{ fontWeight: 500 }}>
                          {formatDate(asset.acquisition_date)}
                        </span>
                      </div>
                    )}
                    
                    {/* Ticker (se disponível) */}
                    {asset.details?.ticker && (
                      <div>
                        <span style={{ color: '#666' }}>Ticker: </span>
                        <span style={{ fontWeight: 500, color: '#28a745' }}>
                          {asset.details.ticker}
                        </span>
                      </div>
                    )}
                  </div>
                </div>

                <div style={{ display: 'flex', gap: 8 }}>
                  <button
                    onClick={() => handleEdit(asset)}
                    style={{
                      padding: '6px',
                      borderRadius: 6,
                      border: 'none',
                      background: '#f8f9fa',
                      color: '#666',
                      cursor: 'pointer',
                      transition: 'all 0.2s ease'
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.background = '#e9ecef';
                      e.currentTarget.style.color = '#333';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.background = '#f8f9fa';
                      e.currentTarget.style.color = '#666';
                    }}
                    title="Editar"
                  >
                    <Edit size={14} />
                  </button>

                  <button
                    onClick={() => {
                      // Navigate to transactions page for this asset
                      const event = new CustomEvent('navigate-to-transactions', { 
                        detail: { assetId: asset.id } 
                      });
                      window.dispatchEvent(event);
                    }}
                    style={{
                      padding: '6px',
                      borderRadius: 6,
                      border: 'none',
                      background: '#f8f9fa',
                      color: '#667eea',
                      cursor: 'pointer',
                      transition: 'all 0.2s ease'
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.background = '#eef2ff';
                      e.currentTarget.style.color = '#5a67d8';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.background = '#f8f9fa';
                      e.currentTarget.style.color = '#667eea';
                    }}
                    title="Ver Transações"
                  >
                    <Activity size={14} />
                  </button>
                  
                  <button
                    onClick={() => handleDelete(asset.id)}
                    style={{
                      padding: '6px',
                      borderRadius: 6,
                      border: 'none',
                      background: '#f8f9fa',
                      color: '#dc3545',
                      cursor: 'pointer',
                      transition: 'all 0.2s ease'
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.background = '#f8d7da';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.background = '#f8f9fa';
                    }}
                    title="Excluir"
                  >
                    <Trash2 size={14} />
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