import React, { useState } from 'react';

interface BarChartData {
  label: string;
  value: number;
  color?: string;
  secondaryValue?: number;
}

interface BarChartProps {
  data: BarChartData[];
  height?: number;
  width?: number;
  showValues?: boolean;
  showGrid?: boolean;
  animate?: boolean;
  onBarClick?: (data: BarChartData, index: number) => void;
}

export default function BarChart({ 
  data, 
  height = 300, 
  width = 400,
  showValues = true,
  showGrid = true,
  animate = true,
  onBarClick 
}: BarChartProps) {
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);
  
  if (!data || data.length === 0) {
    return (
      <div style={{ 
        width, 
        height, 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center',
        color: '#666',
        fontSize: 14
      }}>
        Nenhum dado disponível
      </div>
    );
  }

  const maxValue = Math.max(...data.map(item => Math.max(item.value, item.secondaryValue || 0)));
  const minValue = Math.min(...data.map(item => Math.min(item.value, item.secondaryValue || 0)));
  const range = maxValue - minValue;
  
  const barWidth = (width - 80) / data.length;
  const chartHeight = height - 80;
  const chartWidth = width - 80;
  const startX = 40;
  const startY = height - 40;

  const getBarHeight = (value: number) => {
    if (range === 0) return 0;
    return (value - minValue) / range * chartHeight;
  };

  const getBarY = (value: number) => {
    return startY - getBarHeight(value);
  };

  const getBarColor = (index: number, defaultColor?: string) => {
    if (defaultColor) return defaultColor;
    
    const colors = [
      '#3b82f6', '#22c55e', '#f59e0b', '#ef4444', 
      '#8b5cf6', '#06b6d4', '#ec4899', '#84cc16'
    ];
    return colors[index % colors.length];
  };

  return (
    <div style={{ position: 'relative' }}>
      <svg width={width} height={height} style={{ display: 'block' }}>
        {/* Grid lines */}
        {showGrid && (
          <g>
            {Array.from({ length: 5 }, (_, i) => {
              const y = startY - (i * chartHeight / 4);
              const value = minValue + (i * range / 4);
              return (
                <g key={`grid-${i}`}>
                  <line
                    x1={startX}
                    y1={y}
                    x2={startX + chartWidth}
                    y2={y}
                    stroke="#e2e8f0"
                    strokeWidth="1"
                    opacity="0.5"
                  />
                  <text
                    x={startX - 8}
                    y={y + 4}
                    textAnchor="end"
                    dominantBaseline="middle"
                    fontSize="10"
                    fill="#666"
                  >
                    {value.toLocaleString('pt-BR', { 
                      style: 'currency', 
                      currency: 'BRL',
                      minimumFractionDigits: 0,
                      maximumFractionDigits: 0
                    })}
                  </text>
                </g>
              );
            })}
          </g>
        )}

        {/* Bars */}
        {data.map((item, index) => {
          const barX = startX + index * barWidth + barWidth / 2;
          const barHeight = getBarHeight(item.value);
          const barY = getBarY(item.value);
          
          return (
            <g key={`bar-${index}`}>
              {/* Main bar */}
              <rect
                x={barX - barWidth / 2 + 2}
                y={barY}
                width={barWidth - 4}
                height={barHeight}
                fill={getBarColor(index, item.color)}
                opacity={hoveredIndex === index ? 0.8 : 1}
                style={{ 
                  cursor: onBarClick ? 'pointer' : 'default',
                  transition: animate ? 'opacity 0.2s ease' : 'none'
                }}
                onClick={() => onBarClick?.(item, index)}
                onMouseEnter={() => setHoveredIndex(index)}
                onMouseLeave={() => setHoveredIndex(null)}
              />
              
              {/* Secondary bar if exists */}
              {item.secondaryValue && (
                <rect
                  x={barX - barWidth / 2 + 2}
                  y={getBarY(item.secondaryValue)}
                  width={barWidth - 4}
                  height={getBarHeight(item.secondaryValue)}
                  fill={getBarColor(index, item.color)}
                  opacity={0.3}
                />
              )}
              
              {/* Value label */}
              {showValues && (
                <text
                  x={barX}
                  y={barY - 8}
                  textAnchor="middle"
                  dominantBaseline="end"
                  fontSize="10"
                  fill="#666"
                  fontWeight="500"
                >
                  {item.value.toLocaleString('pt-BR', { 
                    style: 'currency', 
                    currency: 'BRL',
                    minimumFractionDigits: 0,
                    maximumFractionDigits: 0
                  })}
                </text>
              )}
              
              {/* X-axis label */}
              <text
                x={barX}
                y={startY + 20}
                textAnchor="middle"
                dominantBaseline="start"
                fontSize="10"
                fill="#666"
                style={{ 
                  transform: item.label.length > 8 ? 'rotate(-45deg)' : 'none',
                  transformOrigin: `${barX} ${startY + 20}`
                }}
              >
                {item.label}
              </text>
            </g>
          );
        })}

        {/* Axes */}
        <g>
          {/* Y-axis */}
          <line
            x1={startX}
            y1={startY}
            x2={startX}
            y2={startY - chartHeight}
            stroke="#666"
            strokeWidth="2"
          />
          
          {/* X-axis */}
          <line
            x1={startX}
            y1={startY}
            x2={startX + chartWidth}
            y2={startY}
            stroke="#666"
            strokeWidth="2"
          />
        </g>
      </svg>
      
      {/* Tooltip */}
      {hoveredIndex !== null && (
        <div style={{
          position: 'absolute',
          top: -60,
          left: '50%',
          transform: 'translateX(-50%)',
          background: '#333',
          color: 'white',
          padding: '8px 12px',
          borderRadius: '6px',
          fontSize: '12px',
          whiteSpace: 'nowrap',
          zIndex: 10,
          pointerEvents: 'none'
        }}>
          <div style={{ fontWeight: '600' }}>{data[hoveredIndex].label}</div>
          <div style={{ opacity: 0.8 }}>
            Valor: {data[hoveredIndex].value.toLocaleString('pt-BR', { 
              style: 'currency', 
              currency: 'BRL' 
            })}
          </div>
          {data[hoveredIndex].secondaryValue && (
            <div style={{ opacity: 0.8 }}>
              Secundário: {data[hoveredIndex].secondaryValue!.toLocaleString('pt-BR', { 
                style: 'currency', 
                currency: 'BRL' 
              })}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
