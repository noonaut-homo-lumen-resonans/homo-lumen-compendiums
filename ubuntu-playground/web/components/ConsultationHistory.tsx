/**
 * Consultation History Component
 *
 * Mobile-friendly component for viewing past consultations from
 * the GENOMOS blockchain.
 *
 * Usage:
 *   <ConsultationHistory apiUrl="http://localhost:8000" limit={10} />
 */

import React, { useState, useEffect } from 'react';

interface Consultation {
  consultation_id: string;
  block_index: number;
  human_query: string;
  agent_count: number;
  synthesis_summary: string | null;
  related_smk: string[];
  has_biofelt_context: boolean;
  has_thalos_validation: boolean;
  timestamp: string;
  hash: string;
}

interface ConsultationHistoryProps {
  apiUrl: string;
  limit?: number;
  searchQuery?: string;
}

export const ConsultationHistory: React.FC<ConsultationHistoryProps> = ({
  apiUrl,
  limit = 20,
  searchQuery
}) => {
  const [consultations, setConsultations] = useState<Consultation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedConsultation, setSelectedConsultation] = useState<string | null>(null);
  const [detailedData, setDetailedData] = useState<any>(null);

  useEffect(() => {
    fetchConsultations();
  }, [apiUrl, limit, searchQuery]);

  const fetchConsultations = async () => {
    setLoading(true);
    setError(null);

    try {
      let url = `${apiUrl}/api/dna/consultations?limit=${limit}`;
      if (searchQuery) {
        url += `&query=${encodeURIComponent(searchQuery)}`;
      }

      const response = await fetch(url);

      if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`);
      }

      const data = await response.json();
      setConsultations(data);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch consultations');
      console.error('Fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchConsultationDetails = async (consultationId: string) => {
    try {
      const response = await fetch(`${apiUrl}/api/dna/consultations/${consultationId}`);

      if (!response.ok) {
        throw new Error(`Failed to fetch details: ${response.statusText}`);
      }

      const data = await response.json();
      setDetailedData(data);
      setSelectedConsultation(consultationId);
    } catch (err: any) {
      console.error('Details fetch error:', err);
      alert(`Failed to load details: ${err.message}`);
    }
  };

  const formatTimestamp = (timestamp: string): string => {
    try {
      const date = new Date(timestamp);
      const now = new Date();
      const diffMs = now.getTime() - date.getTime();
      const diffMins = Math.floor(diffMs / 60000);
      const diffHours = Math.floor(diffMs / 3600000);
      const diffDays = Math.floor(diffMs / 86400000);

      if (diffMins < 1) return 'Just now';
      if (diffMins < 60) return `${diffMins}m ago`;
      if (diffHours < 24) return `${diffHours}h ago`;
      if (diffDays < 7) return `${diffDays}d ago`;
      return date.toLocaleDateString();
    } catch {
      return timestamp;
    }
  };

  if (loading) {
    return (
      <div style={{
        textAlign: 'center',
        padding: '40px',
        color: '#666'
      }}>
        <div style={{ fontSize: '24px', marginBottom: '10px' }}>⏳</div>
        <div>Loading consultations...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{
        padding: '20px',
        backgroundColor: '#ffebee',
        border: '2px solid #f44336',
        borderRadius: '8px',
        color: '#c62828'
      }}>
        ❌ {error}
      </div>
    );
  }

  return (
    <div style={{
      maxWidth: '800px',
      margin: '0 auto',
      padding: '20px',
      fontFamily: 'system-ui, -apple-system, sans-serif'
    }}>
      <h2 style={{ textAlign: 'center', marginBottom: '20px' }}>
        📜 Consultation History
      </h2>

      {/* Stats Bar */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-around',
        marginBottom: '20px',
        padding: '16px',
        backgroundColor: '#f5f5f5',
        borderRadius: '8px'
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '24px', fontWeight: 600, color: '#4CAF50' }}>
            {consultations.length}
          </div>
          <div style={{ fontSize: '12px', color: '#666' }}>Consultations</div>
        </div>
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '24px', fontWeight: 600, color: '#2196F3' }}>
            {consultations.reduce((sum, c) => sum + c.agent_count, 0)}
          </div>
          <div style={{ fontSize: '12px', color: '#666' }}>Agent Responses</div>
        </div>
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '24px', fontWeight: 600, color: '#FF9800' }}>
            {new Set(consultations.flatMap(c => c.related_smk)).size}
          </div>
          <div style={{ fontSize: '12px', color: '#666' }}>SMK References</div>
        </div>
      </div>

      {/* Consultation List */}
      {consultations.length === 0 ? (
        <div style={{
          textAlign: 'center',
          padding: '40px',
          color: '#999'
        }}>
          <div style={{ fontSize: '48px', marginBottom: '10px' }}>📭</div>
          <div>No consultations found</div>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {consultations.map(consultation => (
            <div
              key={consultation.consultation_id}
              onClick={() => fetchConsultationDetails(consultation.consultation_id)}
              style={{
                padding: '16px',
                backgroundColor: 'white',
                border: selectedConsultation === consultation.consultation_id
                  ? '2px solid #4CAF50'
                  : '2px solid #e0e0e0',
                borderRadius: '12px',
                cursor: 'pointer',
                transition: 'all 0.2s',
                boxShadow: selectedConsultation === consultation.consultation_id
                  ? '0 4px 12px rgba(76, 175, 80, 0.2)'
                  : '0 2px 4px rgba(0,0,0,0.1)'
              }}
            >
              {/* Header */}
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: '10px'
              }}>
                <span style={{
                  fontSize: '12px',
                  fontWeight: 600,
                  color: '#666',
                  backgroundColor: '#f5f5f5',
                  padding: '4px 8px',
                  borderRadius: '4px'
                }}>
                  Block #{consultation.block_index}
                </span>
                <span style={{ fontSize: '12px', color: '#999' }}>
                  {formatTimestamp(consultation.timestamp)}
                </span>
              </div>

              {/* Question */}
              <div style={{
                fontSize: '16px',
                fontWeight: 500,
                marginBottom: '12px',
                color: '#333',
                lineHeight: '1.5'
              }}>
                {consultation.human_query.length > 150
                  ? consultation.human_query.substring(0, 150) + '...'
                  : consultation.human_query}
              </div>

              {/* Metadata */}
              <div style={{
                display: 'flex',
                flexWrap: 'wrap',
                gap: '8px',
                fontSize: '12px'
              }}>
                <span style={{
                  padding: '4px 8px',
                  borderRadius: '12px',
                  backgroundColor: '#e3f2fd',
                  color: '#1976d2'
                }}>
                  👥 {consultation.agent_count} agents
                </span>

                {consultation.related_smk.length > 0 && (
                  <span style={{
                    padding: '4px 8px',
                    borderRadius: '12px',
                    backgroundColor: '#fff3e0',
                    color: '#f57c00'
                  }}>
                    📚 {consultation.related_smk.length} SMK refs
                  </span>
                )}

                {consultation.has_biofelt_context && (
                  <span style={{
                    padding: '4px 8px',
                    borderRadius: '12px',
                    backgroundColor: '#f3e5f5',
                    color: '#7b1fa2'
                  }}>
                    💗 Biofelt
                  </span>
                )}

                {consultation.has_thalos_validation && (
                  <span style={{
                    padding: '4px 8px',
                    borderRadius: '12px',
                    backgroundColor: '#e8f5e9',
                    color: '#388e3c'
                  }}>
                    ✓ Thalos
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Detailed View Modal */}
      {selectedConsultation && detailedData && (
        <div
          onClick={() => {
            setSelectedConsultation(null);
            setDetailedData(null);
          }}
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0,0,0,0.5)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000,
            padding: '20px'
          }}
        >
          <div
            onClick={(e) => e.stopPropagation()}
            style={{
              backgroundColor: 'white',
              borderRadius: '12px',
              padding: '24px',
              maxWidth: '600px',
              maxHeight: '80vh',
              overflow: 'auto',
              boxShadow: '0 8px 32px rgba(0,0,0,0.2)'
            }}
          >
            <h3 style={{ marginTop: 0 }}>
              Consultation Details
            </h3>

            <div style={{ marginBottom: '16px' }}>
              <strong>Question:</strong>
              <p style={{ margin: '8px 0', lineHeight: '1.6' }}>
                {detailedData.human_query}
              </p>
            </div>

            {detailedData.synthesis?.summary && (
              <div style={{ marginBottom: '16px' }}>
                <strong>Synthesis:</strong>
                <p style={{ margin: '8px 0', lineHeight: '1.6' }}>
                  {detailedData.synthesis.summary}
                </p>
              </div>
            )}

            {detailedData.synthesis?.related_smk?.length > 0 && (
              <div style={{ marginBottom: '16px' }}>
                <strong>Related SMKs:</strong>
                <div style={{ marginTop: '8px', display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                  {detailedData.synthesis.related_smk.map((smk: string) => (
                    <span
                      key={smk}
                      style={{
                        padding: '6px 12px',
                        borderRadius: '16px',
                        backgroundColor: '#FF9800',
                        color: 'white',
                        fontSize: '12px',
                        fontWeight: 600
                      }}
                    >
                      {smk}
                    </span>
                  ))}
                </div>
              </div>
            )}

            <div style={{
              marginTop: '20px',
              padding: '12px',
              backgroundColor: '#f5f5f5',
              borderRadius: '8px',
              fontSize: '12px',
              color: '#666'
            }}>
              <p style={{ margin: '4px 0' }}>
                <strong>Block:</strong> #{detailedData.block_index}
              </p>
              <p style={{ margin: '4px 0' }}>
                <strong>Hash:</strong> {detailedData.hash.substring(0, 16)}...
              </p>
            </div>

            <button
              onClick={() => {
                setSelectedConsultation(null);
                setDetailedData(null);
              }}
              style={{
                marginTop: '20px',
                width: '100%',
                padding: '12px',
                backgroundColor: '#4CAF50',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                fontSize: '16px',
                fontWeight: 600,
                cursor: 'pointer'
              }}
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ConsultationHistory;
