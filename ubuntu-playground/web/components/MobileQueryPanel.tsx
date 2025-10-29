/**
 * Mobile Query Panel Component
 *
 * Simple mobile-friendly component for submitting questions to GENOMOS
 * consultations and receiving AI-agent responses.
 *
 * Usage:
 *   <MobileQueryPanel apiUrl="http://localhost:8000" />
 */

import React, { useState } from 'react';

interface Agent {
  name: string;
  color: string;
}

const AVAILABLE_AGENTS: Agent[] = [
  { name: 'manus', color: '#4CAF50' },
  { name: 'lira', color: '#2196F3' },
  { name: 'orion', color: '#FF9800' },
  { name: 'aurora', color: '#9C27B0' },
  { name: 'zara', color: '#F44336' },
];

interface MobileQueryPanelProps {
  apiUrl: string;
  onConsultationStored?: (consultationId: string) => void;
}

export const MobileQueryPanel: React.FC<MobileQueryPanelProps> = ({
  apiUrl,
  onConsultationStored
}) => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [response, setResponse] = useState<any>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!query.trim()) {
      setError('Please enter a question');
      return;
    }

    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      // Generate unique consultation ID
      const consultationId = `CONS_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

      // Simulate agent responses (in production, this would call actual agents)
      const agentResponses: Record<string, any> = {};
      for (const agent of AVAILABLE_AGENTS) {
        agentResponses[agent.name] = {
          response: `Response from ${agent.name} regarding: "${query}"`,
          confidence: 0.85 + Math.random() * 0.15,
          processing_time_ms: Math.floor(Math.random() * 500) + 100
        };
      }

      // Create synthesis
      const synthesis = {
        summary: `This question relates to multiple aspects of the Homo Lumen system.`,
        key_insights: [
          'Agent perspectives aligned on core principles',
          'Multiple knowledge domains engaged'
        ],
        related_smk: [] // SMK references auto-detected by backend
      };

      // Store consultation via API
      const storeResponse = await fetch(`${apiUrl}/api/store-consultation`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          consultation_id: consultationId,
          human_query: query,
          agent_responses: agentResponses,
          synthesis: synthesis,
          timestamp: new Date().toISOString()
        })
      });

      if (!storeResponse.ok) {
        throw new Error(`API error: ${storeResponse.statusText}`);
      }

      const result = await storeResponse.json();
      setResponse(result);

      // Notify parent component
      if (onConsultationStored) {
        onConsultationStored(consultationId);
      }

      // Clear query on success
      setQuery('');
    } catch (err: any) {
      setError(err.message || 'Failed to submit consultation');
      console.error('Consultation error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      maxWidth: '600px',
      margin: '0 auto',
      padding: '20px',
      fontFamily: 'system-ui, -apple-system, sans-serif'
    }}>
      <h2 style={{ textAlign: 'center', marginBottom: '20px' }}>
        🤖 GENOMOS Mobile Q&A
      </h2>

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '15px' }}>
          <label htmlFor="query" style={{ display: 'block', marginBottom: '8px', fontWeight: 600 }}>
            Ask a Question:
          </label>
          <textarea
            id="query"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter your question here..."
            rows={4}
            disabled={loading}
            style={{
              width: '100%',
              padding: '12px',
              fontSize: '16px',
              borderRadius: '8px',
              border: '2px solid #ddd',
              resize: 'vertical',
              fontFamily: 'inherit'
            }}
          />
        </div>

        <button
          type="submit"
          disabled={loading || !query.trim()}
          style={{
            width: '100%',
            padding: '14px',
            fontSize: '16px',
            fontWeight: 600,
            color: 'white',
            backgroundColor: loading ? '#ccc' : '#4CAF50',
            border: 'none',
            borderRadius: '8px',
            cursor: loading ? 'not-allowed' : 'pointer',
            transition: 'background-color 0.2s'
          }}
        >
          {loading ? '⏳ Processing...' : '🚀 Submit Question'}
        </button>
      </form>

      {/* Error Display */}
      {error && (
        <div style={{
          marginTop: '20px',
          padding: '12px',
          backgroundColor: '#ffebee',
          border: '2px solid #f44336',
          borderRadius: '8px',
          color: '#c62828'
        }}>
          ❌ {error}
        </div>
      )}

      {/* Success Response */}
      {response && (
        <div style={{
          marginTop: '20px',
          padding: '16px',
          backgroundColor: '#e8f5e9',
          border: '2px solid #4CAF50',
          borderRadius: '8px'
        }}>
          <h3 style={{ marginTop: 0, color: '#2e7d32' }}>
            ✅ Consultation Stored Successfully
          </h3>
          <p style={{ margin: '10px 0' }}>
            <strong>Consultation ID:</strong> {response.consultation_id}
          </p>
          <p style={{ margin: '10px 0' }}>
            <strong>Blockchain Block:</strong> #{response.blockchain_block_index}
          </p>
          <p style={{ margin: '10px 0', fontSize: '14px', color: '#555' }}>
            📊 {response.message}
          </p>
        </div>
      )}

      {/* Agent Status Indicators */}
      <div style={{ marginTop: '30px' }}>
        <h3 style={{ fontSize: '14px', marginBottom: '10px', color: '#666' }}>
          Active Agents:
        </h3>
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
          {AVAILABLE_AGENTS.map(agent => (
            <span
              key={agent.name}
              style={{
                padding: '6px 12px',
                borderRadius: '16px',
                backgroundColor: agent.color,
                color: 'white',
                fontSize: '12px',
                fontWeight: 600
              }}
            >
              {agent.name}
            </span>
          ))}
        </div>
      </div>

      {/* Info Box */}
      <div style={{
        marginTop: '30px',
        padding: '16px',
        backgroundColor: '#f5f5f5',
        borderRadius: '8px',
        fontSize: '14px',
        color: '#666'
      }}>
        <p style={{ margin: '0 0 10px 0' }}>
          <strong>💡 About GENOMOS:</strong>
        </p>
        <p style={{ margin: 0 }}>
          Every consultation is permanently stored in the GENOMOS blockchain,
          creating an immutable record of knowledge evolution. Your questions
          contribute to the collective memory of the Homo Lumen system.
        </p>
      </div>
    </div>
  );
};

export default MobileQueryPanel;
