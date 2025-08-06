import React, { useEffect, useState } from 'react';
import { CheckCircle, AlertCircle, X, Info } from 'lucide-react';

interface ToastProps {
  message: string;
  type: 'success' | 'error' | 'warning' | 'info';
  duration?: number;
  onClose: () => void;
}

export default function Toast({ message, type, duration = 5000, onClose }: ToastProps) {
  const [isVisible, setIsVisible] = useState(true);
  const [isExiting, setIsExiting] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsExiting(true);
      setTimeout(onClose, 300); // Allow time for exit animation
    }, duration);

    return () => clearTimeout(timer);
  }, [duration, onClose]);

  const getIcon = () => {
    switch (type) {
      case 'success':
        return <CheckCircle size={20} />;
      case 'error':
        return <AlertCircle size={20} />;
      case 'warning':
        return <AlertCircle size={20} />;
      case 'info':
        return <Info size={20} />;
      default:
        return <Info size={20} />;
    }
  };

  const getColors = () => {
    switch (type) {
      case 'success':
        return {
          background: '#f0fdf4',
          border: '#bbf7d0',
          color: '#16a34a',
          iconColor: '#22c55e'
        };
      case 'error':
        return {
          background: '#fef2f2',
          border: '#fecaca',
          color: '#dc2626',
          iconColor: '#ef4444'
        };
      case 'warning':
        return {
          background: '#fffbeb',
          border: '#fed7aa',
          color: '#d97706',
          iconColor: '#f59e0b'
        };
      case 'info':
        return {
          background: '#eff6ff',
          border: '#bfdbfe',
          color: '#2563eb',
          iconColor: '#3b82f6'
        };
      default:
        return {
          background: '#f8fafc',
          border: '#e2e8f0',
          color: '#64748b',
          iconColor: '#94a3b8'
        };
    }
  };

  const colors = getColors();

  return (
    <div
      style={{
        position: 'fixed',
        top: 24,
        right: 24,
        background: colors.background,
        border: `1px solid ${colors.border}`,
        borderRadius: 12,
        padding: '16px 20px',
        display: 'flex',
        alignItems: 'center',
        gap: 12,
        boxShadow: '0 8px 32px rgba(0,0,0,0.12)',
        zIndex: 9999,
        minWidth: 300,
        maxWidth: 500,
        transform: isExiting ? 'translateX(100%)' : 'translateX(0)',
        opacity: isExiting ? 0 : 1,
        transition: 'all 0.3s ease-in-out',
        backdropFilter: 'blur(10px)'
      }}
    >
      <div style={{ color: colors.iconColor, flexShrink: 0 }}>
        {getIcon()}
      </div>
      
      <div style={{ 
        flex: 1, 
        color: colors.color, 
        fontSize: 14, 
        fontWeight: 500,
        lineHeight: 1.4
      }}>
        {message}
      </div>
      
      <button
        onClick={() => {
          setIsExiting(true);
          setTimeout(onClose, 300);
        }}
        style={{
          border: 'none',
          background: 'transparent',
          cursor: 'pointer',
          padding: 4,
          borderRadius: 4,
          color: colors.color,
          opacity: 0.7,
          transition: 'opacity 0.2s ease',
          flexShrink: 0
        }}
        onMouseEnter={e => e.currentTarget.style.opacity = '1'}
        onMouseLeave={e => e.currentTarget.style.opacity = '0.7'}
      >
        <X size={16} />
      </button>
    </div>
  );
}

// Toast Manager Context and Hook
interface ToastContextType {
  showToast: (message: string, type: 'success' | 'error' | 'warning' | 'info', duration?: number) => void;
}

const ToastContext = React.createContext<ToastContextType | undefined>(undefined);

interface ToastItem {
  id: string;
  message: string;
  type: 'success' | 'error' | 'warning' | 'info';
  duration?: number;
}

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = useState<ToastItem[]>([]);

  const showToast = (message: string, type: 'success' | 'error' | 'warning' | 'info', duration?: number) => {
    const id = Math.random().toString(36).substring(7);
    const newToast: ToastItem = { id, message, type, duration };
    
    setToasts(prev => [...prev, newToast]);
  };

  const removeToast = (id: string) => {
    setToasts(prev => prev.filter(toast => toast.id !== id));
  };

  const contextValue: ToastContextType = {
    showToast
  };

  return (
    <ToastContext.Provider value={contextValue}>
      {children}
      
      {/* Render Toasts */}
      <div style={{
        position: 'fixed',
        top: 24,
        right: 24,
        display: 'flex',
        flexDirection: 'column',
        gap: 12,
        zIndex: 9999,
        pointerEvents: 'none'
      }}>
        {toasts.map((toast, index) => (
          <div
            key={toast.id}
            style={{
              transform: `translateY(${index * 80}px)`,
              pointerEvents: 'auto'
            }}
          >
            <Toast
              message={toast.message}
              type={toast.type}
              duration={toast.duration}
              onClose={() => removeToast(toast.id)}
            />
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}

export function useToast() {
  const context = React.useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
}