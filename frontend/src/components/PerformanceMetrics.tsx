import React from 'react';
import { TrendingUp, TrendingDown, Minus, Activity } from 'lucide-react';

interface PerformanceMetricsProps {
  currentValue: number;
  previousValue: number;
  label: string;
  formatValue?: (value: number) => string;
  showPercentage?: boolean;
  showTrend?: boolean;
  size?: 'small' | 'medium' | 'large';
}

export default function PerformanceMetrics({
  currentValue,
  previousValue,
  label,
  formatValue = (value) => value.toLocaleString('pt-BR'),
  showPercentage = true,
  showTrend = true,
  size = 'medium'
}: PerformanceMetricsProps) {
  const change = currentValue - previousValue;
  const changePercentage = previousValue !== 0 ? (change / previousValue) * 100 : 0;
  
  const getTrendIcon = () => {
    if (change > 0) return <TrendingUp size={16} color="#22c55e" />;
    if (change < 0) return <TrendingDown size={16} color="#ef4444" />;
    return <Minus size={16} color="#666" />;
  };

  const getTrendColor = () => {
    if (change > 0) return '#22c55e';
    if (change < 0) return '#ef4444';
    return '#666';
  };

  const getSizeStyles = () => {
    switch (size) {
      case 'small':
        return {
          container: { padding: '12px 16px' },
          label: { fontSize: '12px', marginBottom: '4px' },
          value: { fontSize: '18px', marginBottom: '4px' },
          change: { fontSize: '10px' }
        };
      case 'large':
        return {
          container: { padding: '24px 32px' },
          label: { fontSize: '16px', marginBottom: '8px' },
          value: { fontSize: '32px', marginBottom: '8px' },
          change: { fontSize: '14px' }
        };
      default: // medium
        return {
          container: { padding: '16px 20px' },
          label: { fontSize: '14px', marginBottom: '6px' },
          value: { fontSize: '24px', marginBottom: '6px' },
          change: { fontSize: '12px' }
        };
    }
  };

  const styles = getSizeStyles();

  return (
    <div style={{
      background: 'white',
      borderRadius: '12px',
      border: '1px solid #e2e8f0',
      boxShadow: '0 2px 4px rgba(0, 0, 0, 0.05)',
      ...styles.container
    }}>
      {/* Label */}
      <div style={{
        color: '#666',
        fontWeight: '500',
        ...styles.label
      }}>
        {label}
      </div>

      {/* Current Value */}
      <div style={{
        color: '#222',
        fontWeight: '700',
        ...styles.value
      }}>
        {formatValue(currentValue)}
      </div>

      {/* Change Indicator */}
      {showTrend && (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
          color: getTrendColor(),
          fontWeight: '500',
          ...styles.change
        }}>
          {getTrendIcon()}
          {showPercentage && (
            <span>
              {changePercentage > 0 ? '+' : ''}{changePercentage.toFixed(1)}%
            </span>
          )}
          {change !== 0 && (
            <span>
              ({change > 0 ? '+' : ''}{formatValue(change)})
            </span>
          )}
        </div>
      )}
    </div>
  );
}

interface PerformanceGridProps {
  metrics: Array<{
    label: string;
    currentValue: number;
    previousValue: number;
    formatValue?: (value: number) => string;
    showPercentage?: boolean;
    showTrend?: boolean;
  }>;
  columns?: number;
  size?: 'small' | 'medium' | 'large';
}

export function PerformanceGrid({ metrics, columns = 2, size = 'medium' }: PerformanceGridProps) {
  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: `repeat(${columns}, 1fr)`,
      gap: '16px'
    }}>
      {metrics.map((metric, index) => (
        <PerformanceMetrics
          key={index}
          label={metric.label}
          currentValue={metric.currentValue}
          previousValue={metric.previousValue}
          formatValue={metric.formatValue}
          showPercentage={metric.showPercentage}
          showTrend={metric.showTrend}
          size={size}
        />
      ))}
    </div>
  );
}

interface PerformanceCardProps {
  title: string;
  currentValue: number;
  previousValue: number;
  icon?: React.ReactNode;
  formatValue?: (value: number) => string;
  showPercentage?: boolean;
  showTrend?: boolean;
  color?: string;
}

export function PerformanceCard({
  title,
  currentValue,
  previousValue,
  icon,
  formatValue,
  showPercentage = true,
  showTrend = true,
  color = '#3b82f6'
}: PerformanceCardProps) {
  const change = currentValue - previousValue;
  const changePercentage = previousValue !== 0 ? (change / previousValue) * 100 : 0;

  return (
    <div style={{
      background: `linear-gradient(135deg, ${color}15 0%, ${color}05 100%)`,
      border: `1px solid ${color}20`,
      borderRadius: '16px',
      padding: '24px',
      position: 'relative',
      overflow: 'hidden'
    }}>
      {/* Background Pattern */}
      <div style={{
        position: 'absolute',
        top: '-20px',
        right: '-20px',
        width: '80px',
        height: '80px',
        background: color,
        opacity: '0.1',
        borderRadius: '50%'
      }} />
      
      {/* Header */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        marginBottom: '16px'
      }}>
        <h3 style={{
          margin: 0,
          color: '#222',
          fontSize: '16',
          fontWeight: '600'
        }}>
          {title}
        </h3>
        {icon && (
          <div style={{
            color: color,
            opacity: '0.8'
          }}>
            {icon}
          </div>
        )}
      </div>

      {/* Value */}
      <div style={{
        fontSize: '32px',
        fontWeight: '700',
        color: '#222',
        marginBottom: '8px'
      }}>
        {formatValue ? formatValue(currentValue) : currentValue.toLocaleString('pt-BR')}
      </div>

      {/* Change */}
      {showTrend && (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          fontSize: '14px',
          fontWeight: '500'
        }}>
          {change > 0 ? (
            <TrendingUp size={16} color="#22c55e" />
          ) : change < 0 ? (
            <TrendingDown size={16} color="#ef4444" />
          ) : (
            <Minus size={16} color="#666" />
          )}
          
          <span style={{
            color: change > 0 ? '#22c55e' : change < 0 ? '#ef4444' : '#666'
          }}>
            {showPercentage && (
              <span>
                {changePercentage > 0 ? '+' : ''}{changePercentage.toFixed(1)}%
              </span>
            )}
            {change !== 0 && (
              <span style={{ marginLeft: '4px' }}>
                ({change > 0 ? '+' : ''}{change.toLocaleString('pt-BR')})
              </span>
            )}
          </span>
        </div>
      )}
    </div>
  );
}
