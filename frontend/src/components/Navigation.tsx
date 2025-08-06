import React from 'react';
import {
  LayoutDashboard,
  PieChart,
  BarChart3,
  Upload,
  User,
  TrendingUp,
  Shield,
  FileText,
  Activity
} from 'lucide-react';

interface NavigationProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
}

export default function Navigation({ activeTab, onTabChange }: NavigationProps) {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'assets', label: 'Ativos', icon: PieChart },
    { id: 'transactions', label: 'Transações', icon: Activity },
    { id: 'risk', label: 'Análise de Risco', icon: BarChart3 },
    { id: 'upload', label: 'Upload', icon: Upload },
    { id: 'profile', label: 'Perfil', icon: User }
  ];

  return (
    <nav style={{
      background: 'white',
      padding: '16px 0',
      boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
      borderBottom: '1px solid #e9ecef'
    }}>
      <div style={{
        maxWidth: 1200,
        margin: '0 auto',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        gap: 8
      }}>
        {menuItems.map((item) => {
          const IconComponent = item.icon;
          const isActive = activeTab === item.id;

          return (
            <button
              key={item.id}
              onClick={() => onTabChange(item.id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 8,
                padding: '12px 20px',
                borderRadius: 12,
                border: 'none',
                background: isActive
                  ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                  : 'transparent',
                color: isActive ? 'white' : '#666',
                cursor: 'pointer',
                fontSize: 14,
                fontWeight: isActive ? 600 : 500,
                transition: 'all 0.2s ease',
                minWidth: 120,
                justifyContent: 'center',
                position: 'relative',
                overflow: 'hidden'
              }}
              onMouseEnter={(e) => {
                if (!isActive) {
                  e.currentTarget.style.background = '#f8f9fa';
                  e.currentTarget.style.color = '#333';
                }
              }}
              onMouseLeave={(e) => {
                if (!isActive) {
                  e.currentTarget.style.background = 'transparent';
                  e.currentTarget.style.color = '#666';
                }
              }}
            >
              <IconComponent size={18} />
              <span>{item.label}</span>

              {/* Indicador ativo */}
              {isActive && (
                <div style={{
                  position: 'absolute',
                  bottom: 0,
                  left: '50%',
                  transform: 'translateX(-50%)',
                  width: 20,
                  height: 3,
                  background: 'rgba(255,255,255,0.8)',
                  borderRadius: '2px 2px 0 0'
                }} />
              )}
            </button>
          );
        })}
      </div>
    </nav>
  );
} 