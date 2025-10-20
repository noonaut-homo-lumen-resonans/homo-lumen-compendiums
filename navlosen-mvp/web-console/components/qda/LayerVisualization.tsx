/**
 * QDA v2.0 - Layer Visualization Component
 * 
 * Displays the 6 neurobiological layers with polyvagal-adaptive colors
 * 
 * @version 2.0
 * @date 2025-10-20
 */

'use client';

import React, { useState } from 'react';
import type { LayerOutput, QDAResponse } from '@/lib/qda';

interface Props {
  response: QDAResponse;
  showDebugInfo?: boolean;
}

export const LayerVisualization: React.FC<Props> = ({ response, showDebugInfo = false }) => {
  const [expandedLayer, setExpandedLayer] = useState<string | null>(null);

  const polyvagalState = response.polyvagal_state;
  const stateColors = getPolyvagalColors(polyvagalState);

  const toggleLayer = (layerName: string) => {
    setExpandedLayer(expandedLayer === layerName ? null : layerName);
  };

  return (
    <div
      style={{
        backgroundColor: stateColors.bg,
        padding: '24px',
        borderRadius: '12px',
        border: `2px solid ${stateColors.primary}`,
      }}
    >
      {/* Header */}
      <div style={{ marginBottom: '20px' }}>
        <h3 style={{ color: stateColors.primary, fontSize: '20px', fontWeight: 'bold', marginBottom: '8px' }}>
          Nevrobiologisk Prosessering
        </h3>
        <p style={{ fontSize: '14px', color: '#666', marginBottom: '12px' }}>
          Du er i <strong style={{ color: stateColors.primary }}>{getPolyvagalLabel(polyvagalState)}</strong> tilstand
        </p>
        
        {/* Metrics */}
        <div style={{ display: 'flex', gap: '16px', fontSize: '13px' }}>
          <div>
            <span style={{ color: '#888' }}>Høyeste lag:</span>{' '}
            <strong style={{ color: stateColors.primary }}>{response.highest_layer_used}</strong>
          </div>
          <div>
            <span style={{ color: '#888' }}>Kompleksitet:</span>{' '}
            <strong>{(response.complexity_score * 100).toFixed(0)}%</strong>
          </div>
          <div>
            <span style={{ color: '#888' }}>Kostnad:</span>{' '}
            <strong>${response.total_cost.toFixed(4)}</strong>
          </div>
          <div>
            <span style={{ color: '#888' }}>Tid:</span>{' '}
            <strong>{response.total_time}ms</strong>
          </div>
        </div>
      </div>

      {/* Layers */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {response.layers.map((layer) => (
          <LayerCard
            key={layer.layer_name}
            layer={layer}
            isExpanded={expandedLayer === layer.layer_name}
            onToggle={() => toggleLayer(layer.layer_name)}
            showDebugInfo={showDebugInfo}
          />
        ))}
      </div>
    </div>
  );
};

interface LayerCardProps {
  layer: LayerOutput;
  isExpanded: boolean;
  onToggle: () => void;
  showDebugInfo?: boolean;
}

const LayerCard: React.FC<LayerCardProps> = ({ layer, isExpanded, onToggle, showDebugInfo }) => {
  const layerConfig = getLayerConfig(layer.layer_name);
  const isActive = layer.activated;

  return (
    <div
      style={{
        backgroundColor: isActive ? layerConfig.bgColor : '#f5f5f5',
        border: `2px solid ${isActive ? layerConfig.color : '#ddd'}`,
        borderRadius: '8px',
        padding: '16px',
        cursor: 'pointer',
        transition: 'all 0.2s ease',
        opacity: isActive ? 1 : 0.5,
      }}
      onClick={onToggle}
    >
      {/* Layer Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span style={{ fontSize: '24px' }}>{layerConfig.icon}</span>
          <div>
            <h4 style={{ fontSize: '16px', fontWeight: 'bold', color: layerConfig.color, marginBottom: '4px' }}>
              {layer.layer_number}. {layer.layer_name}
            </h4>
            <p style={{ fontSize: '12px', color: '#666' }}>{layerConfig.description}</p>
          </div>
        </div>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          {isActive && (
            <>
              <div style={{ textAlign: 'right', fontSize: '12px' }}>
                <div style={{ color: '#888' }}>
                  {layer.processing_time}ms
                </div>
                <div style={{ color: layerConfig.color, fontWeight: 'bold' }}>
                  ${layer.cost.toFixed(4)}
                </div>
              </div>
            </>
          )}
          
          <span style={{ fontSize: '18px', color: '#888' }}>
            {isExpanded ? '▼' : '▶'}
          </span>
        </div>
      </div>

      {/* Expanded Content */}
      {isExpanded && isActive && (
        <div style={{ marginTop: '16px', paddingTop: '16px', borderTop: '1px solid #ddd' }}>
          {showDebugInfo && (
            <pre style={{ 
              fontSize: '11px', 
              color: '#444', 
              backgroundColor: '#f9f9f9', 
              padding: '12px', 
              borderRadius: '4px',
              overflow: 'auto',
              maxHeight: '200px'
            }}>
              {JSON.stringify(layer.data, null, 2)}
            </pre>
          )}
          
          {!showDebugInfo && (
            <div style={{ fontSize: '13px', color: '#555' }}>
              {renderLayerSummary(layer)}
            </div>
          )}
        </div>
      )}

      {/* Skipped Reason */}
      {!isActive && layer.data?.reason && (
        <div style={{ marginTop: '8px', fontSize: '12px', color: '#888', fontStyle: 'italic' }}>
          Hoppet over: {layer.data.reason}
        </div>
      )}
    </div>
  );
};

// Helper: Get polyvagal colors
function getPolyvagalColors(state: 'dorsal' | 'sympathetic' | 'ventral') {
  const colors = {
    dorsal: { primary: '#4CAF50', bg: '#E8F5E9' },      // Green (safe, rest)
    sympathetic: { primary: '#FF9800', bg: '#FFF3E0' }, // Orange (alert, stress)
    ventral: { primary: '#2196F3', bg: '#E3F2FD' },     // Blue (social, calm)
  };
  return colors[state];
}

// Helper: Get polyvagal label
function getPolyvagalLabel(state: 'dorsal' | 'sympathetic' | 'ventral'): string {
  const labels = {
    dorsal: 'Dorsal (Shutdown)',
    sympathetic: 'Sympathetic (Fight/Flight)',
    ventral: 'Ventral (Social Engagement)',
  };
  return labels[state];
}

// Helper: Get layer configuration
function getLayerConfig(layerName: string) {
  const configs: Record<string, { icon: string; color: string; bgColor: string; description: string }> = {
    'Vokteren': {
      icon: '🛡️',
      color: '#FF6B6B',
      bgColor: '#FFE8E8',
      description: 'Hjernestamme - Fare-deteksjon og triagering',
    },
    'Føleren': {
      icon: '❤️',
      color: '#FF8C94',
      bgColor: '#FFE5E8',
      description: 'Limbisk System - Emosjonell vurdering',
    },
    'Gjenkjenneren': {
      icon: '🔍',
      color: '#A8DADC',
      bgColor: '#E8F4F5',
      description: 'Cerebellum - Mønstergjenkjenning',
    },
    'Utforskeren': {
      icon: '🧭',
      color: '#457B9D',
      bgColor: '#E3EEF3',
      description: 'Hippocampus - Kunnskapssøk',
    },
    'Strategen': {
      icon: '🧠',
      color: '#1D3557',
      bgColor: '#E5E9ED',
      description: 'Prefrontal Cortex - Strategisk planlegging',
    },
    'Integratoren': {
      icon: '✨',
      color: '#F1FAEE',
      bgColor: '#F8FCFB',
      description: 'Insula - Syntese av alle lag',
    },
  };
  
  return configs[layerName] || {
    icon: '❓',
    color: '#666',
    bgColor: '#f5f5f5',
    description: 'Ukjent lag',
  };
}

// Helper: Render layer summary
function renderLayerSummary(layer: LayerOutput): React.ReactNode {
  const { layer_name, data } = layer;

  switch (layer_name) {
    case 'Vokteren':
      return (
        <div>
          <p><strong>Fare detektert:</strong> {data.danger_detected ? '🚨 JA' : '✅ Nei'}</p>
          <p><strong>Triagering:</strong> {data.triage_level}</p>
          <p><strong>Kompleksitet:</strong> {(data.complexity * 100).toFixed(0)}%</p>
        </div>
      );
    
    case 'Føleren':
      return (
        <div>
          <p><strong>Primær følelse:</strong> {data.primary_emotion}</p>
          <p><strong>Polyvagal tilstand:</strong> {data.polyvagal_state}</p>
          <p><strong>Arousal:</strong> {(data.arousal_level * 100).toFixed(0)}%</p>
          <p><strong>Valens:</strong> {data.valence > 0 ? 'Positiv' : data.valence < 0 ? 'Negativ' : 'Nøytral'}</p>
        </div>
      );
    
    case 'Gjenkjenneren':
      return (
        <div>
          <p><strong>Mønster gjenkjent:</strong> {data.pattern_recognized ? '✅ Ja' : '❌ Nei'}</p>
          {data.pattern_recognized && (
            <>
              <p><strong>Mønster:</strong> {data.pattern_name.replace('_', ' ')}</p>
              <p><strong>Konfidensgrad:</strong> {(data.confidence * 100).toFixed(0)}%</p>
            </>
          )}
        </div>
      );
    
    case 'Utforskeren':
      return (
        <div>
          <p><strong>Ressurser funnet:</strong> {data.resources_found ? '✅ Ja' : '❌ Nei'}</p>
          {data.resources && data.resources.length > 0 && (
            <ul style={{ marginTop: '8px', paddingLeft: '20px' }}>
              {data.resources.slice(0, 3).map((resource: string, i: number) => (
                <li key={i} style={{ marginBottom: '4px' }}>{resource}</li>
              ))}
            </ul>
          )}
        </div>
      );
    
    case 'Strategen':
      return (
        <div>
          {data.action_plan && (
            <>
              <p><strong>Handlingsplan:</strong></p>
              <ul style={{ marginTop: '8px', paddingLeft: '20px' }}>
                {data.action_plan.slice(0, 3).map((step: string, i: number) => (
                  <li key={i} style={{ marginBottom: '4px' }}>{step}</li>
                ))}
              </ul>
            </>
          )}
        </div>
      );
    
    case 'Integratoren':
      return (
        <div>
          <p><strong>Lag brukt:</strong> {data.layers_used}/6</p>
          <p><strong>Syntese-strategi:</strong> {data.synthesis_strategy}</p>
        </div>
      );
    
    default:
      return <p>Ingen detaljer tilgjengelig</p>;
  }
}

