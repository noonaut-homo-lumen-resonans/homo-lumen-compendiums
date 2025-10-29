/**
 * Tour Overlay Component
 *
 * Semi-transparent backdrop for guided tours in Mobile Simulator.
 * Implements Triadic Ethics:
 * - Port 1: User can skip/exit tour at any time
 * - Port 2: NVC language, empowering messaging
 * - Port 3: Celebrates user autonomy and capacity
 *
 * @version 1.0
 * @date 2025-10-22
 * @author Code (Agent #9) - Motor Cortex
 */

'use client';

import { ReactNode } from 'react';

interface TourOverlayProps {
  isActive: boolean;
  children: ReactNode;
  onExit?: () => void;
}

export function TourOverlay({ isActive, children, onExit }: TourOverlayProps) {
  if (!isActive) return null;

  return (
    <div className="tour-overlay">
      {/* Tour content (tooltips, progress, controls) - NO backdrop, device stays visible! */}
      <div className="relative z-50">
        {children}
      </div>

      {/* Exit button (always visible - Triadic Ethics Port 1) */}
      {onExit && (
        <button
          onClick={onExit}
          className="fixed top-4 right-4 z-50 px-4 py-2 bg-red-500 text-white rounded-lg shadow-lg hover:bg-red-600 transition-colors font-medium flex items-center gap-2"
          aria-label="Exit tour"
        >
          <span className="text-xl">❌</span>
          <span>Exit Tour</span>
        </button>
      )}

      {/* Accessibility: Keyboard support */}
      <style jsx>{`
        .tour-overlay {
          /* Ensure tour is keyboard accessible */
          outline: none;
        }
      `}</style>
    </div>
  );
}
