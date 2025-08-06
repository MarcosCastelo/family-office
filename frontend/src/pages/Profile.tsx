import React, { useState, useEffect } from 'react';
import { getCurrentUser, updatePassword } from '../services/profile';
import type { UserProfile } from '../services/profile';
import { useAuth } from '../hooks/useAuth';

export default function Profile() {
  const { user: authUser } = useAuth();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showPasswordForm, setShowPasswordForm] = useState(false);
  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });
  const [updatingPassword, setUpdatingPassword] = useState(false);

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      setLoading(true);
      setError(null);
      const profileData = await getCurrentUser();
      setProfile(profileData);
    } catch (err: any) {
      console.error('Erro ao carregar perfil:', err);
      setError(err.response?.data?.error || 'Erro ao carregar perfil');
    } finally {
      setLoading(false);
    }
  };

  const handlePasswordChange = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (passwordData.newPassword !== passwordData.confirmPassword) {
      alert('As senhas não coincidem');
      return;
    }
    
    if (passwordData.newPassword.length < 6) {
      alert('A nova senha deve ter pelo menos 6 caracteres');
      return;
    }
    
    try {
      setUpdatingPassword(true);
      await updatePassword(passwordData.currentPassword, passwordData.newPassword);
      alert('Senha alterada com sucesso!');
      setShowPasswordForm(false);
      setPasswordData({
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      });
    } catch (err: any) {
      console.error('Erro ao alterar senha:', err);
      alert(err.response?.data?.error || 'Erro ao alterar senha');
    } finally {
      setUpdatingPassword(false);
    }
  };

  const getPermissionLabel = (permission: string) => {
    const labels: { [key: string]: string } = {
      'user_view': 'Visualizar Usuários',
      'user_create': 'Criar Usuários',
      'user_update': 'Editar Usuários',
      'user_delete': 'Excluir Usuários',
      'family_view': 'Visualizar Famílias',
      'family_create': 'Criar Famílias',
      'family_update': 'Editar Famílias',
      'family_delete': 'Excluir Famílias',
      'family_manage_members': 'Gerenciar Membros da Família',
      'asset_view': 'Visualizar Ativos',
      'asset_create': 'Criar Ativos',
      'asset_update': 'Editar Ativos',
      'asset_delete': 'Excluir Ativos',
      'asset_import': 'Importar Ativos',
      'report_view': 'Visualizar Relatórios',
      'report_generate': 'Gerar Relatórios',
      'report_export': 'Exportar Relatórios',
      'admin_users': 'Administrar Usuários',
      'admin_permissions': 'Administrar Permissões',
      'admin_system': 'Administrar Sistema',
      'admin': 'Administrador'
    };
    
    return labels[permission] || permission;
  };

  if (loading) {
    return (
      <div style={{ padding: 24, textAlign: 'center', color: '#666' }}>
        Carregando perfil...
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

  return (
    <div style={{ padding: 24, maxWidth: 800, margin: '0 auto' }}>
      <h1 style={{ color: '#222', marginBottom: 24 }}>Meu Perfil</h1>
      
      {profile && (
        <div style={{ display: 'grid', gap: 24 }}>
          {/* Informações Básicas */}
          <div style={{
            background: '#fff',
            borderRadius: 16,
            padding: 24,
            boxShadow: '0 4px 24px rgba(0,0,0,0.08)'
          }}>
            <h2 style={{ color: '#222', marginBottom: 20 }}>Informações Pessoais</h2>
            
            <div style={{ display: 'grid', gap: 16 }}>
              <div>
                <label style={{ display: 'block', marginBottom: 4, color: '#666', fontSize: 14 }}>
                  E-mail
                </label>
                <div style={{
                  padding: '12px 16px',
                  background: '#f5f5f5',
                  borderRadius: 8,
                  color: '#222',
                  fontSize: 16
                }}>
                  {profile.email}
                </div>
              </div>
              
              <div>
                <label style={{ display: 'block', marginBottom: 4, color: '#666', fontSize: 14 }}>
                  Status
                </label>
                <div style={{
                  padding: '6px 12px',
                  borderRadius: 6,
                  fontSize: 14,
                  fontWeight: 500,
                  color: profile.active ? '#388e3c' : '#d32f2f',
                  background: profile.active ? '#e8f5e8' : '#ffebee',
                  display: 'inline-block'
                }}>
                  {profile.active ? 'Ativo' : 'Inativo'}
                </div>
              </div>
            </div>
          </div>

          {/* Famílias */}
          <div style={{
            background: '#fff',
            borderRadius: 16,
            padding: 24,
            boxShadow: '0 4px 24px rgba(0,0,0,0.08)'
          }}>
            <h2 style={{ color: '#222', marginBottom: 20 }}>Famílias</h2>
            
            {profile.families.length > 0 ? (
              <div style={{ display: 'grid', gap: 12 }}>
                {profile.families.map((family) => (
                  <div key={family.id} style={{
                    padding: '12px 16px',
                    background: '#f8f9fa',
                    borderRadius: 8,
                    border: '1px solid #e9ecef'
                  }}>
                    <div style={{ color: '#222', fontWeight: 500 }}>
                      {family.name}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div style={{ textAlign: 'center', padding: '24px 0', color: '#666' }}>
                Você não está associado a nenhuma família
              </div>
            )}
          </div>

          {/* Permissões */}
          <div style={{
            background: '#fff',
            borderRadius: 16,
            padding: 24,
            boxShadow: '0 4px 24px rgba(0,0,0,0.08)'
          }}>
            <h2 style={{ color: '#222', marginBottom: 20 }}>Permissões</h2>
            
            {profile.permissions.length > 0 ? (
              <div style={{ display: 'grid', gap: 8 }}>
                {profile.permissions.map((permission) => (
                  <div key={permission.id} style={{
                    padding: '8px 12px',
                    background: '#e3f2fd',
                    borderRadius: 6,
                    fontSize: 14,
                    color: '#1976d2',
                    border: '1px solid #bbdefb'
                  }}>
                    {getPermissionLabel(permission.name)}
                  </div>
                ))}
              </div>
            ) : (
              <div style={{ textAlign: 'center', padding: '24px 0', color: '#666' }}>
                Nenhuma permissão atribuída
              </div>
            )}
          </div>

          {/* Alterar Senha */}
          <div style={{
            background: '#fff',
            borderRadius: 16,
            padding: 24,
            boxShadow: '0 4px 24px rgba(0,0,0,0.08)'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
              <h2 style={{ color: '#222', margin: 0 }}>Alterar Senha</h2>
              <button
                onClick={() => setShowPasswordForm(!showPasswordForm)}
                style={{
                  padding: '8px 16px',
                  borderRadius: 8,
                  border: '1px solid #7b6cf6',
                  background: 'transparent',
                  color: '#7b6cf6',
                  cursor: 'pointer',
                  fontSize: 14,
                  fontWeight: 500
                }}
              >
                {showPasswordForm ? 'Cancelar' : 'Alterar Senha'}
              </button>
            </div>
            
            {showPasswordForm && (
              <form onSubmit={handlePasswordChange} style={{ display: 'grid', gap: 16 }}>
                <div>
                  <label style={{ display: 'block', marginBottom: 4, color: '#222' }}>
                    Senha Atual
                  </label>
                  <input
                    type="password"
                    value={passwordData.currentPassword}
                    onChange={(e) => setPasswordData({...passwordData, currentPassword: e.target.value})}
                    required
                    style={{
                      width: '100%',
                      padding: 10,
                      borderRadius: 8,
                      border: '1px solid #ccc',
                      fontSize: 16
                    }}
                  />
                </div>
                
                <div>
                  <label style={{ display: 'block', marginBottom: 4, color: '#222' }}>
                    Nova Senha
                  </label>
                  <input
                    type="password"
                    value={passwordData.newPassword}
                    onChange={(e) => setPasswordData({...passwordData, newPassword: e.target.value})}
                    required
                    minLength={6}
                    style={{
                      width: '100%',
                      padding: 10,
                      borderRadius: 8,
                      border: '1px solid #ccc',
                      fontSize: 16
                    }}
                  />
                  <small style={{ color: '#666', fontSize: 12 }}>
                    Mínimo 6 caracteres
                  </small>
                </div>
                
                <div>
                  <label style={{ display: 'block', marginBottom: 4, color: '#222' }}>
                    Confirmar Nova Senha
                  </label>
                  <input
                    type="password"
                    value={passwordData.confirmPassword}
                    onChange={(e) => setPasswordData({...passwordData, confirmPassword: e.target.value})}
                    required
                    style={{
                      width: '100%',
                      padding: 10,
                      borderRadius: 8,
                      border: '1px solid #ccc',
                      fontSize: 16
                    }}
                  />
                </div>
                
                <button
                  type="submit"
                  disabled={updatingPassword}
                  style={{
                    padding: '12px 24px',
                    borderRadius: 8,
                    background: updatingPassword ? '#ccc' : 'linear-gradient(90deg, #7b6cf6 0%, #5f9df7 100%)',
                    color: '#fff',
                    border: 'none',
                    cursor: updatingPassword ? 'not-allowed' : 'pointer',
                    fontSize: 14,
                    fontWeight: 500
                  }}
                >
                  {updatingPassword ? 'Alterando...' : 'Alterar Senha'}
                </button>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  );
} 