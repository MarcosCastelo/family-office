import React, { useState, useEffect } from 'react';
import { 
  Bell, 
  X, 
  AlertTriangle, 
  Info, 
  CheckCircle, 
  Clock,
  Settings
} from 'lucide-react';
import type { Notification } from '../types/notification';

interface NotificationCenterProps {
  notifications: Notification[];
  onMarkAsRead?: (id: string) => void;
  onMarkAllAsRead?: () => void;
  onDelete?: (id: string) => void;
  maxNotifications?: number;
  showUnreadCount?: boolean;
}

export default function NotificationCenter({
  notifications,
  onMarkAsRead,
  onMarkAllAsRead,
  onDelete,
  maxNotifications = 5,
  showUnreadCount = true
}: NotificationCenterProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [filter, setFilter] = useState<'all' | 'unread'>('all');

  const unreadCount = notifications.filter(n => !n.read).length;
  const filteredNotifications = filter === 'unread' 
    ? notifications.filter(n => !n.read)
    : notifications;

  const getTypeIcon = (type: Notification['type']) => {
    switch (type) {
      case 'success':
        return <CheckCircle size={16} color="#22c55e" />;
      case 'warning':
        return <AlertTriangle size={16} color="#f59e0b" />;
      case 'error':
        return <AlertTriangle size={16} color="#ef4444" />;
      default:
        return <Info size={16} color="#3b82f6" />;
    }
  };

  const getTypeColor = (type: Notification['type']) => {
    switch (type) {
      case 'success':
        return '#22c55e';
      case 'warning':
        return '#f59e0b';
      case 'error':
        return '#ef4444';
      default:
        return '#3b82f6';
    }
  };

  const formatTimestamp = (timestamp: Date) => {
    const now = new Date();
    const diff = now.getTime() - timestamp.getTime();
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 1) return 'Agora';
    if (minutes < 60) return `${minutes}m atrás`;
    if (hours < 24) return `${hours}h atrás`;
    if (days < 7) return `${days}d atrás`;
    return timestamp.toLocaleDateString('pt-BR');
  };

  const handleNotificationClick = (notification: Notification) => {
    if (!notification.read && onMarkAsRead) {
      onMarkAsRead(notification.id);
    }
  };

  const handleMarkAllAsRead = () => {
    if (onMarkAllAsRead) {
      onMarkAllAsRead();
    }
  };

  return (
    <div style={{ position: 'relative' }}>
      {/* Notification Bell */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={{
          background: 'none',
          border: 'none',
          padding: '8px',
          borderRadius: '8px',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: '#666',
          position: 'relative'
        }}
        title="Notificações"
      >
        <Bell size={20} />
        {showUnreadCount && unreadCount > 0 && (
          <div style={{
            position: 'absolute',
            top: '-4px',
            right: '-4px',
            background: '#ef4444',
            color: 'white',
            borderRadius: '50%',
            width: '18px',
            height: '18px',
            fontSize: '10px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontWeight: '600'
          }}>
            {unreadCount > 99 ? '99+' : unreadCount}
          </div>
        )}
      </button>

      {/* Notification Panel */}
      {isOpen && (
        <div style={{
          position: 'absolute',
          top: '100%',
          right: 0,
          width: '400px',
          background: 'white',
          borderRadius: '12px',
          border: '1px solid #e2e8f0',
          boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
          zIndex: 1000,
          marginTop: '8px'
        }}>
          {/* Header */}
          <div style={{
            padding: '16px 20px',
            borderBottom: '1px solid #f1f5f9',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between'
          }}>
            <h3 style={{ margin: 0, fontSize: '16px', fontWeight: '600', color: '#222' }}>
              Notificações
            </h3>
            <div style={{ display: 'flex', gap: '8px' }}>
              <button
                onClick={handleMarkAllAsRead}
                style={{
                  background: 'none',
                  border: 'none',
                  padding: '4px 8px',
                  borderRadius: '4px',
                  fontSize: '11px',
                  color: '#3b82f6',
                  cursor: 'pointer',
                  fontWeight: '500'
                }}
              >
                Marcar como lidas
              </button>
              <button
                onClick={() => setIsOpen(false)}
                style={{
                  background: 'none',
                  border: 'none',
                  padding: '4px',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  color: '#666',
                  opacity: '0.7'
                }}
              >
                <X size={16} />
              </button>
            </div>
          </div>

          {/* Filters */}
          <div style={{
            padding: '12px 20px',
            borderBottom: '1px solid #f1f5f9',
            display: 'flex',
            gap: '8px'
          }}>
            <button
              onClick={() => setFilter('all')}
              style={{
                background: filter === 'all' ? '#3b82f6' : 'none',
                color: filter === 'all' ? 'white' : '#666',
                border: '1px solid #e2e8f0',
                padding: '6px 12px',
                borderRadius: '6px',
                fontSize: '12px',
                cursor: 'pointer',
                fontWeight: '500'
              }}
            >
              Todas
            </button>
            <button
              onClick={() => setFilter('unread')}
              style={{
                background: filter === 'unread' ? '#3b82f6' : 'none',
                color: filter === 'unread' ? 'white' : '#666',
                border: '1px solid #e2e8f0',
                padding: '6px 12px',
                borderRadius: '6px',
                fontSize: '12px',
                cursor: 'pointer',
                fontWeight: '500'
              }}
            >
              Não lidas
            </button>
          </div>

          {/* Notifications List */}
          <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
            {filteredNotifications.length === 0 ? (
              <div style={{
                padding: '40px 20px',
                textAlign: 'center',
                color: '#666',
                fontSize: '14px'
              }}>
                Nenhuma notificação
              </div>
            ) : (
              <div>
                {filteredNotifications.slice(0, maxNotifications).map((notification) => (
                  <div
                    key={notification.id}
                    onClick={() => handleNotificationClick(notification)}
                    style={{
                      padding: '16px 20px',
                      borderBottom: '1px solid #f1f5f9',
                      cursor: 'pointer',
                      transition: 'background 0.2s',
                      position: 'relative'
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.background = '#f8fafc';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.background = 'white';
                    }}
                  >
                    {/* Unread indicator */}
                    {!notification.read && (
                      <div style={{
                        position: 'absolute',
                        left: '8px',
                        top: '50%',
                        transform: 'translateY(-50%)',
                        width: '6px',
                        height: '6px',
                        background: '#3b82f6',
                        borderRadius: '50%'
                      }} />
                    )}

                    {/* Notification content */}
                    <div style={{ marginLeft: notification.read ? '0' : '16px' }}>
                      <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        marginBottom: '4px'
                      }}>
                        {getTypeIcon(notification.type)}
                        <div style={{
                          fontSize: '14px',
                          fontWeight: '600',
                          color: '#222',
                          flex: 1
                        }}>
                          {notification.title}
                        </div>
                      </div>
                      
                      <div style={{
                        fontSize: '13px',
                        color: '#666',
                        marginBottom: '8px',
                        lineHeight: '1.4'
                      }}>
                        {notification.message}
                      </div>

                      {/* Footer */}
                      <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        fontSize: '11px',
                        color: '#999'
                      }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                          <Clock size={12} />
                          {formatTimestamp(notification.timestamp)}
                        </div>
                        
                        <div style={{ display: 'flex', gap: '4px' }}>
                          {notification.action && (
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                notification.action!.onClick();
                              }}
                              style={{
                                background: `${getTypeColor(notification.type)}10`,
                                border: 'none',
                                padding: '4px 8px',
                                borderRadius: '4px',
                                fontSize: '11px',
                                color: getTypeColor(notification.type),
                                cursor: 'pointer',
                                fontWeight: '500'
                              }}
                            >
                              {notification.action.label}
                            </button>
                          )}
                          
                          {onDelete && (
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                onDelete(notification.id);
                              }}
                              style={{
                                background: 'none',
                                border: 'none',
                                padding: '4px',
                                borderRadius: '4px',
                                cursor: 'pointer',
                                color: '#999',
                                opacity: '0.7'
                              }}
                              title="Excluir"
                            >
                              <X size={12} />
                            </button>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Footer */}
          {filteredNotifications.length > maxNotifications && (
            <div style={{
              padding: '12px 20px',
              borderTop: '1px solid #f1f5f9',
              textAlign: 'center',
              fontSize: '12px',
              color: '#666'
            }}>
              Mostrando {maxNotifications} de {filteredNotifications.length} notificações
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// Hook para gerenciar notificações
export function useNotifications() {
  const [notifications, setNotifications] = useState<Notification[]>([]);

  const addNotification = (notification: Omit<Notification, 'id' | 'timestamp' | 'read'>) => {
    const newNotification: Notification = {
      ...notification,
      id: Date.now().toString(),
      timestamp: new Date(),
      read: false
    };
    setNotifications(prev => [newNotification, ...prev]);
  };

  const markAsRead = (id: string) => {
    setNotifications(prev => 
      prev.map(n => n.id === id ? { ...n, read: true } : n)
    );
  };

  const markAllAsRead = () => {
    setNotifications(prev => prev.map(n => ({ ...n, read: true })));
  };

  const deleteNotification = (id: string) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
  };

  const clearAll = () => {
    setNotifications([]);
  };

  return {
    notifications,
    addNotification,
    markAsRead,
    markAllAsRead,
    deleteNotification,
    clearAll
  };
}
