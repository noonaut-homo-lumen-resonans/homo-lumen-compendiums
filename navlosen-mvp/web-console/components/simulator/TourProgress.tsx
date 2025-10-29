/**
 * Tour Progress Component
 *
 * Step indicator showing current progress through guided tour.
 * Implements Triadic Ethics:
 * - Port 1: User can see their progress and jump to any step
 * - Port 2: Clear, accessible progress indicators
 * - Port 3: Celebrates each completed step
 *
 * @version 1.0
 * @date 2025-10-22
 * @author Code (Agent #9) - Motor Cortex
 */

'use client';

interface TourProgressProps {
  currentStep: number;
  totalSteps: number;
  onStepClick?: (step: number) => void;
  allowJump?: boolean; // Port 1: Allow jumping to any step
}

export function TourProgress({
  currentStep,
  totalSteps,
  onStepClick,
  allowJump = true,
}: TourProgressProps) {
  return (
    <div className="tour-progress fixed top-20 left-1/2 transform -translate-x-1/2 z-50">
      <div className="bg-white rounded-full shadow-lg px-6 py-3 border border-gray-200">
        {/* Text indicator */}
        <div className="flex items-center gap-4">
          {/* Step counter */}
          <span className="text-sm font-semibold text-gray-700">
            Step {currentStep} of {totalSteps}
          </span>

          {/* Visual progress dots */}
          <div className="flex items-center gap-2">
            {Array.from({ length: totalSteps }).map((_, index) => {
              const step = index + 1;
              const isCompleted = step < currentStep;
              const isCurrent = step === currentStep;
              const isFuture = step > currentStep;

              return (
                <button
                  key={step}
                  onClick={() => allowJump && onStepClick?.(step)}
                  disabled={!allowJump}
                  className={`
                    w-3 h-3 rounded-full transition-all duration-200
                    ${isCompleted ? 'bg-green-500 hover:bg-green-600' : ''}
                    ${isCurrent ? 'bg-blue-600 scale-125' : ''}
                    ${isFuture ? 'bg-gray-300' : ''}
                    ${allowJump && !isCurrent ? 'cursor-pointer' : 'cursor-default'}
                  `}
                  aria-label={`${isCompleted ? 'Completed ' : ''}${isCurrent ? 'Current ' : ''}Step ${step}`}
                  title={allowJump ? `Jump to step ${step}` : `Step ${step}`}
                />
              );
            })}
          </div>

          {/* Progress percentage */}
          <span className="text-xs text-gray-500 font-medium">
            {Math.round((currentStep / totalSteps) * 100)}%
          </span>
        </div>

        {/* Progress bar (visual reinforcement) */}
        <div className="mt-2 h-1 bg-gray-200 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-blue-500 to-green-500 transition-all duration-500 ease-out"
            style={{ width: `${(currentStep / totalSteps) * 100}%` }}
          />
        </div>
      </div>
    </div>
  );
}
