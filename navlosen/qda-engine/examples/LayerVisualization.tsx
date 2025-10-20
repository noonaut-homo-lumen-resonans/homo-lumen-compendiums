/**
 * LayerVisualization Component - QDA v2.0 Dashboard
 *
 * Copy to: web-console/components/qda/LayerVisualization.tsx
 *
 * Shows all 6 neurobiological layers with polyvagal-adaptive styling
 *
 * @version 2.0
 * @date 2025-10-20
 */

import React, { useState } from 'react';

// Types (should match neurobiological-qda.ts)
interface LayerOutput {
  layer_name: string;
  icon: string;
  data: any;
  processing_time: number;
  cost: number;
  timestamp: number;
}

interface QDAResponse {
  final_response: string;
  layers: LayerOutput[];
  highest_layer_used: string;
  total_cost: number;
  total_time: number;
  complexity_score: number;
}

interface Props {
  response: QDAResponse;
  polyvagalState?: 'dorsal' | 'sympathetic' | 'ventral';
  showDebugInfo?: boolean;
}

export const LayerVisualization: React.FC<Props> = ({
  response,
  polyvagalState = 'sympathetic',
  showDebugInfo = false,
}) => {
  const [expandedLayers, setExpandedLayers] = useState<Set<string>>(
    new Set(['Integratoren']) // Auto-expand final layer
  );

  // Polyvagal-adaptive colors
  const stateColors = {
    dorsal: {
      primary: '#4CAF50',
      bg: '#E8F5E9',
      text: '#2E7D32',
      description: 'Shutdown/Immobilisert - Systemet bruker kun essensielle lag',
    },
    sympathetic: {
      primary: '#FF9800',
      bg: '#FFF3E0',
      text: '#E65100',
      description: 'Fight/Flight - Systemet balanserer hastighet og nøyaktighet',
    },
    ventral: {
      primary: '#2196F3',
      bg: '#E3F2FD',
      text: '#1565C0',
      description: 'Sosialt Engasjert - Systemet kan bruke alle lag for best resultat',
    },
  };

  const colors = stateColors[polyvagalState];

  // Layer colors (semantic)
  const layerColors: Record<string, string> = {
    Vokteren: '#FF6B6B', // Red (alert/safety)
    Føleren: '#FF8C94', // Pink (emotion)
    Gjenkjenneren: '#A8DADC', // Teal (pattern)
    Utforskeren: '#457B9D', // Blue (knowledge)
    Strategen: '#1D3557', // Dark blue (strategy)
    Integratoren: '#F1FAEE', // Light (synthesis)
  };

  // Toggle layer expansion
  const toggleLayer = (layerName: string) => {
    setExpandedLayers(prev => {
      const next = new Set(prev);
      if (next.has(layerName)) {
        next.delete(layerName);
      } else {
        next.add(layerName);
      }
      return next;
    });
  };

  // Get layer summary for collapsed view
  const getLayerSummary = (layer: LayerOutput): string => {
    switch (layer.layer_name) {
      case 'Vokteren':
        return `${layer.data.complexity} query (trygt: ${layer.data.safe ? '✓' : '✗'})`;
      case 'Føleren':
        return `${layer.data.polyvagal_state} state, følelse: ${layer.data.primary_emotion}`;
      case 'Gjenkjenneren':
        return layer.data.recognized
          ? `Mønster: ${layer.data.pattern} (${(layer.data.confidence * 100).toFixed(0)}%)`
          : 'Ingen mønster gjenkjent';
      case 'Utforskeren':
        return layer.data.activated
          ? `Fant ${layer.data.resources?.length ?? 0} ressurser`
          : 'Ikke aktivert (høy pattern confidence)';
      case 'Strategen':
        return layer.data.activated
          ? `${layer.data.action_steps?.length ?? 0}-stegs plan`
          : 'Ikke aktivert (lav kompleksitet)';
      case 'Integratoren':
        return `${layer.data.layers_used} lag syntetisert`;
      default:
        return '';
    }
  };

  return (
    <div
      style={{
        backgroundColor: colors.bg,
        border: `2px solid ${colors.primary}`,
        borderRadius: '12px',
        padding: '20px',
        marginBottom: '16px',
      }}
    >
      {/* Header */}
      <div style={{ marginBottom: '16px' }}>
        <h2 style={{ margin: 0, color: colors.text, fontSize: '24px', fontWeight: 'bold' }}>
          🧠 Nevrobiologisk Prosessering
        </h2>
        <p style={{ margin: '8px 0 0 0', color: colors.text, fontSize: '14px' }}>
          {colors.description}
        </p>
      </div>

      {/* Polyvagal State Badge */}
      <div
        style={{
          display: 'inline-block',
          backgroundColor: colors.primary,
          color: 'white',
          padding: '6px 12px',
          borderRadius: '6px',
          fontSize: '14px',
          fontWeight: 'bold',
          marginBottom: '16px',
        }}
      >
        Tilstand: {polyvagalState.toUpperCase()}
      </div>

      {/* Layers */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {response.layers.map((layer, index) => {
          const isExpanded = expandedLayers.has(layer.layer_name);
          const layerColor = layerColors[layer.layer_name] || '#CCCCCC';

          return (
            <div
              key={layer.layer_name}
              style={{
                borderLeft: `6px solid ${layerColor}`,
                backgroundColor: 'white',
                borderRadius: '8px',
                padding: '16px',
                cursor: 'pointer',
                transition: 'box-shadow 0.2s',
              }}
              onClick={() => toggleLayer(layer.layer_name)}
              onMouseEnter={(e) => {
                e.currentTarget.style.boxShadow = '0 4px 12px rgba(0,0,0,0.1)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.boxShadow = 'none';
              }}
            >
              {/* Layer Header */}
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <span style={{ fontSize: '32px' }}>{layer.icon}</span>
                  <div>
                    <div style={{ fontWeight: 'bold', fontSize: '18px', color: '#333' }}>
                      Lag {index + 1}: {layer.layer_name}
                    </div>
                    <div style={{ fontSize: '14px', color: '#666', marginTop: '4px' }}>
                      {getLayerSummary(layer)}
                    </div>
                  </div>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontSize: '12px', color: '#999' }}>
                    {layer.processing_time}ms
                  </div>
                  {showDebugInfo && (
                    <div style={{ fontSize: '12px', color: '#999' }}>
                      ${layer.cost.toFixed(5)}
                    </div>
                  )}
                </div>
              </div>

              {/* Layer Details (Expanded) */}
              {isExpanded && (
                <div
                  style={{
                    marginTop: '16px',
                    paddingTop: '16px',
                    borderTop: '1px solid #E0E0E0',
                  }}
                >
                  {renderLayerDetails(layer)}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Summary */}
      <div
        style={{
          marginTop: '20px',
          padding: '16px',
          backgroundColor: 'white',
          borderRadius: '8px',
          border: '1px solid #E0E0E0',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
          <span style={{ fontWeight: 'bold', color: '#333' }}>Høyeste lag brukt:</span>
          <span style={{ color: '#666' }}>{response.highest_layer_used}</span>
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
          <span style={{ fontWeight: 'bold', color: '#333' }}>Total prosesseringstid:</span>
          <span style={{ color: '#666' }}>{response.total_time}ms</span>
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
          <span style={{ fontWeight: 'bold', color: '#333' }}>Kompleksitet:</span>
          <span style={{ color: '#666' }}>
            {(response.complexity_score * 100).toFixed(0)}%
          </span>
        </div>
        {showDebugInfo && (
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span style={{ fontWeight: 'bold', color: '#333' }}>Total kostnad:</span>
            <span style={{ color: '#666' }}>${response.total_cost.toFixed(5)}</span>
          </div>
        )}
      </div>

      {/* Final Response */}
      <div
        style={{
          marginTop: '20px',
          padding: '20px',
          backgroundColor: 'white',
          borderRadius: '8px',
          border: `2px solid ${colors.primary}`,
        }}
      >
        <div style={{ fontWeight: 'bold', color: colors.text, marginBottom: '12px', fontSize: '18px' }}>
          ✨ Integrert Respons
        </div>
        <div style={{ color: '#333', fontSize: '16px', lineHeight: '1.6', whiteSpace: 'pre-wrap' }}>
          {response.final_response}
        </div>
      </div>
    </div>
  );
};

/**
 * Render layer-specific details
 */
function renderLayerDetails(layer: LayerOutput): React.ReactNode {
  switch (layer.layer_name) {
    case 'Vokteren':
      return (
        <div>
          <DetailRow label="Danger Level" value={layer.data.danger_level} />
          <DetailRow label="Complexity" value={layer.data.complexity} />
          <DetailRow label="Urgency" value={(layer.data.urgency * 100).toFixed(0) + '%'} />
          <DetailRow
            label="Safe to Proceed"
            value={layer.data.safe ? '✓ Yes' : '✗ No'}
          />
          {layer.data.escalation_needed && (
            <div style={{ marginTop: '8px', padding: '12px', backgroundColor: '#FFEBEE', borderRadius: '4px' }}>
              <strong>⚠️ Escalation Needed:</strong> {layer.data.message}
            </div>
          )}
        </div>
      );

    case 'Føleren':
      return (
        <div>
          <DetailRow label="Primary Emotion" value={layer.data.primary_emotion} />
          <DetailRow label="Polyvagal State" value={layer.data.polyvagal_state} />
          <DetailRow label="Arousal" value={(layer.data.arousal * 100).toFixed(0) + '%'} />
          <DetailRow label="Valence" value={layer.data.valence.toFixed(2)} />
          <DetailRow label="Stress Level" value={layer.data.stress_level + '/10'} />
          <div style={{ marginTop: '8px', fontStyle: 'italic', color: '#666' }}>
            {layer.data.emotional_summary}
          </div>
        </div>
      );

    case 'Gjenkjenneren':
      return (
        <div>
          <DetailRow label="Pattern" value={layer.data.pattern} />
          <DetailRow label="Confidence" value={(layer.data.confidence * 100).toFixed(0) + '%'} />
          <DetailRow
            label="Recognized"
            value={layer.data.recognized ? '✓ Yes' : '✗ No'}
          />
          {layer.data.typical_response && (
            <div style={{ marginTop: '8px', fontStyle: 'italic', color: '#666' }}>
              Typical Response: {layer.data.typical_response}
            </div>
          )}
        </div>
      );

    case 'Utforskeren':
      return (
        <div>
          <DetailRow
            label="Activated"
            value={layer.data.activated ? '✓ Yes' : '✗ No'}
          />
          {layer.data.activated && (
            <>
              <DetailRow label="Pattern Explored" value={layer.data.pattern_explored} />
              <DetailRow
                label="Resources Found"
                value={layer.data.resources?.length ?? 0}
              />
              {layer.data.resources && layer.data.resources.length > 0 && (
                <div style={{ marginTop: '8px' }}>
                  <strong>Resources:</strong>
                  <ul style={{ margin: '4px 0 0 20px', padding: 0 }}>
                    {layer.data.resources.map((resource: string, i: number) => (
                      <li key={i} style={{ marginBottom: '4px' }}>
                        {resource}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </>
          )}
          {!layer.data.activated && (
            <div style={{ marginTop: '8px', fontStyle: 'italic', color: '#666' }}>
              {layer.data.reason}
            </div>
          )}
        </div>
      );

    case 'Strategen':
      return (
        <div>
          <DetailRow
            label="Activated"
            value={layer.data.activated ? '✓ Yes' : '✗ No'}
          />
          {layer.data.activated && (
            <>
              <DetailRow
                label="Complexity Score"
                value={(layer.data.complexity_score * 100).toFixed(0) + '%'}
              />
              {layer.data.action_steps && layer.data.action_steps.length > 0 && (
                <div style={{ marginTop: '8px' }}>
                  <strong>Action Steps:</strong>
                  <ol style={{ margin: '4px 0 0 20px', padding: 0 }}>
                    {layer.data.action_steps.map((step: string, i: number) => (
                      <li key={i} style={{ marginBottom: '4px' }}>
                        {step}
                      </li>
                    ))}
                  </ol>
                </div>
              )}
            </>
          )}
          {!layer.data.activated && (
            <div style={{ marginTop: '8px', fontStyle: 'italic', color: '#666' }}>
              {layer.data.reason}
            </div>
          )}
        </div>
      );

    case 'Integratoren':
      return (
        <div>
          <DetailRow label="Synthesis Strategy" value={layer.data.synthesis_strategy} />
          <DetailRow label="Layers Used" value={layer.data.layers_used} />
          <div style={{ marginTop: '12px', padding: '12px', backgroundColor: '#F5F5F5', borderRadius: '4px' }}>
            <strong>Response Preview:</strong>
            <div style={{ marginTop: '8px', fontSize: '14px', lineHeight: '1.5' }}>
              {layer.data.response_text.substring(0, 200)}
              {layer.data.response_text.length > 200 && '...'}
            </div>
          </div>
        </div>
      );

    default:
      return (
        <pre style={{ fontSize: '12px', overflow: 'auto', backgroundColor: '#F5F5F5', padding: '8px', borderRadius: '4px' }}>
          {JSON.stringify(layer.data, null, 2)}
        </pre>
      );
  }
}

/**
 * Helper: Detail row component
 */
function DetailRow({ label, value }: { label: string; value: any }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
      <span style={{ fontWeight: 'bold', color: '#555' }}>{label}:</span>
      <span style={{ color: '#333' }}>{value}</span>
    </div>
  );
}

export default LayerVisualization;
