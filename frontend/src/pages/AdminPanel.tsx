import React, { useState, useEffect } from 'react';
import { 
  Users, 
  Shield, 
  Home, 
  BarChart3,
  Plus,
  Edit,
  Trash2,
  Eye,
  UserCheck,
  LogOut,
  X
} from 'lucide-react';
import { 
  getAdminDashboard, 
  getUsers, 
  getFamilies, 
  getPermissions, 
  createUser, 
  updateUser, 
  deleteUser,
  getUserDetails,
  createFamily,
  updateFamily,
  deleteFamily,
  createPermission,
  updatePermission,
  deletePermission,
  addUserToFamily,
  removeUserFromFamily,
  type User, 
  type Family, 
  type Permission 
} from '../services/admin';

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

export default function AdminPanel() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [dashboardData, setDashboardData] = useState<AdminDashboardData | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [families, setFamilies] = useState<Family[]>([]);
  const [permissions, setPermissions] = useState<Permission[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  // Estados para modais
  const [showUserModal, setShowUserModal] = useState(false);
  const [showFamilyModal, setShowFamilyModal] = useState(false);
  const [showPermissionModal, setShowPermissionModal] = useState(false);
  const [showUserFamiliesModal, setShowUserFamiliesModal] = useState(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);
  const [editingFamily, setEditingFamily] = useState<Family | null>(null);
  const [editingPermission, setEditingPermission] = useState<Permission | null>(null);
  const [selectedUserForFamilies, setSelectedUserForFamilies] = useState<User | null>(null);

  // Estados para formulários
  const [userForm, setUserForm] = useState({ email: '', password: '', active: true });
  const [familyForm, setFamilyForm] = useState({ name: '' });
  const [permissionForm, setPermissionForm] = useState({ name: '', description: '' });

  useEffect(() => {
    // Verificar se já está autenticado
    const token = localStorage.getItem('access_token');
    if (token) {
      setIsAuthenticated(true);
      loadData();
    }
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      if (activeTab === 'dashboard') {
        const data = await getAdminDashboard();
        setDashboardData(data);
      } else if (activeTab === 'users') {
        const data = await getUsers();
        setUsers(data);
      } else if (activeTab === 'families') {
        const data = await getFamilies();
        setFamilies(data);
      } else if (activeTab === 'permissions') {
        const data = await getPermissions();
        setPermissions(data);
      }
    } catch (err: any) {
      console.error('Erro ao carregar dados:', err);
      if (err.response?.status === 401) {
        setIsAuthenticated(false);
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
      }
      setError(err.response?.data?.error || 'Erro ao carregar dados');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isAuthenticated) {
      loadData();
    }
  }, [activeTab, isAuthenticated]);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch('http://localhost:5000/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();
      
      if (response.ok) {
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('refresh_token', data.refresh_token);
        setIsAuthenticated(true);
      } else {
        setError(data.error || 'Erro no login');
      }
    } catch (err: any) {
      setError('Erro de conexão');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setIsAuthenticated(false);
    setDashboardData(null);
    setUsers([]);
    setFamilies([]);
    setPermissions([]);
  };

  // Funções para usuários
  const openUserModal = (user?: User) => {
    if (user) {
      setEditingUser(user);
      setUserForm({ email: user.email, password: '', active: user.active });
    } else {
      setEditingUser(null);
      setUserForm({ email: '', password: '', active: true });
    }
    setShowUserModal(true);
  };

  const handleUserSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setLoading(true);
      if (editingUser) {
        await updateUser(editingUser.id, userForm);
      } else {
        await createUser(userForm);
      }
      setShowUserModal(false);
      loadData();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Erro ao salvar usuário');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteUser = async (userId: number) => {
    if (window.confirm('Tem certeza que deseja excluir este usuário?')) {
      try {
        await deleteUser(userId);
        loadData();
      } catch (err: any) {
        setError(err.response?.data?.error || 'Erro ao excluir usuário');
      }
    }
  };

  // Funções para famílias
  const openFamilyModal = (family?: Family) => {
    if (family) {
      setEditingFamily(family);
      setFamilyForm({ name: family.name });
    } else {
      setEditingFamily(null);
      setFamilyForm({ name: '' });
    }
    setShowFamilyModal(true);
  };

  const handleFamilySubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setLoading(true);
      if (editingFamily) {
        await updateFamily(editingFamily.id, familyForm);
      } else {
        await createFamily(familyForm);
      }
      setShowFamilyModal(false);
      loadData();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Erro ao salvar família');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteFamily = async (familyId: number) => {
    if (window.confirm('Tem certeza que deseja excluir esta família?')) {
      try {
        await deleteFamily(familyId);
        loadData();
      } catch (err: any) {
        setError(err.response?.data?.error || 'Erro ao excluir família');
      }
    }
  };

  // Funções para permissões
  const openPermissionModal = (permission?: Permission) => {
    if (permission) {
      setEditingPermission(permission);
      setPermissionForm({ name: permission.name, description: permission.description || '' });
    } else {
      setEditingPermission(null);
      setPermissionForm({ name: '', description: '' });
    }
    setShowPermissionModal(true);
  };

  const handlePermissionSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setLoading(true);
      if (editingPermission) {
        await updatePermission(editingPermission.id, permissionForm);
      } else {
        await createPermission(permissionForm);
      }
      setShowPermissionModal(false);
      loadData();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Erro ao salvar permissão');
    } finally {
      setLoading(false);
    }
  };

  const handleDeletePermission = async (permissionId: number) => {
    if (window.confirm('Tem certeza que deseja excluir esta permissão?')) {
      try {
        await deletePermission(permissionId);
        loadData();
      } catch (err: any) {
        setError(err.response?.data?.error || 'Erro ao excluir permissão');
      }
    }
  };

  // Funções para associação de usuários e famílias
  const openUserFamiliesModal = async (user: User) => {
    try {
      setLoading(true);
      // Carregar detalhes completos do usuário
      const userDetails = await getUserDetails(user.id);
      setSelectedUserForFamilies(userDetails);
      setShowUserFamiliesModal(true);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Erro ao carregar detalhes do usuário');
    } finally {
      setLoading(false);
    }
  };

  const handleAddUserToFamily = async (familyId: number) => {
    if (!selectedUserForFamilies) return;
    
    try {
      setLoading(true);
      await addUserToFamily(familyId, selectedUserForFamilies.id);
      // Recarregar detalhes do usuário
      const userDetails = await getUserDetails(selectedUserForFamilies.id);
      setSelectedUserForFamilies(userDetails);
      loadData(); // Recarregar dados gerais
    } catch (err: any) {
      setError(err.response?.data?.error || 'Erro ao associar usuário à família');
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveUserFromFamily = async (familyId: number) => {
    if (!selectedUserForFamilies) return;
    
    if (window.confirm('Tem certeza que deseja remover este usuário da família?')) {
      try {
        setLoading(true);
        await removeUserFromFamily(familyId, selectedUserForFamilies.id);
        // Recarregar detalhes do usuário
        const userDetails = await getUserDetails(selectedUserForFamilies.id);
        setSelectedUserForFamilies(userDetails);
        loadData(); // Recarregar dados gerais
      } catch (err: any) {
        setError(err.response?.data?.error || 'Erro ao remover usuário da família');
      } finally {
        setLoading(false);
      }
    }
  };

  const formatNumber = (value: number) => {
    return new Intl.NumberFormat('pt-BR').format(value);
  };

  // Componente Modal
  const Modal = ({ isOpen, onClose, title, children }: { 
    isOpen: boolean; 
    onClose: () => void; 
    title: string; 
    children: React.ReactNode; 
  }) => {
    if (!isOpen) return null;

    return (
      <div style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'rgba(0,0,0,0.5)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000
      }}>
        <div style={{
          background: 'white',
          borderRadius: '12px',
          padding: '24px',
          minWidth: '400px',
          maxWidth: '500px',
          width: '100%',
          maxHeight: '90vh',
          overflow: 'auto'
        }}>
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: '24px'
          }}>
            <h2 style={{ margin: 0, color: '#333' }}>{title}</h2>
            <button
              onClick={onClose}
              style={{
                background: 'none',
                border: 'none',
                cursor: 'pointer',
                padding: '4px'
              }}
            >
              <X size={24} />
            </button>
          </div>
          {children}
        </div>
      </div>
    );
  };

  const renderLogin = () => {
    return (
      <div style={{ 
        minHeight: '100vh', 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
      }}>
        <div style={{ 
          background: 'white', 
          padding: '40px', 
          borderRadius: '16px', 
          boxShadow: '0 8px 32px rgba(0,0,0,0.1)', 
          minWidth: '400px',
          maxWidth: '500px',
          width: '100%'
        }}>
          <div style={{ textAlign: 'center', marginBottom: '32px' }}>
            <Shield size={48} style={{ color: '#667eea', marginBottom: '16px' }} />
            <h1 style={{ color: '#333', margin: 0 }}>Painel Administrativo</h1>
            <p style={{ color: '#666', margin: '8px 0 0 0' }}>Family Office Digital</p>
          </div>

          <form onSubmit={handleLogin}>
            <div style={{ marginBottom: '20px' }}>
              <label style={{ display: 'block', marginBottom: '8px', color: '#333', fontWeight: '500' }}>
                E-mail
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                style={{
                  width: '100%',
                  padding: '12px',
                  borderRadius: '8px',
                  border: '1px solid #ddd',
                  fontSize: '16px',
                  boxSizing: 'border-box'
                }}
                placeholder="admin@admin.com"
              />
            </div>

            <div style={{ marginBottom: '24px' }}>
              <label style={{ display: 'block', marginBottom: '8px', color: '#333', fontWeight: '500' }}>
                Senha
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                style={{
                  width: '100%',
                  padding: '12px',
                  borderRadius: '8px',
                  border: '1px solid #ddd',
                  fontSize: '16px',
                  boxSizing: 'border-box'
                }}
                placeholder="••••••••"
              />
            </div>

            {error && (
              <div style={{ 
                color: '#d32f2f', 
                marginBottom: '16px', 
                textAlign: 'center',
                padding: '8px',
                background: '#ffebee',
                borderRadius: '4px'
              }}>
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              style={{
                width: '100%',
                padding: '14px',
                borderRadius: '8px',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                fontWeight: '600',
                fontSize: '16px',
                border: 'none',
                cursor: loading ? 'not-allowed' : 'pointer',
                opacity: loading ? 0.7 : 1
              }}
            >
              {loading ? 'Entrando...' : 'Entrar'}
            </button>
          </form>

          <div style={{ 
            marginTop: '24px', 
            textAlign: 'center', 
            color: '#666', 
            fontSize: '14px' 
          }}>
            <p>Credenciais padrão:</p>
            <p><strong>admin@admin.com</strong> / <strong>admin123</strong></p>
          </div>
        </div>
      </div>
    );
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
    if (loading) {
      return <div style={{ textAlign: 'center', padding: '40px' }}>Carregando usuários...</div>;
    }

    return (
      <div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
          <h2 style={{ color: '#333', margin: 0 }}>Gestão de Usuários</h2>
          <button 
            onClick={() => openUserModal()}
            style={{
              padding: '10px 20px',
              borderRadius: '8px',
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              border: 'none',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}
          >
            <Plus size={16} />
            Novo Usuário
          </button>
        </div>

        <div style={{
          background: 'white',
          borderRadius: '8px',
          padding: '16px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
        }}>
          {users.map(user => (
            <div key={user.id} style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              padding: '16px 0',
              borderBottom: '1px solid #eee'
            }}>
              <div>
                <div style={{ fontWeight: '500', color: '#333' }}>{user.email}</div>
                <div style={{ fontSize: '14px', color: '#666' }}>
                  Status: {user.active ? 'Ativo' : 'Inativo'}
                  {user.families && user.families.length > 0 && (
                    <span style={{ marginLeft: '10px' }}>
                      • {user.families.length} família{user.families.length !== 1 ? 's' : ''}
                    </span>
                  )}
                </div>
              </div>
              <div style={{ display: 'flex', gap: '8px' }}>
                <button 
                  onClick={() => openUserFamiliesModal(user)}
                  style={{
                    padding: '6px 12px',
                    borderRadius: '6px',
                    border: '1px solid #4CAF50',
                    background: 'white',
                    color: '#4CAF50',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px'
                  }}
                >
                  <Home size={16} />
                  Famílias
                </button>
                <button 
                  onClick={() => openUserModal(user)}
                  style={{
                    padding: '6px 12px',
                    borderRadius: '6px',
                    border: '1px solid #ddd',
                    background: 'white',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px'
                  }}
                >
                  <Edit size={16} />
                  Editar
                </button>
                <button 
                  onClick={() => handleDeleteUser(user.id)}
                  style={{
                    padding: '6px 12px',
                    borderRadius: '6px',
                    border: '1px solid #ff4444',
                    background: 'white',
                    color: '#ff4444',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px'
                  }}
                >
                  <Trash2 size={16} />
                  Excluir
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderFamilies = () => {
    if (loading) {
      return <div style={{ textAlign: 'center', padding: '40px' }}>Carregando famílias...</div>;
    }

    return (
      <div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
          <h2 style={{ color: '#333', margin: 0 }}>Gestão de Famílias</h2>
          <button 
            onClick={() => openFamilyModal()}
            style={{
              padding: '10px 20px',
              borderRadius: '8px',
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              border: 'none',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}
          >
            <Plus size={16} />
            Nova Família
          </button>
        </div>

        <div style={{
          background: 'white',
          borderRadius: '8px',
          padding: '16px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
        }}>
          {families.map(family => (
            <div key={family.id} style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              padding: '16px 0',
              borderBottom: '1px solid #eee'
            }}>
              <div>
                <div style={{ fontWeight: '500', color: '#333' }}>{family.name}</div>
                <div style={{ fontSize: '14px', color: '#666' }}>
                  {family.user_count || 0} usuário{(family.user_count || 0) !== 1 ? 's' : ''}
                </div>
              </div>
              <div style={{ display: 'flex', gap: '8px' }}>
                <button 
                  onClick={() => openFamilyModal(family)}
                  style={{
                    padding: '6px 12px',
                    borderRadius: '6px',
                    border: '1px solid #ddd',
                    background: 'white',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px'
                  }}
                >
                  <Edit size={16} />
                  Editar
                </button>
                <button 
                  onClick={() => handleDeleteFamily(family.id)}
                  style={{
                    padding: '6px 12px',
                    borderRadius: '6px',
                    border: '1px solid #ff4444',
                    background: 'white',
                    color: '#ff4444',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px'
                  }}
                >
                  <Trash2 size={16} />
                  Excluir
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderPermissions = () => {
    if (loading) {
      return <div style={{ textAlign: 'center', padding: '40px' }}>Carregando permissões...</div>;
    }

    return (
      <div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
          <h2 style={{ color: '#333', margin: 0 }}>Gestão de Permissões</h2>
          <button 
            onClick={() => openPermissionModal()}
            style={{
              padding: '10px 20px',
              borderRadius: '8px',
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              border: 'none',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}
          >
            <Plus size={16} />
            Nova Permissão
          </button>
        </div>

        <div style={{
          background: 'white',
          borderRadius: '8px',
          padding: '16px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
        }}>
          {permissions.map(permission => (
            <div key={permission.id} style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              padding: '16px 0',
              borderBottom: '1px solid #eee'
            }}>
              <div>
                <div style={{ fontWeight: '500', color: '#333' }}>{permission.name}</div>
                <div style={{ fontSize: '14px', color: '#666' }}>
                  {permission.description || 'Sem descrição'}
                </div>
              </div>
              <div style={{ display: 'flex', gap: '8px' }}>
                <button 
                  onClick={() => openPermissionModal(permission)}
                  style={{
                    padding: '6px 12px',
                    borderRadius: '6px',
                    border: '1px solid #ddd',
                    background: 'white',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px'
                  }}
                >
                  <Edit size={16} />
                  Editar
                </button>
                <button 
                  onClick={() => handleDeletePermission(permission.id)}
                  style={{
                    padding: '6px 12px',
                    borderRadius: '6px',
                    border: '1px solid #ff4444',
                    background: 'white',
                    color: '#ff4444',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px'
                  }}
                >
                  <Trash2 size={16} />
                  Excluir
                </button>
              </div>
            </div>
          ))}
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

  if (!isAuthenticated) {
    return renderLogin();
  }

  return (
    <div style={{ minHeight: '100vh', background: '#f5f7fa' }}>
      {/* Header */}
      <header style={{
        background: 'white',
        padding: '16px 24px',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <Shield size={32} style={{ color: '#667eea' }} />
          <div>
            <h1 style={{ margin: 0, color: '#333', fontSize: '20px' }}>Painel Administrativo</h1>
            <p style={{ margin: 0, color: '#666', fontSize: '14px' }}>Family Office Digital</p>
          </div>
        </div>
        <button
          onClick={handleLogout}
          style={{
            padding: '8px 16px',
            borderRadius: '6px',
            border: '1px solid #ddd',
            background: 'white',
            color: '#666',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}
        >
          <LogOut size={16} />
          Sair
        </button>
      </header>

      <div style={{ display: 'flex', minHeight: 'calc(100vh - 80px)' }}>
        {/* Sidebar */}
        <aside style={{
          width: '250px',
          background: 'white',
          borderRight: '1px solid #eee',
          padding: '24px 0'
        }}>
          <nav>
            <button
              onClick={() => setActiveTab('dashboard')}
              style={{
                width: '100%',
                padding: '12px 24px',
                border: 'none',
                background: activeTab === 'dashboard' ? '#667eea' : 'transparent',
                color: activeTab === 'dashboard' ? 'white' : '#333',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                textAlign: 'left',
                fontSize: '14px'
              }}
            >
              <BarChart3 size={20} />
              Dashboard
            </button>

            <button
              onClick={() => setActiveTab('users')}
              style={{
                width: '100%',
                padding: '12px 24px',
                border: 'none',
                background: activeTab === 'users' ? '#667eea' : 'transparent',
                color: activeTab === 'users' ? 'white' : '#333',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                textAlign: 'left',
                fontSize: '14px'
              }}
            >
              <Users size={20} />
              Usuários
            </button>

            <button
              onClick={() => setActiveTab('families')}
              style={{
                width: '100%',
                padding: '12px 24px',
                border: 'none',
                background: activeTab === 'families' ? '#667eea' : 'transparent',
                color: activeTab === 'families' ? 'white' : '#333',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                textAlign: 'left',
                fontSize: '14px'
              }}
            >
              <Home size={20} />
              Famílias
            </button>

            <button
              onClick={() => setActiveTab('permissions')}
              style={{
                width: '100%',
                padding: '12px 24px',
                border: 'none',
                background: activeTab === 'permissions' ? '#667eea' : 'transparent',
                color: activeTab === 'permissions' ? 'white' : '#333',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                textAlign: 'left',
                fontSize: '14px'
              }}
            >
              <Shield size={20} />
              Permissões
            </button>
          </nav>
        </aside>

        {/* Main Content */}
        <main style={{ flex: 1, padding: '32px' }}>
          {renderContent()}
        </main>
      </div>

      {/* Modais */}
      <Modal
        isOpen={showUserModal}
        onClose={() => setShowUserModal(false)}
        title={editingUser ? 'Editar Usuário' : 'Novo Usuário'}
      >
        <form onSubmit={handleUserSubmit}>
          <div style={{ marginBottom: '16px' }}>
            <label style={{ display: 'block', marginBottom: '8px', color: '#333', fontWeight: '500' }}>
              E-mail
            </label>
            <input
              type="email"
              value={userForm.email}
              onChange={(e) => setUserForm({ ...userForm, email: e.target.value })}
              required
              style={{
                width: '100%',
                padding: '12px',
                borderRadius: '8px',
                border: '1px solid #ddd',
                fontSize: '16px',
                boxSizing: 'border-box'
              }}
            />
          </div>

          <div style={{ marginBottom: '16px' }}>
            <label style={{ display: 'block', marginBottom: '8px', color: '#333', fontWeight: '500' }}>
              Senha {editingUser && '(deixe em branco para manter)'}
            </label>
            <input
              type="password"
              value={userForm.password}
              onChange={(e) => setUserForm({ ...userForm, password: e.target.value })}
              required={!editingUser}
              style={{
                width: '100%',
                padding: '12px',
                borderRadius: '8px',
                border: '1px solid #ddd',
                fontSize: '16px',
                boxSizing: 'border-box'
              }}
            />
          </div>

          <div style={{ marginBottom: '24px' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
              <input
                type="checkbox"
                checked={userForm.active}
                onChange={(e) => setUserForm({ ...userForm, active: e.target.checked })}
                style={{ width: '16px', height: '16px' }}
              />
              <span style={{ color: '#333' }}>Usuário ativo</span>
            </label>
          </div>

          <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end' }}>
            <button
              type="button"
              onClick={() => setShowUserModal(false)}
              style={{
                padding: '10px 20px',
                borderRadius: '6px',
                border: '1px solid #ddd',
                background: 'white',
                color: '#666',
                cursor: 'pointer'
              }}
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={loading}
              style={{
                padding: '10px 20px',
                borderRadius: '6px',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                border: 'none',
                cursor: loading ? 'not-allowed' : 'pointer',
                opacity: loading ? 0.7 : 1
              }}
            >
              {loading ? 'Salvando...' : (editingUser ? 'Atualizar' : 'Criar')}
            </button>
          </div>
        </form>
      </Modal>

      <Modal
        isOpen={showFamilyModal}
        onClose={() => setShowFamilyModal(false)}
        title={editingFamily ? 'Editar Família' : 'Nova Família'}
      >
        <form onSubmit={handleFamilySubmit}>
          <div style={{ marginBottom: '24px' }}>
            <label style={{ display: 'block', marginBottom: '8px', color: '#333', fontWeight: '500' }}>
              Nome da Família
            </label>
            <input
              type="text"
              value={familyForm.name}
              onChange={(e) => setFamilyForm({ name: e.target.value })}
              required
              style={{
                width: '100%',
                padding: '12px',
                borderRadius: '8px',
                border: '1px solid #ddd',
                fontSize: '16px',
                boxSizing: 'border-box'
              }}
            />
          </div>

          <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end' }}>
            <button
              type="button"
              onClick={() => setShowFamilyModal(false)}
              style={{
                padding: '10px 20px',
                borderRadius: '6px',
                border: '1px solid #ddd',
                background: 'white',
                color: '#666',
                cursor: 'pointer'
              }}
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={loading}
              style={{
                padding: '10px 20px',
                borderRadius: '6px',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                border: 'none',
                cursor: loading ? 'not-allowed' : 'pointer',
                opacity: loading ? 0.7 : 1
              }}
            >
              {loading ? 'Salvando...' : (editingFamily ? 'Atualizar' : 'Criar')}
            </button>
          </div>
        </form>
      </Modal>

      <Modal
        isOpen={showPermissionModal}
        onClose={() => setShowPermissionModal(false)}
        title={editingPermission ? 'Editar Permissão' : 'Nova Permissão'}
      >
        <form onSubmit={handlePermissionSubmit}>
          <div style={{ marginBottom: '16px' }}>
            <label style={{ display: 'block', marginBottom: '8px', color: '#333', fontWeight: '500' }}>
              Nome da Permissão
            </label>
            <input
              type="text"
              value={permissionForm.name}
              onChange={(e) => setPermissionForm({ ...permissionForm, name: e.target.value })}
              required
              style={{
                width: '100%',
                padding: '12px',
                borderRadius: '8px',
                border: '1px solid #ddd',
                fontSize: '16px',
                boxSizing: 'border-box'
              }}
            />
          </div>

          <div style={{ marginBottom: '24px' }}>
            <label style={{ display: 'block', marginBottom: '8px', color: '#333', fontWeight: '500' }}>
              Descrição
            </label>
            <textarea
              value={permissionForm.description}
              onChange={(e) => setPermissionForm({ ...permissionForm, description: e.target.value })}
              rows={3}
              style={{
                width: '100%',
                padding: '12px',
                borderRadius: '8px',
                border: '1px solid #ddd',
                fontSize: '16px',
                boxSizing: 'border-box',
                resize: 'vertical'
              }}
            />
          </div>

          <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end' }}>
            <button
              type="button"
              onClick={() => setShowPermissionModal(false)}
              style={{
                padding: '10px 20px',
                borderRadius: '6px',
                border: '1px solid #ddd',
                background: 'white',
                color: '#666',
                cursor: 'pointer'
              }}
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={loading}
              style={{
                padding: '10px 20px',
                borderRadius: '6px',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                border: 'none',
                cursor: loading ? 'not-allowed' : 'pointer',
                opacity: loading ? 0.7 : 1
              }}
            >
              {loading ? 'Salvando...' : (editingPermission ? 'Atualizar' : 'Criar')}
            </button>
          </div>
        </form>
      </Modal>

      <Modal
        isOpen={showUserFamiliesModal}
        onClose={() => setShowUserFamiliesModal(false)}
        title={selectedUserForFamilies ? `Famílias de ${selectedUserForFamilies.email}` : 'Gerenciar Famílias'}
      >
        {selectedUserForFamilies && (
          <div>
            {/* Famílias Associadas */}
            <div style={{ marginBottom: '24px' }}>
              <h3 style={{ marginBottom: '12px', color: '#333', fontSize: '16px' }}>Famílias Associadas</h3>
              {selectedUserForFamilies.families && selectedUserForFamilies.families.length > 0 ? (
                <div style={{ 
                  border: '1px solid #eee', 
                  borderRadius: '8px', 
                  maxHeight: '200px', 
                  overflowY: 'auto' 
                }}>
                  {selectedUserForFamilies.families.map(family => (
                    <div key={family.id} style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      padding: '12px 16px',
                      borderBottom: '1px solid #eee'
                    }}>
                      <span style={{ fontWeight: '500' }}>{family.name}</span>
                      <button
                        onClick={() => handleRemoveUserFromFamily(family.id)}
                        style={{
                          padding: '4px 8px',
                          borderRadius: '4px',
                          border: '1px solid #ff4444',
                          background: 'white',
                          color: '#ff4444',
                          cursor: 'pointer',
                          fontSize: '12px'
                        }}
                      >
                        Remover
                      </button>
                    </div>
                  ))}
                </div>
              ) : (
                <div style={{ 
                  padding: '16px', 
                  textAlign: 'center', 
                  color: '#666',
                  fontStyle: 'italic',
                  border: '1px solid #eee',
                  borderRadius: '8px'
                }}>
                  Usuário não está associado a nenhuma família
                </div>
              )}
            </div>

            {/* Adicionar a Nova Família */}
            <div>
              <h3 style={{ marginBottom: '12px', color: '#333', fontSize: '16px' }}>Adicionar à Família</h3>
              <div style={{ 
                border: '1px solid #eee', 
                borderRadius: '8px', 
                maxHeight: '200px', 
                overflowY: 'auto' 
              }}>
                {families
                  .filter(family => !selectedUserForFamilies.families?.some(uf => uf.id === family.id))
                  .map(family => (
                    <div key={family.id} style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      padding: '12px 16px',
                      borderBottom: '1px solid #eee'
                    }}>
                      <span style={{ fontWeight: '500' }}>{family.name}</span>
                      <button
                        onClick={() => handleAddUserToFamily(family.id)}
                        disabled={loading}
                        style={{
                          padding: '4px 8px',
                          borderRadius: '4px',
                          border: '1px solid #4CAF50',
                          background: 'white',
                          color: '#4CAF50',
                          cursor: loading ? 'not-allowed' : 'pointer',
                          fontSize: '12px',
                          opacity: loading ? 0.6 : 1
                        }}
                      >
                        Adicionar
                      </button>
                    </div>
                  ))}
                {families.filter(family => !selectedUserForFamilies.families?.some(uf => uf.id === family.id)).length === 0 && (
                  <div style={{ 
                    padding: '16px', 
                    textAlign: 'center', 
                    color: '#666',
                    fontStyle: 'italic'
                  }}>
                    Todas as famílias já estão associadas a este usuário
                  </div>
                )}
              </div>
            </div>

            {error && (
              <div style={{ 
                marginTop: '16px',
                padding: '8px 12px',
                background: '#ffebee',
                border: '1px solid #ff4444',
                borderRadius: '4px',
                color: '#d32f2f',
                fontSize: '14px'
              }}>
                {error}
              </div>
            )}

            <div style={{ marginTop: '24px', textAlign: 'right' }}>
              <button
                onClick={() => setShowUserFamiliesModal(false)}
                style={{
                  padding: '10px 20px',
                  borderRadius: '6px',
                  border: '1px solid #ddd',
                  background: 'white',
                  color: '#666',
                  cursor: 'pointer'
                }}
              >
                Fechar
              </button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
} 