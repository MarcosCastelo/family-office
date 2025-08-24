import React, { useState, useRef, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { ChevronDown, Users, Check } from 'lucide-react';
import { useFamily } from '../contexts/FamilyContext';

interface Family {
  id: number;
  name: string;
}

export default function FamilySelect() {
  const { families, selectedFamilyId, setSelectedFamilyId, loading, error } = useFamily();
  const [isOpen, setIsOpen] = useState(false);
  const [buttonRect, setButtonRect] = useState<DOMRect | null>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);

  const selectedFamily = families.find(f => f.id === selectedFamilyId);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node) &&
          buttonRef.current && !buttonRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    const handleScroll = () => {
      if (isOpen && buttonRef.current) {
        setButtonRect(buttonRef.current.getBoundingClientRect());
      }
    };

    const handleResize = () => {
      if (isOpen) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    window.addEventListener('scroll', handleScroll, true);
    window.addEventListener('resize', handleResize);
    
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      window.removeEventListener('scroll', handleScroll, true);
      window.removeEventListener('resize', handleResize);
    };
  }, [isOpen]);

  const handleButtonClick = () => {
    if (!loading && families.length > 0) {
      if (!isOpen && buttonRef.current) {
        setButtonRect(buttonRef.current.getBoundingClientRect());
      }
      setIsOpen(!isOpen);
    }
  };

  const handleSelect = (familyId: number) => {
    setSelectedFamilyId(familyId);
    setIsOpen(false);
  };

  // Estilos para o header
  const buttonStyles = {
    width: '100%',
    padding: '8px 12px',
    borderRadius: 8,
    border: '1px solid #e2e8f0',
    background: loading ? '#f1f5f9' : 'white',
    color: loading ? '#666' : '#222',
    cursor: loading ? 'not-allowed' : 'pointer',
    fontSize: 14,
    fontWeight: 500,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    transition: 'all 0.2s ease',
    minHeight: 40,
    boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)'
  };

  const dropdownStyles = {
    position: 'absolute' as const,
    top: buttonRect ? buttonRect.bottom + 8 : 'auto',
    left: buttonRect ? buttonRect.left : 'auto',
    width: buttonRect ? buttonRect.width : 'auto',
    background: 'white',
    borderRadius: 8,
    border: '1px solid #e2e8f0',
    boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
    zIndex: 1000,
    maxHeight: 300,
    overflowY: 'auto' as const
  };

  if (loading) {
    return (
      <div style={buttonStyles}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <Users size={16} />
          <span>Carregando...</span>
        </div>
        <ChevronDown size={16} />
      </div>
    );
  }

  if (error) {
    return (
      <div style={buttonStyles}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <Users size={16} />
          <span>Erro ao carregar</span>
        </div>
        <ChevronDown size={16} />
      </div>
    );
  }

  if (families.length === 0) {
    return (
      <div style={buttonStyles}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <Users size={16} />
          <span>Nenhuma família</span>
        </div>
        <ChevronDown size={16} />
      </div>
    );
  }

  return (
    <>
      <button
        ref={buttonRef}
        onClick={handleButtonClick}
        style={buttonStyles}
        disabled={loading}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <Users size={16} />
          <span>{selectedFamily ? selectedFamily.name : 'Selecione uma família'}</span>
        </div>
        <ChevronDown size={16} />
      </button>

      {isOpen && buttonRect && createPortal(
        <div ref={dropdownRef} style={dropdownStyles}>
          {families.map((family) => (
            <div
              key={family.id}
              onClick={() => handleSelect(family.id)}
              style={{
                padding: '12px 16px',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                borderBottom: family.id === families[families.length - 1].id ? 'none' : '1px solid #f1f5f9',
                background: family.id === selectedFamilyId ? '#f8fafc' : 'white',
                transition: 'background 0.2s'
              }}
              onMouseEnter={(e) => {
                if (family.id !== selectedFamilyId) {
                  e.currentTarget.style.background = '#f8fafc';
                }
              }}
              onMouseLeave={(e) => {
                if (family.id !== selectedFamilyId) {
                  e.currentTarget.style.background = 'white';
                }
              }}
            >
              <span style={{
                fontSize: 14,
                color: family.id === selectedFamilyId ? '#3b82f6' : '#222',
                fontWeight: family.id === selectedFamilyId ? '600' : '500'
              }}>
                {family.name}
              </span>
              {family.id === selectedFamilyId && (
                <Check size={16} color="#3b82f6" />
              )}
            </div>
          ))}
        </div>,
        document.body
      )}
    </>
  );
} 