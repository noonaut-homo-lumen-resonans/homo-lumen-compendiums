/**
 * Tour Tooltip Component
 *
 * Annotation boxes with arrows pointing to specific features.
 * Implements Triadic Ethics:
 * - Port 1: User can skip this step
 * - Port 2: NVC language, 8th grade reading level, transparent science
 * - Port 3: Empowerment messaging, celebrates user capacity
 *
 * @version 1.0
 * @date 2025-10-22
 * @author Code (Agent #9) - Motor Cortex
 */

'use client';

interface TourTooltipProps {
  title: string;
  description: string;
  position: 'top' | 'bottom' | 'left' | 'right';
  targetX?: number;
  targetY?: number;
  onNext?: () => void;
  onSkip?: () => void;
  showNext?: boolean;
  showSkip?: boolean;
}

export function TourTooltip({
  title,
  description,
  position = 'right',
  targetX = 0,
  targetY = 0,
  onNext,
  onSkip,
  showNext = true,
  showSkip = true,
}: TourTooltipProps) {
  // Position tooltip relative to target
  const getTooltipPosition = () => {
    const offset = 20; // Distance from target

    switch (position) {
      case 'top':
        return {
          left: `${targetX}px`,
          top: `${targetY - offset}px`,
          transform: 'translate(-50%, -100%)',
        };
      case 'bottom':
        return {
          left: `${targetX}px`,
          top: `${targetY + offset}px`,
          transform: 'translate(-50%, 0)',
        };
      case 'left':
        return {
          left: `${targetX - offset}px`,
          top: `${targetY}px`,
          transform: 'translate(-100%, -50%)',
        };
      case 'right':
        return {
          left: `${targetX + offset}px`,
          top: `${targetY}px`,
          transform: 'translate(0, -50%)',
        };
      default:
        return {};
    }
  };

  // Arrow direction based on position
  const getArrowClass = () => {
    switch (position) {
      case 'top':
        return 'arrow-down';
      case 'bottom':
        return 'arrow-up';
      case 'left':
        return 'arrow-right';
      case 'right':
        return 'arrow-left';
      default:
        return '';
    }
  };

  return (
    <div
      className="tour-tooltip fixed z-50"
      style={getTooltipPosition()}
    >
      {/* Tooltip box */}
      <div className="bg-white rounded-lg shadow-2xl p-6 max-w-sm border-2 border-blue-500">
        {/* Title */}
        <h3 className="text-xl font-bold text-gray-900 mb-3">
          {title}
        </h3>

        {/* Description (NVC language, 8th grade level) */}
        <p className="text-gray-700 mb-4 leading-relaxed">
          {description}
        </p>

        {/* Action buttons */}
        <div className="flex gap-3 justify-end">
          {/* Skip button (Triadic Ethics Port 1 - Cognitive Sovereignty) */}
          {showSkip && onSkip && (
            <button
              onClick={onSkip}
              className="px-4 py-2 text-gray-600 hover:text-gray-800 font-medium transition-colors"
              aria-label="Skip this step"
            >
              Skip
            </button>
          )}

          {/* Next button */}
          {showNext && onNext && (
            <button
              onClick={onNext}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
              aria-label="Next step"
            >
              Next →
            </button>
          )}
        </div>
      </div>

      {/* Arrow pointing to target */}
      <div className={`tooltip-arrow ${getArrowClass()}`} />

      <style jsx>{`
        .tooltip-arrow {
          position: absolute;
          width: 0;
          height: 0;
          border: 10px solid transparent;
        }

        .arrow-left {
          right: 100%;
          top: 50%;
          transform: translateY(-50%);
          border-right-color: #3b82f6;
        }

        .arrow-right {
          left: 100%;
          top: 50%;
          transform: translateY(-50%);
          border-left-color: #3b82f6;
        }

        .arrow-up {
          bottom: 100%;
          left: 50%;
          transform: translateX(-50%);
          border-bottom-color: #3b82f6;
        }

        .arrow-down {
          top: 100%;
          left: 50%;
          transform: translateX(-50%);
          border-top-color: #3b82f6;
        }
      `}</style>
    </div>
  );
}
