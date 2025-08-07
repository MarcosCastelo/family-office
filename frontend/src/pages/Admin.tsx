import React, { useState, useEffect } from 'react';
import { 
  Users, 
  Shield, 
  Home, 
  BarChart3, 
  Settings,
  Plus,
  Edit,
  Trash2,
  Eye,
  UserCheck,
  UserX
} from 'lucide-react';
import { getAdminDashboard } from '../services/admin';

interface AdminDashboardData {
  metrics: {
    total_users: number;
    active_users: number;
    total_families: number;
    total_permissions: number;
  };
  families: Array<{
    id: number;
    name: string;
    user_count: number;
  }>;
  permissions: Array<{
    id: number;
    name: string;
    user_count: number;
  }>;
}

export default function Admin() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [dashboardData, setDashboardData] = useState<AdminDashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (activeTab === 'dashboard') {
      loadDashboardData();
    }
  }, [activeTab]);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getAdminDashboard();
      setDashboardData(data);
    } catch (err: any) {
      console.error('Erro ao carregar dashboard administrativo:', err);
      setError(err.response?.data?.error || 'Erro ao carregar dados administrativos');
    } finally {
      setLoading(false);
    }
  };

  const formatNumber = (value: number) => {
    return new Intl.NumberFormat('pt-BR').format(value);
  };

  const renderDashboard = () => {
    if (loading) {
      return (
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <div>Carregando dados administrativos...</div>
        </div>
      );
    }

    if (error) {
      return (
        <div style={{ textAlign: 'center', padding: '40px', color: '#d32f2f' }}>
          <div>Erro: {error}</div>
        </div>
      );
    }

    if (!dashboardData) {
      return (
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <div>Nenhum dado disponível</div>
        </div>
      );
    }

    return (
      <div>
        <h2 style={{ marginBottom: '24px', color: '#333' }}>Dashboard Administrativo</h2>
        
        {/* Métricas */}
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
          gap: '16px', 
          marginBottom: '32px' 
        }}>
          <div style={{
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            padding: '24px',
            borderRadius: '12px',
            color: 'white',
            textAlign: 'center'
          }}>
            <Users size={32} style={{ marginBottom: '8px' }} />
            <div style={{ fontSize: '24px', fontWeight: 'bold' }}>
              {formatNumber(dashboardData.metrics.total_users)}
            </div>
            <div style={{ fontSize: '14px', opacity: 0.9 }}>Total de Usuários</div>
          </div>

          <div style={{
            background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
            padding: '24px',
            borderRadius: '12px',
            color: 'white',
            textAlign: 'center'
          }}>
            <UserCheck size={32} style={{ marginBottom: '8px' }} />
            <div style={{ fontSize: '24px', fontWeight: 'bold' }}>
              {formatNumber(dashboardData.metrics.active_users)}
            </div>
            <div style={{ fontSize: '14px', opacity: 0.9 }}>Usuários Ativos</div>
          </div>

          <div style={{
            background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
            padding: '24px',
            borderRadius: '12px',
            color: 'white',
            textAlign: 'center'
          }}>
            <Home size={32} style={{ marginBottom: '8px' }} />
            <div style={{ fontSize: '24px', fontWeight: 'bold' }}>
              {formatNumber(dashboardData.metrics.total_families)}
            </div>
            <div style={{ fontSize: '14px', opacity: 0.9 }}>Famílias</div>
          </div>

          <div style={{
            background: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
            padding: '24px',
            borderRadius: '12px',
            color: 'white',
            textAlign: 'center'
          }}>
            <Shield size={32} style={{ marginBottom: '8px' }} />
            <div style={{ fontSize: '24px', fontWeight: 'bold' }}>
              {formatNumber(dashboardData.metrics.total_permissions)}
            </div>
            <div style={{ fontSize: '14px', opacity: 0.9 }}>Permissões</div>
          </div>
        </div>

        {/* Famílias */}
        <div style={{ marginBottom: '32px' }}>
          <h3 style={{ marginBottom: '16px', color: '#333' }}>Famílias</h3>
          <div style={{
            background: 'white',
            borderRadius: '8px',
            padding: '16px',
            boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
          }}>
            {dashboardData.families.map(family => (
              <div key={family.id} style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                padding: '12px 0',
                borderBottom: '1px solid #eee'
              }}>
                <div>
                  <div style={{ fontWeight: '500' }}>{family.name}</div>
                  <div style={{ fontSize: '14px', color: '#666' }}>
                    {family.user_count} usuário{family.user_count !== 1 ? 's' : ''}
                  </div>
                </div>
                <div style={{ display: 'flex', gap: '8px' }}>
                  <button style={{
                    padding: '6px 12px',
                    borderRadius: '6px',
                    border: '1px solid #ddd',
                    background: 'white',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px'
                  }}>
                    <Eye size={16} />
                    Ver
                  </button>
                  <button style={{
                    padding: '6px 12px',
                    borderRadius: '6px',
                    border: '1px solid #ddd',
                    background: 'white',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px'
                  }}>
                    <Edit size={16} />
                    Editar
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Permissões */}
        <div>
          <h3 style={{ marginBottom: '16px', color: '#333' }}>Permissões</h3>
          <div style={{
            background: 'white',
            borderRadius: '8px',
            padding: '16px',
            boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
          }}>
            {dashboardData.permissions.map(permission => (
              <div key={permission.id} style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                padding: '12px 0',
                borderBottom: '1px solid #eee'
              }}>
                <div>
                  <div style={{ fontWeight: '500' }}>{permission.name}</div>
                  <div style={{ fontSize: '14px', color: '#666' }}>
                    {permission.user_count} usuário{permission.user_count !== 1 ? 's' : ''}
                  </div>
                </div>
                <div style={{ display: 'flex', gap: '8px' }}>
                  <button style={{
                    padding: '6px 12px',
                    borderRadius: '6px',
                    border: '1px solid #ddd',
                    background: 'white',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px'
                  }}>
                    <Edit size={16} />
                    Editar
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  const renderUsers = () => {
    return (
      <div>
        <h2 style={{ marginBottom: '24px', color: '#333' }}>Gestão de Usuários</h2>
        <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
          <Users size={48} style={{ marginBottom: '16px', opacity: 0.5 }} />
          <div>Interface de gestão de usuários em desenvolvimento</div>
        </div>
      </div>
    );
  };

  const renderFamilies = () => {
    return (
      <div>
        <h2 style={{ marginBottom: '24px', color: '#333' }}>Gestão de Famílias</h2>
        <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
          <Home size={48} style={{ marginBottom: '16px', opacity: 0.5 }} />
          <div>Interface de gestão de famílias em desenvolvimento</div>
        </div>
      </div>
    );
  };

  const renderPermissions = () => {
    return (
      <div>
        <h2 style={{ marginBottom: '24px', color: '#333' }}>Gestão de Permissões</h2>
        <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
          <Shield size={48} style={{ marginBottom: '16px', opacity: 0.5 }} />
          <div>Interface de gestão de permissões em desenvolvimento</div>
        </div>
      </div>
    );
  };

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return renderDashboard();
      case 'users':
        return renderUsers();
      case 'families':
        return renderFamilies();
      case 'permissions':
        return renderPermissions();
      default:
        return renderDashboard();
    }
  };

  return (
    <div>
      {/* Navegação */}
      <div style={{
        display: 'flex',
        gap: '8px',
        marginBottom: '32px',
        borderBottom: '1px solid #eee',
        paddingBottom: '16px'
      }}>
        <button
          onClick={() => setActiveTab('dashboard')}
          style={{
            padding: '12px 20px',
            borderRadius: '8px',
            border: 'none',
            background: activeTab === 'dashboard' ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' : '#f5f5f5',
            color: activeTab === 'dashboard' ? 'white' : '#333',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            fontWeight: '500'
          }}
        >
          <BarChart3 size={20} />
          Dashboard
        </button>

        <button
          onClick={() => setActiveTab('users')}
          style={{
            padding: '12px 20px',
            borderRadius: '8px',
            border: 'none',
            background: activeTab === 'users' ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' : '#f5f5f5',
            color: activeTab === 'users' ? 'white' : '#333',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            fontWeight: '500'
          }}
        >
          <Users size={20} />
          Usuários
        </button>

        <button
          onClick={() => setActiveTab('families')}
          style={{
            padding: '12px 20px',
            borderRadius: '8px',
            border: 'none',
            background: activeTab === 'families' ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' : '#f5f5f5',
            color: activeTab === 'families' ? 'white' : '#333',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            fontWeight: '500'
          }}
        >
          <Home size={20} />
          Famílias
        </button>

        <button
          onClick={() => setActiveTab('permissions')}
          style={{
            padding: '12px 20px',
            borderRadius: '8px',
            border: 'none',
            background: activeTab === 'permissions' ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' : '#f5f5f5',
            color: activeTab === 'permissions' ? 'white' : '#333',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            fontWeight: '500'
          }}
        >
          <Shield size={20} />
          Permissões
        </button>
      </div>

      {/* Conteúdo */}
      {renderContent()}
    </div>
  );
} 