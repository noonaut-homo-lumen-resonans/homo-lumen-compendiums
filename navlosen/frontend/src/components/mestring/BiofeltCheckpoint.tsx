"use client";

import { useState, useEffect } from "react";

/**
 * BiofeltCheckpoint - 4-6-8 Breathing Exercise
 *
 * Visual Metaphor: Gyllent, pulserende punkt (Golden pulsing point)
 * Purpose: Pause, breathe, reconnect with body before continuing
 *
 * Triadisk Ethics:
 * - Suverenitet: User can skip or repeat the exercise
 * - Koherens: Based on 4-6-8 breathing technique (evidence-based)
 * - Healing: Teaches self-regulation, builds capacity
 *
 * Integration: Nyra's Biofelt-checkpoint concept
 */

export interface BiofeltCheckpointProps {
  onComplete?: () => void;
  onSkip?: () => void;
  showSkipButton?: boolean;
}

type BreathPhase = "inhale" | "hold" | "exhale" | "rest";

export default function BiofeltCheckpoint({
  onComplete,
  onSkip,
  showSkipButton = true,
}: BiofeltCheckpointProps) {
  const [phase, setPhase] = useState<BreathPhase>("rest");
  const [countdown, setCountdown] = useState<number>(0);
  const [cycleCount, setCycleCount] = useState<number>(0);
  const [isActive, setIsActive] = useState<boolean>(false);

  // Phase durations in seconds
  const phaseDurations: Record<BreathPhase, number> = {
    inhale: 4,
    hold: 6,
    exhale: 8,
    rest: 2,
  };

  // Start breathing exercise
  const startBreathing = () => {
    setIsActive(true);
    setPhase("inhale");
    setCountdown(phaseDurations.inhale);
    setCycleCount(0);
  };

  // Skip to completion
  const handleSkip = () => {
    setIsActive(false);
    setPhase("rest");
    onSkip?.();
  };

  // Complete checkpoint
  const handleComplete = () => {
    setIsActive(false);
    setPhase("rest");
    onComplete?.();
  };

  // Countdown timer
  useEffect(() => {
    if (!isActive || countdown <= 0) return;

    const timer = setInterval(() => {
      setCountdown((prev) => prev - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [isActive, countdown]);

  // Phase transitions
  useEffect(() => {
    if (!isActive || countdown > 0) return;

    // Move to next phase
    if (phase === "inhale") {
      setPhase("hold");
      setCountdown(phaseDurations.hold);
    } else if (phase === "hold") {
      setPhase("exhale");
      setCountdown(phaseDurations.exhale);
    } else if (phase === "exhale") {
      // Complete one cycle
      const newCycleCount = cycleCount + 1;
      setCycleCount(newCycleCount);

      // After 3 cycles (54 seconds total), auto-complete
      if (newCycleCount >= 3) {
        handleComplete();
      } else {
        // Start new cycle
        setPhase("rest");
        setCountdown(phaseDurations.rest);
      }
    } else if (phase === "rest") {
      setPhase("inhale");
      setCountdown(phaseDurations.inhale);
    }
  }, [countdown, phase, isActive, cycleCount]);

  // Phase messages in Norwegian
  const phaseMessages: Record<BreathPhase, string> = {
    inhale: "Pust inn...",
    hold: "Hold...",
    exhale: "Pust ut...",
    rest: "Rolig...",
  };

  // Phase colors
  const phaseColors: Record<BreathPhase, string> = {
    inhale: "from-cyan-400 to-blue-500",
    hold: "from-blue-500 to-purple-500",
    exhale: "from-purple-500 to-pink-400",
    rest: "from-green-400 to-teal-400",
  };

  return (
    <div className="w-full">
      <div className="bg-gradient-to-br from-blue-50 to-cyan-50 rounded-2xl p-8 shadow-lg mx-auto" style={{ maxWidth: "700px" }}>
        {/* Header */}
        <div className="text-center mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Biofelt-checkpoint
          </h2>
          <p className="text-gray-600">
            Pust. Føl deg selv. Nå er du klar til å fortsette.
          </p>
        </div>

        {!isActive ? (
          /* Start State */
          <div className="text-center">
            <div className="mb-8">
              <div className="inline-block w-32 h-32 rounded-full bg-gradient-to-br from-yellow-300 to-amber-400 pulse-glow"></div>
            </div>

            <p className="text-lg text-gray-700 mb-6">
              Ta en kort pause med 4-6-8 pustemetoden.
              <br />
              <span className="text-sm text-gray-500">
                (3 sykluser, ca. 1 minutt)
              </span>
            </p>

            <div className="flex gap-4 justify-center">
              <button
                onClick={startBreathing}
                className="px-6 py-3 bg-gradient-to-r from-blue-500 to-cyan-500 text-white rounded-lg font-medium hover:from-blue-600 hover:to-cyan-600 transition-all calm-hover"
              >
                Start pusteøvelse
              </button>

              {showSkipButton && (
                <button
                  onClick={handleSkip}
                  className="px-6 py-3 bg-white border-2 border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 transition-all calm-hover"
                >
                  Hopp over
                </button>
              )}
            </div>
          </div>
        ) : (
          /* Breathing State */
          <div className="text-center">
            {/* Animated breathing circle */}
            <div className="mb-8 flex items-center justify-center">
              <div
                className={`w-48 h-48 rounded-full bg-gradient-to-br ${phaseColors[phase]} breathe-animation transition-all duration-1000`}
                style={{
                  transform:
                    phase === "inhale" || phase === "hold"
                      ? "scale(1.3)"
                      : "scale(1)",
                }}
              ></div>
            </div>

            {/* Phase instruction */}
            <div className="mb-6">
              <p className="text-3xl font-bold text-gray-900 mb-2">
                {phaseMessages[phase]}
              </p>
              <p className="text-6xl font-bold text-gray-700">{countdown}</p>
            </div>

            {/* Cycle counter */}
            <div className="mb-6">
              <div className="flex gap-2 justify-center">
                {[1, 2, 3].map((cycle) => (
                  <div
                    key={cycle}
                    className={`w-3 h-3 rounded-full transition-all ${
                      cycle <= cycleCount
                        ? "bg-green-500"
                        : cycle === cycleCount + 1
                        ? "bg-blue-500 pulse-glow"
                        : "bg-gray-300"
                    }`}
                  ></div>
                ))}
              </div>
              <p className="text-sm text-gray-500 mt-2">
                Syklus {cycleCount + 1} av 3
              </p>
            </div>

            {/* Early completion option */}
            <button
              onClick={handleComplete}
              className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800 underline"
            >
              Fullfør nå
            </button>
          </div>
        )}
      </div>

      {/* Explanation */}
      <div className="mt-6 text-center text-sm text-gray-500">
        <p>
          4-6-8 metoden: Pust inn (4 sek), hold (6 sek), pust ut (8 sek)
        </p>
        <p>Aktiverer parasympatiske nervesystem og gir ro.</p>
      </div>
    </div>
  );
}
