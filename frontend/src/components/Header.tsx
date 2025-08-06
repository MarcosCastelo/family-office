import React, { useState, useEffect } from 'react';
import { LogOut, User, Clock, Building2 } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import FamilySelect from './FamilySelect';

interface Family {
  id: number;
  name: string;
}

interface HeaderProps {
  selectedFamilyId: number | null;
  onFamilyChange: (familyId: number) => void;
  families: Family[];
}

export default function Header({ selectedFamilyId, onFamilyChange, families }: HeaderProps) {
  const { user, logout } = useAuth();
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('pt-BR', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  const formatDate = (date: Date) => {
    return date.toLocaleDateString('pt-BR', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const handleLogout = () => {
    logout();
  };

  return (
    <header style={{
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      color: 'white',
      padding: '16px 24px',
      boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      minHeight: 80
    }}>
      {/* Logo e Nome do Sistema */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: 12,
          padding: '8px 16px',
          background: 'rgba(255,255,255,0.1)',
          borderRadius: 12,
          backdropFilter: 'blur(10px)'
        }}>
          <Building2 size={24} />
          <div>
            <div style={{ fontWeight: 600, fontSize: 18 }}>Family Office</div>
            <div style={{ fontSize: 12, opacity: 0.8 }}>Gestão Patrimonial</div>
          </div>
        </div>
      </div>

      {/* Informações do Sistema e Família */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 24 }}>
        {/* Data e Hora */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: 8,
          padding: '8px 16px',
          background: 'rgba(255,255,255,0.1)',
          borderRadius: 12,
          backdropFilter: 'blur(10px)'
        }}>
          <Clock size={16} />
          <div style={{ fontSize: 14 }}>
            <div>{formatTime(currentTime)}</div>
            <div style={{ fontSize: 12, opacity: 0.8 }}>{formatDate(currentTime)}</div>
          </div>
        </div>

        {/* Select de Família */}
        {families.length > 0 && (
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: 8,
            padding: '8px 16px',
            background: 'rgba(255,255,255,0.1)',
            borderRadius: 12,
            backdropFilter: 'blur(10px)'
          }}>
            <label style={{ 
              color: 'white', 
              fontSize: 14, 
              fontWeight: 500,
              whiteSpace: 'nowrap'
            }}>
              Família:
            </label>
            <div style={{ minWidth: 200 }}>
              <FamilySelect
                families={families}
                selectedFamilyId={selectedFamilyId}
                onFamilyChange={onFamilyChange}
                placeholder="Selecione uma família"
              />
            </div>
          </div>
        )}

        {/* Informações do Usuário */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: 8,
          padding: '8px 16px',
          background: 'rgba(255,255,255,0.1)',
          borderRadius: 12,
          backdropFilter: 'blur(10px)'
        }}>
          <User size={16} />
          <div style={{ fontSize: 14 }}>
            <div style={{ fontWeight: 500 }}>{user?.email}</div>
            <div style={{ fontSize: 12, opacity: 0.8 }}>Usuário</div>
          </div>
        </div>

        {/* Botão de Logout */}
        <button
          onClick={handleLogout}
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            width: 40,
            height: 40,
            borderRadius: '50%',
            border: 'none',
            background: 'rgba(255,255,255,0.1)',
            color: 'white',
            cursor: 'pointer',
            transition: 'all 0.2s ease',
            backdropFilter: 'blur(10px)'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = 'rgba(255,255,255,0.2)';
            e.currentTarget.style.transform = 'scale(1.05)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = 'rgba(255,255,255,0.1)';
            e.currentTarget.style.transform = 'scale(1)';
          }}
          title="Sair"
        >
          <LogOut size={18} />
        </button>
      </div>
    </header>
  );
} 