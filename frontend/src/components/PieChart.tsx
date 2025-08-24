import React, { useState } from 'react';

interface PieChartData {
  label: string;
  value: number;
  color: string;
}

interface PieChartProps {
  data: PieChartData[];
  size?: number;
  showLabels?: boolean;
  showValues?: boolean;
  onSliceClick?: (data: PieChartData, index: number) => void;
}

export default function PieChart({ 
  data, 
  size = 200, 
  showLabels = true, 
  showValues = true,
  onSliceClick 
}: PieChartProps) {
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);
  
  if (!data || data.length === 0) {
    return (
      <div style={{ 
        width: size, 
        height: size, 
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

  const total = data.reduce((sum, item) => sum + item.value, 0);
  const centerX = size / 2;
  const centerY = size / 2;
  const radius = Math.min(centerX, centerY) - 20;

  let currentAngle = -90; // Começar do topo
  const paths: JSX.Element[] = [];
  const labels: JSX.Element[] = [];

  data.forEach((item, index) => {
    const percentage = total > 0 ? (item.value / total) : 0;
    const angle = (percentage * 360);
    const endAngle = currentAngle + angle;

    // Calcular coordenadas do arco
    const startX = centerX + radius * Math.cos(currentAngle * Math.PI / 180);
    const startY = centerY + radius * Math.sin(currentAngle * Math.PI / 180);
    const endX = centerX + radius * Math.cos(endAngle * Math.PI / 180);
    const endY = centerY + radius * Math.sin(endAngle * Math.PI / 180);

    // Determinar se o arco é maior que 180 graus
    const largeArcFlag = angle > 180 ? 1 : 0;

    // Criar o path do arco
    const pathData = [
      `M ${startX} ${startY}`,
      `A ${radius} ${radius} 0 ${largeArcFlag} 1 ${endX} ${endY}`,
      'L ' + centerX + ' ' + centerY,
      'Z'
    ].join(' ');

    // Calcular posição do label
    const labelAngle = currentAngle + angle / 2;
    const labelRadius = radius + 30;
    const labelX = centerX + labelRadius * Math.cos(labelAngle * Math.PI / 180);
    const labelY = centerY + labelRadius * Math.sin(labelAngle * Math.PI / 180);

    // Adicionar o slice
    paths.push(
      <path
        key={`slice-${index}`}
        d={pathData}
        fill={item.color}
        stroke="white"
        strokeWidth="2"
        opacity={hoveredIndex === index ? 0.8 : 1}
        style={{ 
          cursor: onSliceClick ? 'pointer' : 'default',
          transition: 'opacity 0.2s ease'
        }}
        onClick={() => onSliceClick?.(item, index)}
        onMouseEnter={() => setHoveredIndex(index)}
        onMouseLeave={() => setHoveredIndex(null)}
      />
    );

    // Adicionar o label
    if (showLabels && percentage > 0.05) { // Só mostrar labels para slices > 5%
      labels.push(
        <g key={`label-${index}`}>
          <line
            x1={centerX + (radius + 10) * Math.cos(labelAngle * Math.PI / 180)}
            y1={centerY + (radius + 10) * Math.sin(labelAngle * Math.PI / 180)}
            x2={centerX + (radius + 25) * Math.cos(labelAngle * Math.PI / 180)}
            y2={centerY + (radius + 25) * Math.sin(labelAngle * Math.PI / 180)}
            stroke="#666"
            strokeWidth="1"
            opacity="0.5"
          />
          <text
            x={labelX}
            y={labelY}
            textAnchor={labelX > centerX ? 'start' : 'end'}
            dominantBaseline="middle"
            fontSize="12"
            fill="#666"
            fontWeight="500"
          >
            {item.label}
          </text>
          {showValues && (
            <text
              x={labelX}
              y={labelY + 16}
              textAnchor={labelX > centerX ? 'start' : 'end'}
              dominantBaseline="middle"
              fontSize="10"
              fill="#999"
            >
              {percentage.toFixed(1)}%
            </text>
          )}
        </g>
      );
    }

    currentAngle = endAngle;
  });

  return (
    <div style={{ position: 'relative' }}>
      <svg width={size} height={size} style={{ display: 'block' }}>
        {/* Slices */}
        {paths}
        
        {/* Labels */}
        {labels}
        
        {/* Centro do gráfico */}
        <circle
          cx={centerX}
          cy={centerY}
          r={radius * 0.3}
          fill="white"
          stroke="#e2e8f0"
          strokeWidth="1"
        />
        
        {/* Informação central */}
        <text
          x={centerX}
          y={centerY - 8}
          textAnchor="middle"
          dominantBaseline="middle"
          fontSize="14"
          fontWeight="600"
          fill="#666"
        >
          Total
        </text>
        <text
          x={centerX}
          y={centerY + 8}
          textAnchor="middle"
          dominantBaseline="middle"
          fontSize="12"
          fill="#999"
        >
          {total.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
        </text>
      </svg>
      
      {/* Tooltip */}
      {hoveredIndex !== null && (
        <div style={{
          position: 'absolute',
          top: -40,
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
            {data[hoveredIndex].value.toLocaleString('pt-BR', { 
              style: 'currency', 
              currency: 'BRL' 
            })}
          </div>
        </div>
      )}
    </div>
  );
}
