"use client";

import React from "react";
import { cn } from "@/lib/utils";
import { StressState } from "@/types";

interface StressSliderProps {
  value: number;
  onChange: (value: number) => void;
  className?: string;
}

/**
 * StressSlider Component
 *
 * Polyvagal-informed stress level slider (1-10)
 * Based on NAV-Losen Design System v1.0
 *
 * Stress States:
 * - 1-3: Ventral Vagal (Calm, green)
 * - 4-7: Sympathetic (Alert, orange)
 * - 8-10: Dorsal Vagal (Freeze, blue)
 *
 * @example
 * <StressSlider value={stressLevel} onChange={setStressLevel} />
 */
export default function StressSlider({
  value,
  onChange,
  className,
}: StressSliderProps) {
  const getStressState = (level: number): StressState => {
    if (level <= 3) return "ventral";
    if (level <= 7) return "sympathetic";
    return "dorsal";
  };

  const getStateColor = (state: StressState): string => {
    switch (state) {
      case "ventral":
        return "#4CAF50"; // Green
      case "sympathetic":
        return "#FF9800"; // Orange
      case "dorsal":
        return "#2196F3"; // Blue
    }
  };

  const getStateLabel = (state: StressState): string => {
    switch (state) {
      case "ventral":
        return "Rolig";
      case "sympathetic":
        return "Aktivert";
      case "dorsal":
        return "Overveldet";
    }
  };

  const currentState = getStressState(value);
  const stateColor = getStateColor(currentState);
  const stateLabel = getStateLabel(currentState);

  return (
    <div className={cn("w-full text-left", className)}>
      {/* Current value display */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-[var(--color-text-primary)] text-left">
          Hvor mye trykk kjenner du på?
        </h3>
        <div className="flex items-center gap-3">
          <span
            className="text-2xl font-bold"
            style={{ color: stateColor }}
            aria-label={`Stressnivå ${value} av 10`}
          >
            {value}
          </span>
          <span
            className="text-sm font-medium px-3 py-1 rounded-full"
            style={{
              backgroundColor: `${stateColor}20`,
              color: stateColor,
            }}
          >
            {stateLabel}
          </span>
        </div>
      </div>

      {/* Slider */}
      <div className="relative">
        <input
          type="range"
          min="1"
          max="10"
          value={value}
          onChange={(e) => onChange(Number(e.target.value))}
          className="w-full h-2 rounded-lg appearance-none cursor-pointer"
          style={{
            background: `linear-gradient(to right,
              #4CAF50 0%,
              #4CAF50 30%,
              #FF9800 30%,
              #FF9800 70%,
              #2196F3 70%,
              #2196F3 100%)`,
          }}
          aria-label="Stressnivå slider fra 1 til 10"
        />

        {/* Labels */}
        <div className="flex justify-between mt-2 text-sm text-[var(--color-text-secondary)]">
          <span>Lite</span>
          <span>Mye</span>
        </div>

        {/* State zone indicators */}
        <div className="flex justify-between mt-4 text-xs text-[var(--color-text-tertiary)]">
          <span className="flex items-center gap-1">
            <span
              className="w-3 h-3 rounded-full"
              style={{ backgroundColor: "#4CAF50" }}
            />
            1-3: Rolig
          </span>
          <span className="flex items-center gap-1">
            <span
              className="w-3 h-3 rounded-full"
              style={{ backgroundColor: "#FF9800" }}
            />
            4-7: Aktivert
          </span>
          <span className="flex items-center gap-1">
            <span
              className="w-3 h-3 rounded-full"
              style={{ backgroundColor: "#2196F3" }}
            />
            8-10: Overveldet
          </span>
        </div>
      </div>

      {/* Accessibility note */}
      <style jsx>{`
        input[type="range"]::-webkit-slider-thumb {
          appearance: none;
          width: 24px;
          height: 24px;
          background: ${stateColor};
          border: 2px solid white;
          border-radius: 50%;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
          cursor: pointer;
        }

        input[type="range"]::-moz-range-thumb {
          width: 24px;
          height: 24px;
          background: ${stateColor};
          border: 2px solid white;
          border-radius: 50%;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
          cursor: pointer;
        }

        input[type="range"]:focus {
          outline: none;
        }

        input[type="range"]:focus-visible {
          outline: 3px solid var(--color-primary);
          outline-offset: 2px;
        }
      `}</style>
    </div>
  );
}
