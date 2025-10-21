/**
 * Mobile Simulator - Interactive Demo Platform
 *
 * Extended mobile simulator for Innovation Norge stakeholder demos.
 * Shows NAV-Losen frontend in realistic mobile frames with guided tours,
 * annotations, analytics, and screen recording.
 *
 * @version 1.2
 * @date 2025-10-22
 * @author Code (Agent #9) - Motor Cortex / Cerebellum
 * @timeline Dag 3/7 - Guided Tours Integration
 */

'use client';

import { useState, useEffect } from 'react';
import { DeviceFrame } from '@/components/simulator/DeviceFrame';
import { ControlsPanel } from '@/components/simulator/ControlsPanel';
import { TourOverlay } from '@/components/simulator/TourOverlay';
import { TourTooltip } from '@/components/simulator/TourTooltip';
import { TourProgress } from '@/components/simulator/TourProgress';
import { TourController } from '@/components/simulator/TourController';
import { allTours, getTourById, type Tour } from '@/lib/tourScripts';
import type { Metadata } from 'next';

export default function MobileSimulatorPage() {
  const [deviceType, setDeviceType] = useState<'iphone' | 'samsung' | 'ipad'>('iphone');
  const [currentPage, setCurrentPage] = useState('/mestring');
  const [guidedTourActive, setGuidedTourActive] = useState(false);
  const [recordingActive, setRecordingActive] = useState(false);

  // Tour state
  const [activeTour, setActiveTour] = useState<Tour | null>(null);
  const [currentStep, setCurrentStep] = useState(1);
  const [isPlaying, setIsPlaying] = useState(false);
  const [showTourSelection, setShowTourSelection] = useState(false);

  // Frontend URL - Vercel production (deployed by Manus 21.10.2025)
  const frontendBaseUrl = process.env.NEXT_PUBLIC_FRONTEND_URL || 'https://navlosen-frontend.vercel.app';
  const iframeSrc = `${frontendBaseUrl}${currentPage}`;

  // Keyboard shortcuts (Triadic Ethics Port 1 - User Control)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!activeTour) return;

      switch (e.key) {
        case 'Escape':
          handleExitTour();
          break;
        case 'ArrowRight':
          handleNext();
          break;
        case 'ArrowLeft':
          handlePrevious();
          break;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [activeTour, currentStep]);

  // Auto-navigate to tour step's target page
  useEffect(() => {
    if (activeTour && activeTour.steps[currentStep - 1]) {
      const targetPage = activeTour.steps[currentStep - 1].targetPage;
      setCurrentPage(targetPage);
    }
  }, [activeTour, currentStep]);

  // Tour control handlers
  const handleStartTour = (tourId: string) => {
    const tour = getTourById(tourId);
    if (tour) {
      setActiveTour(tour);
      setCurrentStep(1);
      setIsPlaying(true);
      setGuidedTourActive(true);
      setShowTourSelection(false);
    }
  };

  const handleExitTour = () => {
    setActiveTour(null);
    setCurrentStep(1);
    setIsPlaying(false);
    setGuidedTourActive(false);
  };

  const handleNext = () => {
    if (activeTour && currentStep < activeTour.steps.length) {
      setCurrentStep(currentStep + 1);
    } else if (activeTour && currentStep === activeTour.steps.length) {
      // Tour complete
      handleExitTour();
    }
  };

  const handlePrevious = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSkipTour = () => {
    handleExitTour();
  };

  const handleJumpToStep = (step: number) => {
    if (activeTour && step >= 1 && step <= activeTour.steps.length) {
      setCurrentStep(step);
    }
  };

  const currentTourStep = activeTour?.steps[currentStep - 1];

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
          onGuidedTourToggle={() => setShowTourSelection(!showTourSelection)}
          recordingActive={recordingActive}
          onRecordingToggle={() => setRecordingActive(!recordingActive)}
        />

        {/* Tour Selection Modal */}
        {showTourSelection && !activeTour && (
          <div
            className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4"
            onClick={() => setShowTourSelection(false)}
          >
            <div
              className="bg-white rounded-lg shadow-2xl p-8 max-w-2xl w-full mx-4 relative z-60"
              onClick={(e) => e.stopPropagation()}
            >
              <h2 className="text-3xl font-bold text-gray-900 mb-2">
                Choose a Guided Tour
              </h2>
              <p className="text-gray-600 mb-6">
                Explore NAV-Losen at your own pace. You can skip any step or exit anytime.
              </p>

              {/* Tour cards */}
              <div className="space-y-4">
                {allTours.map((tour) => (
                  <button
                    key={tour.id}
                    onClick={() => handleStartTour(tour.id)}
                    className="w-full text-left p-6 border-2 border-gray-200 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-all group"
                  >
                    <h3 className="text-xl font-bold text-gray-900 group-hover:text-blue-600 mb-2">
                      {tour.name}
                    </h3>
                    <p className="text-gray-600 mb-3">
                      {tour.description}
                    </p>
                    <div className="flex items-center gap-4 text-sm text-gray-500">
                      <span>⏱️ {tour.duration}</span>
                      <span>📍 {tour.steps.length} steps</span>
                    </div>
                  </button>
                ))}
              </div>

              {/* Close button */}
              <button
                onClick={() => setShowTourSelection(false)}
                className="mt-6 w-full px-6 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors font-medium"
              >
                Close
              </button>
            </div>
          </div>
        )}

        {/* Device Frame with iframe */}
        <DeviceFrame
          deviceType={deviceType}
          iframeSrc={iframeSrc}
        />

        {/* Guided Tour Overlay */}
        {activeTour && (
          <TourOverlay
            isActive={true}
            onExit={handleExitTour}
          >
            {/* Tour Progress Indicator */}
            {activeTour && (
              <TourProgress
                currentStep={currentStep}
                totalSteps={activeTour.steps.length}
                onStepClick={handleJumpToStep}
                allowJump={true}
              />
            )}

            {/* Tour Tooltip */}
            {currentTourStep && (
              <TourTooltip
                title={currentTourStep.title}
                description={currentTourStep.description}
                position={currentTourStep.position}
                targetX={window.innerWidth / 2}
                targetY={window.innerHeight / 2}
                onNext={handleNext}
                onSkip={handleSkipTour}
                showNext={currentStep < activeTour.steps.length}
                showSkip={true}
              />
            )}

            {/* Tour Controller */}
            {activeTour && (
              <TourController
                isPlaying={isPlaying}
                onPlay={() => setIsPlaying(true)}
                onPause={() => setIsPlaying(false)}
                onNext={handleNext}
                onPrevious={handlePrevious}
                onSkip={handleSkipTour}
                onExit={handleExitTour}
                currentStep={currentStep}
                totalSteps={activeTour.steps.length}
              />
            )}
          </TourOverlay>
        )}

        {/* Footer Info */}
        <div className="mt-8 text-center text-sm text-gray-500">
          <p>
            Powered by QDA v2.0 • 14+ Pages • Polyvagal-Adaptive Design
          </p>
          <p className="mt-2">
            Timeline: Dag 3/7 • Status: Guided Tours Integrated ✅
          </p>
        </div>
      </div>
    </div>
  );
}
