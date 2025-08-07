import React, { useState, useRef, useEffect } from 'react';
import { createPortal } from 'react-dom';
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
  variant?: 'default' | 'header';
}

export default function FamilySelect({ 
  families, 
  selectedFamilyId, 
  onFamilyChange, 
  placeholder = "Selecione uma família",
  disabled = false,
  variant = 'default'
}: FamilySelectProps) {
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
    if (!disabled) {
      if (!isOpen && buttonRef.current) {
        setButtonRect(buttonRef.current.getBoundingClientRect());
      }
      setIsOpen(!isOpen);
    }
  };

  const handleSelect = (familyId: number) => {
    onFamilyChange(familyId);
    setIsOpen(false);
  };

  // Estilos baseados na variante
  const getButtonStyles = () => {
    if (variant === 'header') {
      return {
        width: '100%',
        padding: '8px 12px',
        borderRadius: 6,
        border: '1px solid rgba(255,255,255,0.3)',
        background: disabled ? 'rgba(255,255,255,0.1)' : 'rgba(255,255,255,0.9)',
        color: disabled ? 'rgba(255,255,255,0.6)' : '#222',
        cursor: disabled ? 'not-allowed' : 'pointer',
        fontSize: 13,
        fontWeight: 500,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        transition: 'all 0.2s ease',
        minHeight: 36,
        backdropFilter: 'blur(10px)'
      };
    }
    
    return {
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
    };
  };

  const getDropdownStyles = () => {
    if (variant === 'header') {
      return {
        position: 'absolute',
        top: '100%',
        left: 0,
        right: 0,
        background: 'rgba(255,255,255,0.95)',
        border: '1px solid rgba(255,255,255,0.3)',
        borderRadius: 8,
        boxShadow: '0 8px 32px rgba(0,0,0,0.2)',
        zIndex: 1000,
        maxHeight: 200,
        overflowY: 'auto',
        backdropFilter: 'blur(10px)',
        marginTop: 4
      };
    }
    
    return {
      position: 'absolute',
      top: '100%',
      left: 0,
      right: 0,
      background: '#fff',
      border: '1px solid #ddd',
      borderRadius: 8,
      boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
      zIndex: 1000,
      maxHeight: 200,
      overflowY: 'auto',
      marginTop: 4
    };
  };

  const getOptionStyles = (isSelected: boolean) => {
    if (variant === 'header') {
      return {
        padding: '10px 12px',
        cursor: 'pointer',
        fontSize: 13,
        fontWeight: isSelected ? 600 : 500,
        color: isSelected ? '#667eea' : '#333',
        background: isSelected ? 'rgba(102, 126, 234, 0.1)' : 'transparent',
        display: 'flex',
        alignItems: 'center',
        gap: 8,
        transition: 'all 0.2s ease',
        borderBottom: '1px solid rgba(0,0,0,0.05)'
      };
    }
    
    return {
      padding: '12px 16px',
      cursor: 'pointer',
      fontSize: 14,
      fontWeight: isSelected ? 600 : 500,
      color: isSelected ? '#667eea' : '#333',
      background: isSelected ? 'rgba(102, 126, 234, 0.1)' : 'transparent',
      display: 'flex',
      alignItems: 'center',
      gap: 8,
      transition: 'all 0.2s ease',
      borderBottom: '1px solid #f0f0f0'
    };
  };

  return (
    <div style={{ position: 'relative', minWidth: 200 }}>
      <button
        ref={buttonRef}
        onClick={handleButtonClick}
        disabled={disabled}
        style={getButtonStyles()}
        onMouseEnter={(e) => {
          if (!disabled && variant === 'header') {
            e.currentTarget.style.background = 'rgba(255,255,255,0.95)';
          } else if (!disabled) {
            e.currentTarget.style.background = '#f8f9fa';
          }
        }}
        onMouseLeave={(e) => {
          if (!disabled && variant === 'header') {
            e.currentTarget.style.background = 'rgba(255,255,255,0.9)';
          } else if (!disabled) {
            e.currentTarget.style.background = '#fff';
          }
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, flex: 1 }}>
          <Users size={16} style={{ color: variant === 'header' ? '#667eea' : '#666' }} />
          <span style={{ 
            overflow: 'hidden', 
            textOverflow: 'ellipsis', 
            whiteSpace: 'nowrap',
            color: variant === 'header' ? '#222' : undefined
          }}>
            {selectedFamily ? selectedFamily.name : placeholder}
          </span>
        </div>
        <ChevronDown 
          size={16} 
          style={{ 
            color: variant === 'header' ? '#667eea' : '#666',
            transform: isOpen ? 'rotate(180deg)' : 'rotate(0deg)',
            transition: 'transform 0.2s ease'
          }} 
        />
      </button>

      {isOpen && buttonRect && createPortal(
        <div
          ref={dropdownRef}
          style={{
            ...getDropdownStyles(),
            position: 'fixed',
            top: buttonRect.bottom + 4,
            left: buttonRect.left,
            width: buttonRect.width
          }}
        >
          {families.map((family) => (
            <div
              key={family.id}
              onClick={() => handleSelect(family.id)}
              style={getOptionStyles(family.id === selectedFamilyId)}
              onMouseEnter={(e) => {
                if (family.id !== selectedFamilyId) {
                  e.currentTarget.style.background = variant === 'header' 
                    ? 'rgba(102, 126, 234, 0.05)' 
                    : '#f8f9fa';
                }
              }}
              onMouseLeave={(e) => {
                if (family.id !== selectedFamilyId) {
                  e.currentTarget.style.background = 'transparent';
                }
              }}
            >
              <Users size={14} style={{ color: '#667eea' }} />
              <span style={{ flex: 1 }}>{family.name}</span>
              {family.id === selectedFamilyId && (
                <Check size={14} style={{ color: '#667eea' }} />
              )}
            </div>
          ))}
        </div>,
        document.body
      )}
    </div>
  );
} 