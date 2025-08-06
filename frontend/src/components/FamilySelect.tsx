import React, { useState, useRef, useEffect } from 'react';
import { ChevronDown, Users, Check } from 'lucide-react';

interface Family {
  id: number;
  name: string;
}

interface FamilySelectProps {
  families: Family[];
  selectedFamilyId: number | null;
  onFamilyChange: (familyId: number) => void;
  placeholder?: string;
  disabled?: boolean;
}

export default function FamilySelect({ 
  families, 
  selectedFamilyId, 
  onFamilyChange, 
  placeholder = "Selecione uma família",
  disabled = false 
}: FamilySelectProps) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const selectedFamily = families.find(f => f.id === selectedFamilyId);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleSelect = (familyId: number) => {
    onFamilyChange(familyId);
    setIsOpen(false);
  };

  return (
    <div ref={dropdownRef} style={{ position: 'relative', minWidth: 200 }}>
      <button
        onClick={() => !disabled && setIsOpen(!isOpen)}
        disabled={disabled}
        style={{
          width: '100%',
          padding: '10px 16px',
          borderRadius: 8,
          border: '1px solid #ddd',
          background: disabled ? '#f8f9fa' : '#fff',
          color: disabled ? '#6c757d' : '#222',
          cursor: disabled ? 'not-allowed' : 'pointer',
          fontSize: 14,
          fontWeight: 500,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          transition: 'all 0.2s ease',
          minHeight: 42
        }}
        onMouseEnter={(e) => {
          if (!disabled) {
            e.currentTarget.style.borderColor = '#667eea';
            e.currentTarget.style.boxShadow = '0 0 0 3px rgba(102, 126, 234, 0.1)';
          }
        }}
        onMouseLeave={(e) => {
          if (!disabled) {
            e.currentTarget.style.borderColor = '#ddd';
            e.currentTarget.style.boxShadow = 'none';
          }
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <Users size={16} color={disabled ? '#6c757d' : '#667eea'} />
          <span style={{ 
            color: selectedFamily ? '#222' : '#666',
            fontWeight: selectedFamily ? 500 : 400
          }}>
            {selectedFamily ? selectedFamily.name : placeholder}
          </span>
        </div>
        <ChevronDown 
          size={16} 
          color={disabled ? '#6c757d' : '#666'}
          style={{ 
            transition: 'transform 0.2s ease',
            transform: isOpen ? 'rotate(180deg)' : 'rotate(0deg)'
          }} 
        />
      </button>

      {isOpen && (
        <div style={{
          position: 'absolute',
          top: '100%',
          left: 0,
          right: 0,
          background: '#fff',
          borderRadius: 8,
          border: '1px solid #e9ecef',
          boxShadow: '0 8px 32px rgba(0,0,0,0.12)',
          zIndex: 1000,
          marginTop: 4,
          maxHeight: 200,
          overflow: 'auto'
        }}>
          {families.length === 0 ? (
            <div style={{
              padding: '12px 16px',
              color: '#666',
              fontSize: 14,
              textAlign: 'center'
            }}>
              Nenhuma família disponível
            </div>
          ) : (
            families.map((family) => (
              <button
                key={family.id}
                onClick={() => handleSelect(family.id)}
                style={{
                  width: '100%',
                  padding: '10px 16px',
                  border: 'none',
                  background: 'transparent',
                  color: '#222',
                  cursor: 'pointer',
                  fontSize: 14,
                  textAlign: 'left',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  transition: 'all 0.2s ease'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = '#f8f9fa';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = 'transparent';
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <Users size={16} color="#667eea" />
                  <span style={{ fontWeight: family.id === selectedFamilyId ? 600 : 400 }}>
                    {family.name}
                  </span>
                </div>
                {family.id === selectedFamilyId && (
                  <Check size={16} color="#667eea" />
                )}
              </button>
            ))
          )}
        </div>
      )}
    </div>
  );
} 