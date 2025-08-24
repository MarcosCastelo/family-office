import React, { useState } from 'react';
import { 
  Menu, 
  X, 
  User, 
  Settings, 
  LogOut, 
  ChevronDown,
  Bell,
  Search,
  Shield
} from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import { useFamily } from '../contexts/FamilyContext';
import FamilySelect from './FamilySelect';
import NotificationCenter, { useNotifications } from './NotificationCenter';
import type { Notification } from '../types/notification';

export default function Header() {
  const { user, logout } = useAuth();
  const { selectedFamilyId } = useFamily();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);
  const { notifications, markAsRead, markAllAsRead, deleteNotification } = useNotifications();

  const handleLogout = () => {
    logout();
    setIsUserMenuOpen(false);
  };

  const handleMenuToggle = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const handleUserMenuToggle = () => {
    setIsUserMenuOpen(!isUserMenuOpen);
  };

  // Simular algumas notificações para demonstração
  React.useEffect(() => {
    if (notifications.length === 0) {
      // Adicionar notificações de exemplo
      const exampleNotifications: Omit<Notification, 'id' | 'timestamp' | 'read'>[] = [
        {
          type: 'info',
          title: 'Atualização de Cotações',
          message: 'As cotações dos ativos foram atualizadas com sucesso',
          read: false
        },
        {
          type: 'warning',
          title: 'Alerta de Concentração',
          message: 'O ativo PETR4 representa mais de 30% da carteira',
          read: false,
          action: {
            label: 'Ver Detalhes',
            onClick: () => console.log('Ver detalhes do alerta')
          }
        },
        {
          type: 'success',
          title: 'Relatório Gerado',
          message: 'O relatório de carteira foi gerado com sucesso',
          read: true
        }
      ];

      exampleNotifications.forEach(notification => {
        // Simular adição de notificações
        setTimeout(() => {
          // Esta função seria chamada pelo sistema real
        }, 1000);
      });
    }
  }, [notifications.length]);

  return (
    <header style={{
      background: 'white',
      borderBottom: '1px solid #e2e8f0',
      padding: '0 24px',
      position: 'sticky',
      top: 0,
      zIndex: 100,
      boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)'
    }}>
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        height: '64px'
      }}>
        {/* Left side - Logo and Menu */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '24px' }}>
          {/* Mobile menu button */}
          <button
            onClick={handleMenuToggle}
            style={{
              background: 'none',
              border: 'none',
              padding: '8px',
              borderRadius: '8px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#666'
            }}
            aria-label="Toggle menu"
          >
            {isMenuOpen ? <X size={20} /> : <Menu size={20} />}
          </button>

          {/* Logo */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            fontSize: '20px',
            fontWeight: '700',
            color: '#222'
          }}>
            <div style={{
              width: '32px',
              height: '32px',
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              borderRadius: '8px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white',
              fontSize: '16px',
              fontWeight: '700'
            }}>
              FO
            </div>
            <span style={{ display: { xs: 'none', sm: 'block' } }}>
              Family Office
            </span>
          </div>
        </div>

        {/* Center - Family Selector */}
        <div style={{ flex: 1, display: 'flex', justifyContent: 'center', maxWidth: '400px' }}>
          <FamilySelect />
        </div>

        {/* Right side - Search, Notifications, User */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          {/* Search */}
          <div style={{
            position: 'relative',
            display: { xs: 'none', md: 'block' }
          }}>
            <input
              type="text"
              placeholder="Buscar ativos, transações..."
              style={{
                width: '240px',
                padding: '8px 12px 8px 36px',
                border: '1px solid #e2e8f0',
                borderRadius: '8px',
                fontSize: '14px',
                background: '#f8fafc',
                outline: 'none',
                transition: 'all 0.2s'
              }}
              onFocus={(e) => {
                e.target.style.background = 'white';
                e.target.style.borderColor = '#3b82f6';
              }}
              onBlur={(e) => {
                e.target.style.background = '#f8fafc';
                e.target.style.borderColor = '#e2e8f0';
              }}
            />
            <Search 
              size={16} 
              style={{
                position: 'absolute',
                left: '12px',
                top: '50%',
                transform: 'translateY(-50%)',
                color: '#666'
              }}
            />
          </div>

          {/* Notifications */}
          <NotificationCenter
            notifications={notifications}
            onMarkAsRead={markAsRead}
            onMarkAllAsRead={markAllAsRead}
            onDelete={deleteNotification}
            maxNotifications={5}
            showUnreadCount={true}
          />

          {/* User Menu */}
          <div style={{ position: 'relative' }}>
            <button
              onClick={handleUserMenuToggle}
              style={{
                background: 'none',
                border: 'none',
                padding: '8px 12px',
                borderRadius: '8px',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                color: '#666',
                transition: 'all 0.2s'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = '#f8fafc';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = 'none';
              }}
            >
              <div style={{
                width: '32px',
                height: '32px',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'white',
                fontSize: '14px',
                fontWeight: '600'
              }}>
                {user?.name?.charAt(0)?.toUpperCase() || 'U'}
              </div>
              <span style={{ 
                fontSize: '14px', 
                fontWeight: '500',
                display: { xs: 'none', sm: 'block' }
              }}>
                {user?.name || 'Usuário'}
              </span>
              <ChevronDown size={16} />
            </button>

            {/* User Dropdown Menu */}
            {isUserMenuOpen && (
              <div style={{
                position: 'absolute',
                top: '100%',
                right: 0,
                width: '200px',
                background: 'white',
                borderRadius: '12px',
                boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
                border: '1px solid #e2e8f0',
                zIndex: 1000,
                overflow: 'hidden',
                marginTop: '8px'
              }}>
                {/* User Info */}
                <div style={{
                  padding: '16px 20px',
                  borderBottom: '1px solid #f1f5f9',
                  background: '#f8fafc'
                }}>
                  <div style={{
                    fontSize: '14px',
                    fontWeight: '600',
                    color: '#222',
                    marginBottom: '4px'
                  }}>
                    {user?.name || 'Usuário'}
                  </div>
                  <div style={{
                    fontSize: '12px',
                    color: '#666'
                  }}>
                    {user?.email || 'usuario@email.com'}
                  </div>
                </div>

                {/* Menu Items */}
                <div style={{ padding: '8px 0' }}>
                  <button
                    onClick={() => {
                      // Navegar para perfil
                      setIsUserMenuOpen(false);
                    }}
                    style={{
                      width: '100%',
                      background: 'none',
                      border: 'none',
                      padding: '12px 20px',
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '12px',
                      color: '#666',
                      fontSize: '14px',
                      transition: 'background 0.2s'
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.background = '#f8fafc';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.background = 'none';
                    }}
                  >
                    <User size={16} />
                    Meu Perfil
                  </button>

                  <button
                    onClick={() => {
                      // Navegar para configurações
                      setIsUserMenuOpen(false);
                    }}
                    style={{
                      width: '100%',
                      background: 'none',
                      border: 'none',
                      padding: '12px 20px',
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '12px',
                      color: '#666',
                      fontSize: '14px',
                      transition: 'background 0.2s'
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.background = '#f8fafc';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.background = 'none';
                    }}
                  >
                    <Settings size={16} />
                    Configurações
                  </button>

                  {/* Admin Panel Link - Only for admin users */}
                  {user && user.permissions && (
                    user.permissions.includes('admin') || 
                    user.permissions.includes('admin_system') || 
                    user.permissions.includes('admin_users')
                  ) && (
                    <button
                      onClick={() => {
                        // Navegar para o painel administrativo
                        setIsUserMenuOpen(false);
                        window.location.href = '/admin';
                      }}
                      style={{
                        width: '100%',
                        background: 'none',
                        border: 'none',
                        padding: '12px 20px',
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '12px',
                        color: '#8b5cf6',
                        fontSize: '14px',
                        transition: 'background 0.2s'
                      }}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.background = '#f3f4f6';
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.background = 'none';
                      }}
                    >
                      <Shield size={16} />
                      Painel Admin
                    </button>
                  )}

                  <div style={{
                    height: '1px',
                    background: '#f1f5f9',
                    margin: '8px 0'
                  }} />

                  <button
                    onClick={handleLogout}
                    style={{
                      width: '100%',
                      background: 'none',
                      border: 'none',
                      padding: '12px 20px',
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '12px',
                      color: '#ef4444',
                      fontSize: '14px',
                      transition: 'background 0.2s'
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.background = '#fef2f2';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.background = 'none';
                    }}
                  >
                    <LogOut size={16} />
                    Sair
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Mobile Menu Overlay */}
      {isMenuOpen && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0, 0, 0, 0.5)',
          zIndex: 200,
          display: { xs: 'block', md: 'none' }
        }} onClick={handleMenuToggle}>
          <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '280px',
            height: '100%',
            background: 'white',
            padding: '24px',
            overflowY: 'auto'
          }} onClick={(e) => e.stopPropagation()}>
            {/* Mobile Menu Content */}
            <div style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              marginBottom: '32px'
            }}>
              <h2 style={{
                margin: 0,
                fontSize: '20px',
                fontWeight: '700',
                color: '#222'
              }}>
                Menu
              </h2>
              <button
                onClick={handleMenuToggle}
                style={{
                  background: 'none',
                  border: 'none',
                  padding: '8px',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  color: '#666'
                }}
              >
                <X size={20} />
              </button>
            </div>

            {/* Mobile Navigation Items */}
            <nav style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              <a href="/dashboard" style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                padding: '12px 16px',
                borderRadius: '8px',
                color: '#666',
                textDecoration: 'none',
                fontSize: '16px',
                fontWeight: '500',
                transition: 'background 0.2s'
              }}>
                Dashboard
              </a>
              <a href="/assets" style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                padding: '12px 16px',
                borderRadius: '8px',
                color: '#666',
                textDecoration: 'none',
                fontSize: '16px',
                fontWeight: '500',
                transition: 'background 0.2s'
              }}>
                Ativos
              </a>
              <a href="/transactions" style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                padding: '12px 16px',
                borderRadius: '8px',
                color: '#666',
                textDecoration: 'none',
                fontSize: '16px',
                fontWeight: '500',
                transition: 'background 0.2s'
              }}>
                Transações
              </a>
              <a href="/risk-analysis" style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                padding: '12px 16px',
                borderRadius: '8px',
                color: '#666',
                textDecoration: 'none',
                fontSize: '16px',
                fontWeight: '500',
                transition: 'background 0.2s'
              }}>
                Análise de Risco
              </a>
              <a href="/upload" style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                padding: '12px 16px',
                borderRadius: '8px',
                color: '#666',
                textDecoration: 'none',
                fontSize: '16px',
                fontWeight: '500',
                transition: 'background 0.2s'
              }}>
                Upload
              </a>
              <a href="/profile" style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                padding: '12px 16px',
                borderRadius: '8px',
                color: '#666',
                textDecoration: 'none',
                fontSize: '16px',
                fontWeight: '500',
                transition: 'background 0.2s'
              }}>
                Perfil
              </a>
            </nav>
          </div>
        </div>
      )}

      {/* Click outside to close user menu */}
      {isUserMenuOpen && (
        <div
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            zIndex: 999
          }}
          onClick={() => setIsUserMenuOpen(false)}
        />
      )}
    </header>
  );
} 