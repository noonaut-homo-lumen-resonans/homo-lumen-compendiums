/**
 * Tour Controller Component
 *
 * Control panel for guided tour (play, pause, skip, exit).
 * Implements Triadic Ethics:
 * - Port 1: User has full control (play/pause/skip/exit)
 * - Port 2: Clear, accessible controls with labels
 * - Port 3: Empowering messaging ("You're in control")
 *
 * @version 1.0
 * @date 2025-10-22
 * @author Code (Agent #9) - Motor Cortex
 */

'use client';

interface TourControllerProps {
  isPlaying: boolean;
  onPlay?: () => void;
  onPause?: () => void;
  onNext?: () => void;
  onPrevious?: () => void;
  onSkip?: () => void;
  onExit?: () => void;
  currentStep: number;
  totalSteps: number;
}

export function TourController({
  isPlaying,
  onPlay,
  onPause,
  onNext,
  onPrevious,
  onSkip,
  onExit,
  currentStep,
  totalSteps,
}: TourControllerProps) {
  const isFirstStep = currentStep === 1;
  const isLastStep = currentStep === totalSteps;

  return (
    <div className="tour-controller fixed bottom-8 left-1/2 transform -translate-x-1/2 z-50">
      <div className="bg-white rounded-lg shadow-2xl p-4 border border-gray-200">
        {/* Empowerment message (Triadic Ethics Port 3) */}
        <div className="text-center mb-3">
          <p className="text-xs text-gray-600 font-medium">
            You're in control - take it at your own pace
          </p>
        </div>

        {/* Control buttons */}
        <div className="flex items-center gap-2">
          {/* Previous button */}
          <button
            onClick={onPrevious}
            disabled={isFirstStep}
            className={`
              px-4 py-2 rounded-lg font-medium transition-colors
              ${isFirstStep
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }
            `}
            aria-label="Previous step"
            title={isFirstStep ? 'Already at first step' : 'Go to previous step'}
          >
            ← Previous
          </button>

          {/* Play/Pause button */}
          {isPlaying ? (
            <button
              onClick={onPause}
              className="px-6 py-2 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600 transition-colors font-medium"
              aria-label="Pause tour"
            >
              ⏸️ Pause
            </button>
          ) : (
            <button
              onClick={onPlay}
              className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium"
              aria-label="Play tour"
            >
              ▶️ Play
            </button>
          )}

          {/* Next button */}
          <button
            onClick={onNext}
            disabled={isLastStep}
            className={`
              px-4 py-2 rounded-lg font-medium transition-colors
              ${isLastStep
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700'
              }
            `}
            aria-label="Next step"
            title={isLastStep ? 'Already at last step' : 'Go to next step'}
          >
            Next →
          </button>

          {/* Divider */}
          <div className="w-px h-8 bg-gray-300 mx-2" />

          {/* Skip button (Triadic Ethics Port 1) */}
          <button
            onClick={onSkip}
            className="px-4 py-2 text-gray-600 hover:text-gray-800 font-medium transition-colors"
            aria-label="Skip this tour"
            title="Skip to the end of this tour"
          >
            Skip Tour
          </button>

          {/* Exit button (Triadic Ethics Port 1) */}
          <button
            onClick={onExit}
            className="px-4 py-2 text-red-600 hover:text-red-800 font-medium transition-colors"
            aria-label="Exit tour"
            title="Exit and close this tour"
          >
            ❌ Exit
          </button>
        </div>

        {/* Keyboard shortcuts hint */}
        <div className="text-center mt-3 pt-3 border-t border-gray-200">
          <p className="text-xs text-gray-500">
            <span className="font-semibold">Keyboard:</span> ← Previous | → Next | Esc Exit
          </p>
        </div>
      </div>
    </div>
  );
}
