/**
 * QDA v2.0 - Demo Dashboard Page
 * 
 * Demonstrates the LayerVisualization component with sample data
 * 
 * @version 2.0
 * @date 2025-10-20
 */

'use client';

import React, { useState } from 'react';
import { LayerVisualization } from '@/components/qda/LayerVisualization';
import type { QDAResponse } from '@/lib/qda';

export default function QDADemoPage() {
  const [testMessage, setTestMessage] = useState('Jeg føler meg veldig stresset på jobb');
  const [qdaResponse, setQdaResponse] = useState<QDAResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [showDebugInfo, setShowDebugInfo] = useState(false);

  const testQDA = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('/api/qda/respond', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: testMessage,
          context: {
            quadrant: 'høy-energi-negativt',
            emotion: 'stresset',
            pressureSignals: ['hodepine', 'muskelspenning'],
          },
          userState: {
            stressLevel: 7,
            polyvagalState: 'sympathetic',
            arousal: 0.8,
            valence: -0.4,
          },
        }),
      });

      const data = await response.json();
      setQdaResponse({
        final_response: data.response,
        layers: data.layers,
        highest_layer_used: data.highest_layer_used,
        total_cost: data.total_cost,
        total_time: data.total_time,
        complexity_score: data.complexity_score,
        polyvagal_state: data.polyvagal_state,
      });
    } catch (error) {
      console.error('Error testing QDA:', error);
      alert('Error testing QDA. See console for details.');
    } finally {
      setIsLoading(false);
    }
  };

  const testScenarios = [
    {
      name: 'Simple Query',
      message: 'Hei, hvordan har du det?',
      stressLevel: 3,
    },
    {
      name: 'Moderate (Job Stress)',
      message: 'Jeg føler meg veldig stresset på jobb. Sjefen min er så krevende.',
      stressLevel: 7,
    },
    {
      name: 'Critical (Danger)',
      message: 'Jeg orker ikke mer. Jeg har tenkt på selvmord.',
      stressLevel: 10,
    },
  ];

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#000', color: '#fff', padding: '40px' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        {/* Header */}
        <div style={{ marginBottom: '40px' }}>
          <h1 style={{ fontSize: '32px', fontWeight: 'bold', marginBottom: '8px' }}>
            QDA v2.0 Demo Dashboard
          </h1>
          <p style={{ fontSize: '16px', color: '#aaa' }}>
            Test the Neocortical Ascent Model with different scenarios
          </p>
        </div>

        {/* Test Input */}
        <div style={{ 
          backgroundColor: '#1a1a1a', 
          padding: '24px', 
          borderRadius: '12px', 
          marginBottom: '24px',
          border: '1px solid #333'
        }}>
          <h2 style={{ fontSize: '20px', fontWeight: 'bold', marginBottom: '16px' }}>
            Test Query
          </h2>
          
          {/* Quick Scenarios */}
          <div style={{ display: 'flex', gap: '12px', marginBottom: '16px', flexWrap: 'wrap' }}>
            {testScenarios.map((scenario) => (
              <button
                key={scenario.name}
                onClick={() => setTestMessage(scenario.message)}
                style={{
                  backgroundColor: '#333',
                  color: '#fff',
                  padding: '8px 16px',
                  borderRadius: '8px',
                  border: 'none',
                  cursor: 'pointer',
                  fontSize: '14px',
                }}
              >
                {scenario.name}
              </button>
            ))}
          </div>

          {/* Message Input */}
          <textarea
            value={testMessage}
            onChange={(e) => setTestMessage(e.target.value)}
            placeholder="Enter a message to test..."
            style={{
              width: '100%',
              minHeight: '100px',
              backgroundColor: '#000',
              color: '#fff',
              border: '1px solid #333',
              borderRadius: '8px',
              padding: '12px',
              fontSize: '14px',
              fontFamily: 'monospace',
              marginBottom: '16px',
              resize: 'vertical',
            }}
          />

          {/* Controls */}
          <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
            <button
              onClick={testQDA}
              disabled={isLoading || !testMessage.trim()}
              style={{
                backgroundColor: isLoading ? '#555' : '#4CAF50',
                color: '#fff',
                padding: '12px 24px',
                borderRadius: '8px',
                border: 'none',
                cursor: isLoading ? 'not-allowed' : 'pointer',
                fontSize: '16px',
                fontWeight: 'bold',
              }}
            >
              {isLoading ? 'Processing...' : 'Test QDA'}
            </button>

            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '14px', color: '#aaa' }}>
              <input
                type="checkbox"
                checked={showDebugInfo}
                onChange={(e) => setShowDebugInfo(e.target.checked)}
              />
              Show Debug Info
            </label>
          </div>
        </div>

        {/* Response */}
        {qdaResponse && (
          <div style={{ marginBottom: '24px' }}>
            {/* Final Response */}
            <div style={{ 
              backgroundColor: '#1a1a1a', 
              padding: '24px', 
              borderRadius: '12px', 
              marginBottom: '24px',
              border: '1px solid #333'
            }}>
              <h2 style={{ fontSize: '20px', fontWeight: 'bold', marginBottom: '16px' }}>
                Lira's Response
              </h2>
              <div style={{ 
                fontSize: '16px', 
                lineHeight: '1.6', 
                color: '#ddd',
                whiteSpace: 'pre-wrap'
              }}>
                {qdaResponse.final_response}
              </div>
            </div>

            {/* Layer Visualization */}
            <LayerVisualization 
              response={qdaResponse} 
              showDebugInfo={showDebugInfo}
            />
          </div>
        )}

        {/* Instructions */}
        {!qdaResponse && (
          <div style={{ 
            backgroundColor: '#1a1a1a', 
            padding: '24px', 
            borderRadius: '12px',
            border: '1px solid #333'
          }}>
            <h2 style={{ fontSize: '20px', fontWeight: 'bold', marginBottom: '16px' }}>
              How to Use
            </h2>
            <ol style={{ paddingLeft: '20px', color: '#aaa', lineHeight: '1.8' }}>
              <li>Click one of the quick scenario buttons or type your own message</li>
              <li>Click "Test QDA" to process the message through all 6 layers</li>
              <li>View Lira's response and the layer breakdown</li>
              <li>Click on each layer to see detailed information</li>
              <li>Enable "Show Debug Info" to see raw layer data</li>
            </ol>
          </div>
        )}
      </div>
    </div>
  );
}

