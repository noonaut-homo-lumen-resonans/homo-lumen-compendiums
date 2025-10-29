/**
 * Mobile Consultation Page
 *
 * Complete mobile consultation interface combining:
 * - Query submission panel
 * - Consultation history viewer
 *
 * This page can be used in:
 * - Mobile web browsers
 * - React Native WebView
 * - Standalone mobile apps
 */

import React, { useState } from 'react';
import { MobileQueryPanel } from '../components/MobileQueryPanel';
import { ConsultationHistory } from '../components/ConsultationHistory';

interface MobileConsultationPageProps {
  apiUrl?: string;
}

export const MobileConsultationPage: React.FC<MobileConsultationPageProps> = ({
  apiUrl = 'http://localhost:8000'
}) => {
  const [activeTab, setActiveTab] = useState<'query' | 'history'>('query');
  const [refreshHistory, setRefreshHistory] = useState(0);

  const handleConsultationStored = (consultationId: string) => {
    console.log('Consultation stored:', consultationId);
    // Refresh history view
    setRefreshHistory(prev => prev + 1);
    // Switch to history tab
    setTimeout(() => setActiveTab('history'), 1000);
  };

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: '#f5f5f5',
      fontFamily: 'system-ui, -apple-system, sans-serif'
    }}>
      {/* Header */}
      <header style={{
        backgroundColor: '#4CAF50',
        color: 'white',
        padding: '16px 20px',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
      }}>
        <h1 style={{
          margin: 0,
          fontSize: '20px',
          fontWeight: 600,
          textAlign: 'center'
        }}>
          🧬 GENOMOS Mobile
        </h1>
        <p style={{
          margin: '4px 0 0 0',
          fontSize: '12px',
          textAlign: 'center',
          opacity: 0.9
        }}>
          Homo Lumen AI Agent Consultations
        </p>
      </header>

      {/* Tab Navigation */}
      <div style={{
        display: 'flex',
        backgroundColor: 'white',
        borderBottom: '2px solid #e0e0e0',
        position: 'sticky',
        top: 0,
        zIndex: 100
      }}>
        <button
          onClick={() => setActiveTab('query')}
          style={{
            flex: 1,
            padding: '16px',
            fontSize: '16px',
            fontWeight: 600,
            color: activeTab === 'query' ? '#4CAF50' : '#666',
            backgroundColor: 'white',
            border: 'none',
            borderBottom: activeTab === 'query' ? '3px solid #4CAF50' : '3px solid transparent',
            cursor: 'pointer',
            transition: 'all 0.2s'
          }}
        >
          🤖 Ask Question
        </button>
        <button
          onClick={() => setActiveTab('history')}
          style={{
            flex: 1,
            padding: '16px',
            fontSize: '16px',
            fontWeight: 600,
            color: activeTab === 'history' ? '#4CAF50' : '#666',
            backgroundColor: 'white',
            border: 'none',
            borderBottom: activeTab === 'history' ? '3px solid #4CAF50' : '3px solid transparent',
            cursor: 'pointer',
            transition: 'all 0.2s'
          }}
        >
          📜 History
        </button>
      </div>

      {/* Main Content */}
      <main style={{ padding: '20px 0' }}>
        {activeTab === 'query' && (
          <MobileQueryPanel
            apiUrl={apiUrl}
            onConsultationStored={handleConsultationStored}
          />
        )}

        {activeTab === 'history' && (
          <ConsultationHistory
            key={refreshHistory} // Force refresh when new consultation added
            apiUrl={apiUrl}
            limit={20}
          />
        )}
      </main>

      {/* Footer */}
      <footer style={{
        padding: '20px',
        textAlign: 'center',
        fontSize: '12px',
        color: '#999',
        borderTop: '1px solid #e0e0e0'
      }}>
        <p style={{ margin: '0 0 8px 0' }}>
          Powered by GENOMOS Blockchain
        </p>
        <p style={{ margin: 0 }}>
          Every consultation is immutably recorded for future generations
        </p>
      </footer>
    </div>
  );
};

export default MobileConsultationPage;
