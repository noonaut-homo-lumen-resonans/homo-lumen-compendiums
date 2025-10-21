/**
 * Mobile Simulator - Interactive Demo Platform
 *
 * Extended mobile simulator for Innovation Norge stakeholder demos.
 * Shows NAV-Losen frontend in realistic mobile frames with guided tours,
 * annotations, analytics, and screen recording.
 *
 * @version 1.1
 * @date 2025-10-21
 * @author Code (Agent #9) - Motor Cortex / Cerebellum
 * @timeline Dag 1/7 - Production URL Integration
 */

'use client';

import { useState } from 'react';
import { DeviceFrame } from '@/components/simulator/DeviceFrame';
import { ControlsPanel } from '@/components/simulator/ControlsPanel';
import type { Metadata } from 'next';

export default function MobileSimulatorPage() {
  const [deviceType, setDeviceType] = useState<'iphone' | 'samsung' | 'ipad'>('iphone');
  const [currentPage, setCurrentPage] = useState('/mestring');
  const [guidedTourActive, setGuidedTourActive] = useState(false);
  const [recordingActive, setRecordingActive] = useState(false);

  // Frontend URL - Netlify production (deployed by Manus 21.10.2025)
  const frontendBaseUrl = process.env.NEXT_PUBLIC_FRONTEND_URL || 'https://navlosen-frontend.netlify.app';
  const iframeSrc = `${frontendBaseUrl}${currentPage}`;

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-100 via-gray-50 to-blue-50 py-8 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            NAV-Losen Mobile Simulator
          </h1>
          <p className="text-lg text-gray-600">
            Interactive Demo Platform for Innovation Norge & NAV Tvedestrand
          </p>
        </div>

        {/* Controls Panel */}
        <ControlsPanel
          deviceType={deviceType}
          onDeviceChange={setDeviceType}
          currentPage={currentPage}
          onPageChange={setCurrentPage}
          guidedTourActive={guidedTourActive}
          onGuidedTourToggle={() => setGuidedTourActive(!guidedTourActive)}
          recordingActive={recordingActive}
          onRecordingToggle={() => setRecordingActive(!recordingActive)}
        />

        {/* Device Frame with iframe */}
        <DeviceFrame
          deviceType={deviceType}
          iframeSrc={iframeSrc}
        />

        {/* Footer Info */}
        <div className="mt-8 text-center text-sm text-gray-500">
          <p>
            Powered by QDA v2.0 • 14+ Pages • Polyvagal-Adaptive Design
          </p>
          <p className="mt-2">
            Timeline: Dag 1/7 • Status: Device Frame & Navigation ✅
          </p>
        </div>
      </div>
    </div>
  );
}
